from qdrant_client import QdrantClient

from movemate.config import settings


qdrant_client = QdrantClient(url=settings.qdrant_url)