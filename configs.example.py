from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

HOST = "127.0.0.1"
PORT = 2123
DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/yourdb"
ENGINE = create_async_engine(DATABASE_URL)
ASYNC_SESSION = async_sessionmaker(ENGINE, expire_on_commit=False)
IMAGE_BASE_URL = "https://example.com/"
