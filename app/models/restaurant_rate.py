import sqlalchemy as sa

from app.database import db

users_rates = sa.Table(
    "restaurant_rates",
    db.Model.metadata,
    sa.Column(
        "restaurant_id", sa.ForeignKey("restaurants.id"), primary_key=True
    ),  # noqa E501
    sa.Column("rate_id", sa.ForeignKey("rates.id"), primary_key=True),
)
