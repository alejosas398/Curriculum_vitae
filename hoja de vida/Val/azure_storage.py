"""
Custom storage backend for Azure Blob Storage media files.
This ensures media files (photos, certificates) are stored in Azure instead of local filesystem.
"""

from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import File
from io import BytesIO
import os
import uuid
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import AzureError, ResourceNotFoundError


class AzureBlobStorage(Storage):
    """Custom storage class for Azure Blob Storage"""

    def __init__(self):
        self.connection_string = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', '')
        self.container_name = getattr(settings, 'AZURE_CONTAINER_NAME', 'media')
        self.account_name = self._extract_account_name()

        # Only raise error if we're trying to use Azure storage
        if not self.connection_string:
            import logging
            logging.warning('AZURE_STORAGE_CONNECTION_STRING not configured, Azure storage operations may fail')

    def _get_service_client(self):
        """Get Azure Blob Service Client"""
        if not self.connection_string:
            raise ValueError('AZURE_STORAGE_CONNECTION_STRING must be configured in settings')
        return BlobServiceClient.from_connection_string(self.connection_string)

    def _extract_account_name(self):
        """Extract account name from connection string"""
        if 'AccountName=' in self.connection_string:
            start = self.connection_string.find('AccountName=') + len('AccountName=')
            end = self.connection_string.find(';', start)
            if end == -1:
                end = len(self.connection_string)
            return self.connection_string[start:end]
        return None

    def _open(self, name, mode='rb'):
        """Open a file for reading"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            stream = blob_client.download_blob()
            return BytesIO(stream.readall())
        except (AzureError, ResourceNotFoundError) as e:
            raise FileNotFoundError(f'Blob {name} not found in Azure: {str(e)}')

    def _save(self, name, content):
        """Save a file to Azure Blob Storage"""
        if not name:
            name = str(uuid.uuid4())
        
        # Keep the original name to make URLs more predictable
        # UUID will be added only if needed to avoid conflicts
        
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )

            # Determine content type
            content_type = getattr(content, 'content_type', None)
            if not content_type:
                if name.lower().endswith(('.jpg', '.jpeg')):
                    content_type = 'image/jpeg'
                elif name.lower().endswith('.png'):
                    content_type = 'image/png'
                elif name.lower().endswith('.gif'):
                    content_type = 'image/gif'
                elif name.lower().endswith('.pdf'):
                    content_type = 'application/pdf'
                elif name.lower().endswith('.webp'):
                    content_type = 'image/webp'

            # Upload to Azure (overwrite if exists)
            if hasattr(content, 'read'):
                blob_client.upload_blob(content, overwrite=True, content_settings={'content_type': content_type} if content_type else {})
            else:
                blob_client.upload_blob(content, overwrite=True, content_settings={'content_type': content_type} if content_type else {})

            return name
        except AzureError as e:
            raise IOError(f'Error saving blob {name} to Azure: {str(e)}')

    def delete(self, name):
        """Delete a file from Azure Blob Storage"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            blob_client.delete_blob()
        except (AzureError, ResourceNotFoundError):
            pass  # Blob already deleted or doesn't exist

    def exists(self, name):
        """Check if a file exists in Azure Blob Storage"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            return blob_client.exists()
        except AzureError:
            return False

    def listdir(self, path):
        """List files in a directory"""
        try:
            service_client = self._get_service_client()
            container_client = service_client.get_container_client(self.container_name)
            
            directories = set()
            files = []
            
            blobs = container_client.list_blobs(name_starts_with=path)
            for blob in blobs:
                blob_name = blob.name
                if path and not blob_name.startswith(path):
                    continue
                
                relative_name = blob_name[len(path):] if path else blob_name
                if '/' in relative_name:
                    dir_name = relative_name.split('/')[0]
                    directories.add(dir_name)
                else:
                    files.append(relative_name)
            
            return list(directories), files
        except AzureError:
            return [], []

    def size(self, name):
        """Get the size of a file"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            properties = blob_client.get_blob_properties()
            return properties.size
        except AzureError:
            return 0

    def url(self, name):
        """Get the URL of a file with SAS token for access"""
        if not self.account_name:
            return f'/media/{name}'
        
        try:
            # Try to generate SAS URL (if account key is available)
            if 'AccountKey=' in self.connection_string:
                # Extract account key
                start = self.connection_string.find('AccountKey=') + len('AccountKey=')
                end = self.connection_string.find(';', start)
                if end == -1:
                    end = len(self.connection_string)
                account_key = self.connection_string[start:end]
                
                # Generate SAS token (valid for 30 days - long enough for most images)
                sas_token = generate_blob_sas(
                    account_name=self.account_name,
                    container_name=self.container_name,
                    blob_name=name,
                    account_key=account_key,
                    permission=BlobSasPermissions(read=True),
                    expiry=datetime.utcnow() + timedelta(days=30)
                )
                
                base_url = f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{name}'
                return f'{base_url}?{sas_token}'
        except Exception as e:
            import logging
            logging.warning(f'Could not generate SAS token: {str(e)}')
        
        # Fallback URL (requires public access, which may not work)
        return f'https://{self.account_name}.blob.core.windows.net/{self.container_name}/{name}'

    def get_accessed_time(self, name):
        """Get last accessed time"""
        raise NotImplementedError('Azure Blob Storage does not support accessed time')

    def get_created_time(self, name):
        """Get creation time"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            properties = blob_client.get_blob_properties()
            return properties.creation_time
        except AzureError:
            return None

    def get_modified_time(self, name):
        """Get modification time"""
        try:
            service_client = self._get_service_client()
            blob_client = service_client.get_blob_client(
                container=self.container_name,
                blob=name
            )
            properties = blob_client.get_blob_properties()
            return properties.last_modified
        except AzureError:
            return None
