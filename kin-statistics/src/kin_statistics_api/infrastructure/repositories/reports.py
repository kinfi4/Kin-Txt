import logging
from typing import Any, cast

from sqlalchemy import desc
from sqlalchemy.orm import Session

from kin_txt_core.database import Database

from kin_statistics_api.domain.entities import (
    BaseReport,
    ReportIdentificationEntity,
    StatisticalReport,
    WordCloudReport,
    ReportsFetchSettings,
)
from kin_statistics_api.infrastructure.models import Report
from kin_statistics_api.exceptions import ImpossibleToModifyProcessingReport, ReportNotFound
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.constants import ReportProcessingResult, ReportTypes, ITEMS_PER_PAGE


class ReportsRepository(IReportRepository):
    def __init__(self, db: Database) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    def save_finished_report(self, finished_report: WordCloudReport | StatisticalReport) -> None:
        with self._db.session() as session:
            session: Session

            report: Report = session.query(Report).get(finished_report.report_id)

            report.processing_status = finished_report.processing_status
            report.report_warnings = finished_report.report_warnings
            report.report_failed_reason = finished_report.report_failed_reason

            report.report_data = finished_report.get_report_data_dict()

            session.commit()

            self._logger.info(f"[ReportsRepository] Finished report {report.report_id=} {report.name=} was saved")

    def update_report_status(self, report_id: int, status: ReportProcessingResult) -> None:
        with self._db.session() as session:
            session: Session

            report = session.query(Report).get(report_id)
            report.processing_status = status

    def get_user_reports(
        self,
        username: str,
        fetch_settings: ReportsFetchSettings | None,
    ) -> tuple[list[ReportIdentificationEntity], int]:
        with self._db.session() as session:
            session: Session

            reports_query = session.query(Report).filter(Report.owner_username == username)

            if fetch_settings is not None:
                reports_query = self._apply_filters(reports_query, fetch_settings)

        return [
            self._map_dict_to_identification_entity(cast(Report, report))
            for report in reports_query.all()
        ], reports_query.count()

    def get_report_names(
        self,
        report_ids: list[int],
        apply_settings: ReportsFetchSettings | None = None,
    ) -> list[ReportIdentificationEntity]:
        with self._db.session() as session:
            session: Session

            reports_query = session.query(Report).filter(Report.report_id.in_(report_ids))

            if apply_settings is not None:
                reports_query = self._apply_filters(reports_query, apply_settings)

        return [
            self._map_dict_to_identification_entity(cast(Report, report))
            for report in reports_query.all()
        ]

    def create_user_report(
        self,
        username: str,
        report_name: str,
        report_type: ReportTypes,
        processing_status: ReportProcessingResult,
    ) -> int:
        """
        Must return report id
        """

        with self._db.session() as session:
            session: Session

            report = Report(
                name=report_name,
                report_type=report_type,
                processing_status=processing_status,
                owner_username=username,
            )

            session.add(report)
            session.commit()

            self._logger.info(f"[ReportsRepository] Report {report_name=} was saved")

            return report.report_id

    def update_report_name(self, report_id: int, report_name: str) -> ReportIdentificationEntity:
        report = self.get_report(report_id)

        if report.processing_status == ReportProcessingResult.PROCESSING:
            raise ImpossibleToModifyProcessingReport("You can not change the report during processing.")

        with self._db.session() as session:
            session: Session

            updated_report = session.query(Report).get(report_id)
            updated_report.name = report_name

        return self._map_dict_to_identification_entity(updated_report)

    def get_report(self, report_id: int) -> BaseReport | StatisticalReport | WordCloudReport:
        with self._db.session() as session:
            session: Session

            orm_report = session.query(Report).get(report_id)

        if orm_report is None:
            raise ReportNotFound("Report with this id was not found")

        return self._map_orm_object_to_entity(orm_report)

    def delete_report(self, report_id: int) -> None:
        with self._db.session() as session:
            session: Session

            if (report := session.query(Report).get(report_id)) is None:
                return None

            session.delete(report)

    def report_exists(self, report_id: int) -> bool:
        with self._db.session() as session:
            session: Session

            return session.query(Report).filter(Report.report_id == report_id).count() > 0

    def get_total_reports_count(self, filters: ReportsFetchSettings | None) -> int:
        with self._db.session() as session:
            session: Session

            reports_query = session.query(Report)

            if filters is not None:
                reports_query = self._apply_filters(reports_query, filters)

            return reports_query.count()

    def _apply_filters(self, reports_query: Any, filters: ReportsFetchSettings) -> Any:
        if filters.name is not None:
            reports_query = reports_query.filter(Report.name.ilike(f"%{filters.name}%"))
        if filters.date_from is not None:
            reports_query = reports_query.filter(Report.generation_date >= filters.date_from)
        if filters.date_to is not None:
            reports_query = reports_query.filter(Report.generation_date <= filters.date_to)
        if filters.processing_status is not None:
            reports_query = reports_query.filter(Report.processing_status == filters.processing_status)
        if filters.report_type is not None:
            reports_query = reports_query.filter(Report.report_type == filters.report_type)

        if filters.order_by is not None:
            if filters.descending:
                reports_query = reports_query.order_by(desc(filters.order_by))
            else:
                reports_query = reports_query.order_by(filters.order_by)

        if filters.page is not None:
            reports_query = reports_query.offset(filters.page * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE)

        return reports_query

    def _map_dict_to_identification_entity(self, orm_report: Report) -> ReportIdentificationEntity:
        return ReportIdentificationEntity(
            report_id=orm_report.report_id,
            name=orm_report.name,
            processing_status=orm_report.processing_status,
            report_type=orm_report.report_type,
            generation_date=orm_report.generation_date,
        )

    def _map_orm_object_to_entity(
        self,
        orm_report: Report,
    ) -> BaseReport | StatisticalReport | WordCloudReport:
        """
            Returns BaseReport if report is still processing
            Returns WordCloudReport if report is of type WordCloud
            Returns StatisticalReport if report is of type Statistical
        """

        base_report_dict_values = {
            "report_id": orm_report.report_id,
            "name": orm_report.name,
            "report_type": orm_report.report_type,
            "processing_status": orm_report.processing_status,
            "generation_date": orm_report.generation_date,
            "report_failed_reason": orm_report.report_failed_reason,
            "report_warnings": orm_report.report_warnings,
        }

        if orm_report.processing_status in (ReportProcessingResult.NEW, ReportProcessingResult.PROCESSING):
            return BaseReport(**base_report_dict_values)

        if orm_report.report_type == ReportTypes.WORD_CLOUD:
            return WordCloudReport(
                posts_categories=orm_report.report_data["posts_categories"],
                total_words=orm_report.report_data["total_words"],
                total_words_frequency=orm_report.report_data["total_words_frequency"],
                data_by_channel=orm_report.report_data["data_by_channel"],
                data_by_category=orm_report.report_data["data_by_category"],
                data_by_channel_by_category=orm_report.report_data["data_by_channel_by_category"],
                **base_report_dict_values
            )

        return StatisticalReport(
            total_messages_count=orm_report.report_data["total_messages_count"],
            posts_categories=orm_report.report_data["posts_categories"],
            visualization_diagrams_list=orm_report.report_data["visualization_diagrams_list"],
            data=orm_report.report_data["data"],
            **base_report_dict_values
        )
