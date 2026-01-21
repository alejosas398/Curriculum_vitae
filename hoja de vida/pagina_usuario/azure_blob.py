from django.conf import settings
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, AzureError


def _get_service_client():
    conn_str = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', None)
    if not conn_str:
        raise RuntimeError('AZURE_STORAGE_CONNECTION_STRING is not configured')
    return BlobServiceClient.from_connection_string(conn_str)


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
