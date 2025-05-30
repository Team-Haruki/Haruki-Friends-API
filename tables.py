from sqlalchemy import String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group: Mapped[str] = mapped_column(String(64), unique=True)
    group_list: Mapped[list["GroupList"]] = relationship("GroupList", back_populates="group", lazy="selectin")


class GroupList(Base):
    __tablename__ = "group_lists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    name: Mapped[str] = mapped_column(String(64))
    avatar: Mapped[str] = mapped_column(String(500), nullable=True)
    bg: Mapped[str] = mapped_column(String(500), nullable=True)
    group_info: Mapped[str] = mapped_column(String(100))
    detail: Mapped[str] = mapped_column(String(300))

    group: Mapped["Group"] = relationship("Group", back_populates="group_list")
