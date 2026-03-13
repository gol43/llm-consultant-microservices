import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.deps import get_db
from app.db.base import Base
from app.main import app

# Тестовая БД в памяти
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(TEST_DATABASE_URL)
AsyncSessionTest = async_sessionmaker(bind=engine_test, class_=AsyncSession)

# Фикстура для клиента
@pytest.fixture
async def client():
    # Создаем таблицы перед тестом
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Переопределяем зависимость БД
    async def override_get_db():
        async with AsyncSessionTest() as session:
            yield session
            
    app.dependency_overrides[get_db] = override_get_db
    
    # Используем AsyncClient для асинхронных тестов (из урока 3)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    # Очищаем переопределения после теста (важное правило из урока 3)
    app.dependency_overrides.clear()
    
    # Удаляем таблицы
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)