
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

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ServiceReport(Base):
    __tablename__ = "service_reports"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="SET NULL"), nullable=True)
    kind = Column(String(40), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
