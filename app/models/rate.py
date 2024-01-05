import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import generate_uuid

from .restaurant import Restaurant


class Rate(db.Model):
    __tablename__ = "rates"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        unique=True,
        default=generate_uuid,
    )
    user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("users.id"), nullable=False)

    # rate based on order_id
    # order_id: orm.Mapped[int] = orm.mapped_column(
    #     sa.ForeignKey("orders.id"), nullable=False
    # )

    restaurant_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("restaurants.id"), nullable=False)
    rate: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    # rate range limit
    sa.CheckConstraint("rate >= 1 AND rate <= 5")

    restaurant: orm.Mapped[Restaurant] = orm.relationship(
        "Restaurant",
        foreign_keys=[restaurant_id],
        viewonly=True,
        backref="ratings",
    )

    def __repr__(self):
        return f"<{self.id}: {self.rate}>"
