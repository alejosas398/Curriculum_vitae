from django.conf import settings
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, AzureError
import os


def _get_service_client():
    conn_str = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
    if not conn_str:
        raise RuntimeError('AZURE_STORAGE_CONNECTION_STRING is not configured')
    return BlobServiceClient.from_connection_string(conn_str)


def upload_blob_bytes(blob_name: str, data: bytes, content_type: str = None) -> bool:
    """Upload bytes to Azure Blob Storage.

    Returns True if successful, False otherwise.
    """
    if not blob_name or not data:
        return False

    container = getattr(settings, 'AZURE_CONTAINER_NAME', None) or 'cursos'
    try:
        svc = _get_service_client()
        blob_client = svc.get_blob_client(container=container, blob=blob_name)

        # Set content type if provided
        blob_kwargs = {}
        if content_type:
            blob_kwargs['content_type'] = content_type

        blob_client.upload_blob(data, overwrite=True, **blob_kwargs)
        return True
    except AzureError as e:
        print(f"Error uploading to Azure: {e}")
        return False


def upload_file_to_blob(file_path: str, blob_name: str) -> bool:
    """Upload a file from local filesystem to Azure Blob Storage.

    Returns True if successful, False otherwise.
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            # Determine content type based on file extension
            content_type = None
            if file_path.lower().endswith(('.jpg', '.jpeg')):
                content_type = 'image/jpeg'
            elif file_path.lower().endswith('.png'):
                content_type = 'image/png'
            elif file_path.lower().endswith('.gif'):
                content_type = 'image/gif'
            elif file_path.lower().endswith('.webp'):
                content_type = 'image/webp'
            elif file_path.lower().endswith('.pdf'):
                content_type = 'application/pdf'

            return upload_blob_bytes(blob_name, data, content_type)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False


def download_blob_bytes(blob_name: str) -> bytes | None:
    """Download a blob from the configured container and return its bytes.

    Returns None if the blob does not exist or on error.
    """
    if not blob_name:
        return None
    container = getattr(settings, 'AZURE_CONTAINER_NAME', None) or 'cursos'
    try:
        svc = _get_service_client()
        blob_client = svc.get_blob_client(container=container, blob=blob_name)
        stream = blob_client.download_blob()
        return stream.readall()
    except ResourceNotFoundError:
        return None
    except AzureError:
        return None
