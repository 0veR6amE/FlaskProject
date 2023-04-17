import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm


from .db_session import SqlAlchemyBase


class Value(SqlAlchemyBase):
    __tablename__ = 'values'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
