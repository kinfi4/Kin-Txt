import logging
from typing import Any, Mapping

from pymongo import MongoClient, ReturnDocument

from kin_statistics_api.domain.entities import (
    BaseReport,
    ReportIdentificationEntity,
    StatisticalReport,
    WordCloudReport,
    ReportsFetchSettings,
)
from kin_statistics_api.exceptions import ImpossibleToModifyProcessingReport, ReportNotFound
from kin_statistics_api.infrastructure.interfaces import IReportRepository
from kin_statistics_api.constants import ReportProcessingResult, ReportTypes, ITEMS_PER_PAGE


class ReportsMongoRepository(IReportRepository):
    def __init__(self, mongo_client: MongoClient) -> None:
        self._mongo_client = mongo_client
        self._reports_db = mongo_client["statistics_service"]
        self._reports_collection = self._reports_db["reports"]

        self._logger = logging.getLogger(self.__class__.__name__)

    def update_report_status(self, report_id: int, status: ReportProcessingResult) -> None:
        self._reports_collection.find_one_and_update(
            {"report_id": report_id},
            {"$set": {"processing_status": status}},
        )

    def get_report_names(
        self,
        report_ids: list[int],
        apply_settings: ReportsFetchSettings | None = None,
    ) -> list[ReportIdentificationEntity]:
        filters = {"report_id": {"$in": report_ids}}
        filters.update(self._build_mongo_filters(apply_settings))

        reports_cursor = self._reports_collection.find(filters)

        if apply_settings is not None:
            if apply_settings.order_by is not None:
                reports_cursor = reports_cursor.sort(apply_settings.order_by, -1 if apply_settings.descending else 1)
            if apply_settings.page is not None:
                reports_cursor = reports_cursor.skip(apply_settings.page*ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE)

        return [
            self._map_dict_to_identification_entity(report_dict)
            for report_dict in reports_cursor
        ]

    def save_user_report(self, report: BaseReport) -> None:
        self._logger.info(
            f"[ReportsMongoRepository] "
            f"Saving user report with id: {report.report_id} and status: {report.processing_status}"
        )

        report_dict = report.dict()
        self._reports_collection.replace_one(
            {"report_id": report.report_id},
            report_dict,
            upsert=True,
        )

    def update_report_name(self, report_id: int, report_name: str) -> ReportIdentificationEntity:
        report = self.get_report(report_id)

        if report.processing_status == ReportProcessingResult.PROCESSING:
            raise ImpossibleToModifyProcessingReport("You can not change the report during processing.")

        updated_report = self._reports_collection.find_one_and_update(
            {"report_id": report_id},
            {"$set": {"name": report_name}},
            return_document=ReturnDocument.AFTER,
        )

        return self._map_dict_to_identification_entity(updated_report)

    def get_report(self, report_id: int) -> BaseReport | StatisticalReport | WordCloudReport:
        dict_report = self._reports_collection.find_one({
            "report_id": report_id
        })

        if dict_report is None:
            raise ReportNotFound("Report with this id was not found")

        return self._map_dict_to_entity(dict_report)

    def delete_report(self, report_id: int) -> None:
        dict_report = self._reports_collection.find_one({
            "report_id": report_id
        })

        if dict_report is None:
            return

        self._reports_collection.delete_one({
            "report_id": report_id
        })

    def report_exists(self, report_id: int) -> bool:
        return self._reports_collection.count_documents({"report_id": report_id}) > 0

    def get_total_reports_count(self, filters: ReportsFetchSettings | None) -> int:
        mongo_filters = self._build_mongo_filters(filters)

        return self._reports_collection.count_documents(mongo_filters)

    def _map_dict_to_identification_entity(self, dict_report: dict[str, Any]) -> ReportIdentificationEntity:
        return ReportIdentificationEntity(
            report_id=dict_report["report_id"],
            name=dict_report["name"],
            processing_status=dict_report["processing_status"],
            report_type=dict_report["report_type"],
            generation_date=dict_report["generation_date"],
        )

    def _map_dict_to_entity(self, dict_report: Mapping[str, Any]) -> BaseReport | StatisticalReport | WordCloudReport:
        """
            Returns BaseReport if report is still processing
            Returns WordCloudReport if report is of type WordCloud
            Returns StatisticalReport if report is of type Statistical
        """

        if dict_report.get("processing_status") in (ReportProcessingResult.NEW, ReportProcessingResult.PROCESSING):
            return BaseReport(**dict(dict_report))

        if dict_report.get("report_type") == ReportTypes.WORD_CLOUD:
            return WordCloudReport(**dict(dict_report))

        return StatisticalReport(**dict(dict_report))

    def _build_mongo_filters(self, apply_filters: ReportsFetchSettings | None) -> dict[str, Any]:
        if apply_filters is None:
            return {}

        filters: dict[str, Any] = {}

        if apply_filters.name is not None:
            filters["name"] = {"$regex": f".*{apply_filters.name}.*", "$options": "i"}
        if apply_filters.date_from is not None:
            if "date" not in filters:
                filters["date"] = {}
            filters["date"]["$gte"] = apply_filters.date_from
        if apply_filters.date_to is not None:
            if "date" not in filters:
                filters["date"] = {}
            filters["date"]["$lte"] = apply_filters.date_to
        if apply_filters.processing_status is not None:
            filters["processing_status"] = apply_filters.processing_status
        if apply_filters.report_type is not None:
            filters["report_type"] = apply_filters.report_type

        return filters
