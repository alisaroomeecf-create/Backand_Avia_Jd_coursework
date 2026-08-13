from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL="postgresql+asyncpg://postgres:Anna_95@localhost:5432/backendavia"
engine=create_async_engine(DATABASE_URL,echo=True)
SessionLocal=async_sessionmaker(bind=engine,expire_on_commit=False)
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session