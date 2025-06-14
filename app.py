from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager

from tables import Base, Group
from configs import ENGINE, ASYNC_SESSION, IMAGE_BASE_URL


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await ENGINE.dispose()


@app.get("/friend_groups")
async def get_group_data():
    async with ASYNC_SESSION() as session:
        result = await session.execute(select(Group).options(selectinload(Group.group_list)))
        groups = result.scalars().all()
        data = []
        for g in groups:
            group_list = [
                {
                    "name": x.name,
                    "avatar": IMAGE_BASE_URL + x.avatar if x.avatar else None,
                    "bg": IMAGE_BASE_URL + x.bg if x.bg else None,
                    "group_info": x.group_info,
                    "detail": x.detail,
                }
                for x in g.group_list
            ]
            if group_list:
                data.append({"group": g.group, "group_list": group_list})
        return data

app = FastAPI(lifespan=lifespan)