from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from .meta import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    referral = Column(UUID(as_uuid=True), ForeignKey('referral.id'), nullable=True)
    balance = Column(Integer, default=0)
    total_referrals = Column(Integer, default=0)


class Referral(Base):
    __tablename__ = 'referral'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    num_referrals = Column(Integer, default=0)


Index('email_index', User.email, unique=True, mysql_length=255)
Index('referral_index', Referral.id, unique=True, mysql_length=255)