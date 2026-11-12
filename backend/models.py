from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)

    authority = Column(String(255))
    eligibility = Column(Text)
    documents = Column(Text)
    steps = Column(Text)

    official_source = Column(String(1000))
    last_reviewed = Column(DateTime(timezone=True))
    status = Column(String(50), default="draft")

    created_at = Column(DateTime, server_default=func.now())


class ServiceLocation(Base):
    __tablename__ = "service_locations"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    governorate = Column(String(100), nullable=True)
    latitude = Column(String(40), nullable=True)
    longitude = Column(String(40), nullable=True)
    phone = Column(String(80), nullable=True)
    working_hours = Column(Text, nullable=True)
    official_source = Column(String(1000), nullable=False)
    last_verified = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="draft")


class ServiceReport(Base):
    __tablename__ = "service_reports"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="SET NULL"), nullable=True)
    kind = Column(String(40), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(60), nullable=False, index=True)
    service_id = Column(Integer, nullable=True, index=True)
    service_name = Column(String(255), nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), index=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(60), nullable=True)
    email = Column(String(254), nullable=False, unique=True, index=True)
    display_name = Column(String(60), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuthSession(Base):
    __tablename__ = "auth_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(64), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserFavorite(Base):
    __tablename__ = "user_favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True)
