import pytest
from sqlalchemy import text

from movemate.infrastructure.database import AsyncSessionLocal


@pytest.mark.anyio
async def test_database_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()

        assert value == 1