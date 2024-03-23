from datetime import datetime

from sqlalchemy import String, DateTime, func, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from kin_txt_core.database import Base
from kin_txt_core.reports_building.constants import ModelTypes, ClassificationScopes

from kin_statistics_api.constants import (
    ReportProcessingResult,
    ReportTypes,
)


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(primary_key=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    simultaneous_reports_generation: Mapped[int] = mapped_column(nullable=False, default=0)

    reports: Mapped[list["Report"]] = relationship(back_populates="user")
    generation_templates: Mapped[list["GenerationTemplate"]] = relationship(back_populates="user")


class Report(Base):
    __tablename__ = "report"

    report_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    report_type: Mapped[ReportTypes] = mapped_column(nullable=False)
    processing_status: Mapped[ReportProcessingResult] = mapped_column(nullable=False)
    generation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    report_failed_reason: Mapped[str | None] = mapped_column(nullable=True)
    report_warnings: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    report_data: Mapped[JSONB] = mapped_column(JSONB, nullable=True)

    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates="reports")


class GenerationTemplate(Base):
    __tablename__ = "generation_template"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    channel_list: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    from_date: Mapped[datetime] = mapped_column(nullable=False)
    to_date: Mapped[datetime] = mapped_column(nullable=False)
    report_type: Mapped[ReportTypes] = mapped_column(nullable=False)
    template_id: Mapped[str] = mapped_column(nullable=True)
    model_code: Mapped[str] = mapped_column(nullable=False)
    report_name: Mapped[str] = mapped_column(nullable=False)
    datasource_type: Mapped[str] = mapped_column(nullable=False)
    model_type: Mapped[ModelTypes] = mapped_column(nullable=False)
    classification_scope: Mapped[ClassificationScopes] = mapped_column(
        nullable=False,
        default=ClassificationScopes.ENTIRE_POST,
    )

    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship(back_populates="generation_templates")
