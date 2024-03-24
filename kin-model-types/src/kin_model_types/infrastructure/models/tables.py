from sqlalchemy import ForeignKey, ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from kin_txt_core.database import Base
from kin_txt_core.reports_building.constants import ModelTypes, ModelStatuses
from kin_txt_core.reports_building.domain.entities.preprocessing import PossiblePaddingTruncating


class PreprocessingConfig(Base):
    __tablename__ = "model_preprocessing_config"

    lowercase: Mapped[bool] = mapped_column(nullable=False, default=True)
    remove_links: Mapped[bool] = mapped_column(nullable=False, default=True)
    remove_emoji: Mapped[bool] = mapped_column(nullable=False, default=False)
    remove_punctuation: Mapped[bool] = mapped_column(nullable=False, default=True)
    remove_extra_spaces: Mapped[bool] = mapped_column(nullable=False, default=True)
    remove_html_tags: Mapped[bool] = mapped_column(nullable=False, default=True)

    remove_stop_words: Mapped[bool] = mapped_column(nullable=False)
    stop_words_file_original_name: Mapped[str | None] = mapped_column(nullable=True)

    lemmatize_text: Mapped[bool] = mapped_column(nullable=False)
    language: Mapped[str | None] = mapped_column(nullable=True)

    max_tokens: Mapped[int | None] = mapped_column(nullable=True)
    padding: Mapped[PossiblePaddingTruncating] = mapped_column(nullable=False)
    truncating: Mapped[PossiblePaddingTruncating] = mapped_column(nullable=False)

    model: Mapped["Model"] = relationship(back_populates="preprocessing_config", uselist=False)
    model_code: Mapped[str] = mapped_column(ForeignKey("model.code", ondelete="CASCADE"), primary_key=True)


class Model(Base):
    __tablename__ = "model"

    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    model_type: Mapped[ModelTypes] = mapped_column(nullable=False)
    category_mapping: Mapped[JSONB] = mapped_column(JSONB, nullable=False)
    model_status: Mapped[ModelStatuses] = mapped_column(nullable=False)

    validation_message: Mapped[str | None] = mapped_column(nullable=True)

    original_model_file_name: Mapped[str | None] = mapped_column(nullable=True)
    original_tokenizer_file_name: Mapped[str | None] = mapped_column(nullable=True)

    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username"), nullable=False)

    preprocessing_config: Mapped[PreprocessingConfig | None] = relationship(back_populates="model", uselist=False)


class VisualizationTemplate(Base):
    __tablename__ = "visualization_template"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    content_types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    visualization_diagram_types: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    owner_username: Mapped[str] = mapped_column(ForeignKey("user.username"), nullable=False)
