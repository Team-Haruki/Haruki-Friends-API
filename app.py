import asyncio
from sqlalchemy import select
from quart import Quart, jsonify
from hypercorn.asyncio import serve
from hypercorn.config import Config
from sqlalchemy.orm import selectinload

from tables import Base, Group
from configs import ENGINE, ASYNC_SESSION, HOST, PORT

app = Quart(__name__)


@app.before_serving
async def setup_db():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.route("/friend_groups")
async def get_group_data():
    async with ASYNC_SESSION() as session:
        result = await session.execute(select(Group).options(selectinload(Group.group_list)))
        groups = result.scalars().all()
        data = []
        for g in groups:
            group_list = [
                {"name": x.name, "avatar": x.avatar, "bg": x.bg, "group_info": x.group_info, "detail": x.detail}
                for x in g.group_list
            ]
            if group_list:
                data.append({"group": g.group, "group_list": group_list})
        return jsonify(data)


@app.after_serving
async def shutdown():
    await ENGINE.dispose()


if __name__ == "__main__":
    config = Config()
    config.bind = [f"{HOST}:{PORT}"]
    asyncio.run(serve(app, config))
