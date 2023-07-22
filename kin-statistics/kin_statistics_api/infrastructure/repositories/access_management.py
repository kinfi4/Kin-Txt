import logging

import sqlalchemy.sql.functions as func
from sqlalchemy import select, insert, update, delete
from kin_news_core.database import Database

from kin_statistics_api.infrastructure.models import user_report_table, user_generate_reports_table


class ReportsAccessManagementRepository:
    def __init__(self, db: Database):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    def get_user_report_ids(self, username: str) -> list[int]:
        select_query = (
            select(user_report_table)
            .where(user_report_table.c.username == username)
        )

        with self._db.connection() as conn:
            reports = conn.execute(select_query).mappings().all()

        return [report["report_id"] for report in reports]

    def create_new_user_report(self, username: str) -> int:
        """
            Returns: int - Report ID that was created
        """

        with self._db.connection() as conn:
            select_max_report_id = (
                select(func.max(user_report_table.c.report_id).label("max_report_id"))
            )
            row = conn.execute(select_max_report_id).mappings().one()
            max_report_id = row["max_report_id"] if row["max_report_id"] is not None else 0

            self._logger.info(f"Setting report access rights of report_id: {max_report_id + 1} to user: {username}")

            insert_new_report = (
                insert(user_report_table)
                .values(report_id=max_report_id + 1, username=username)
            )

            conn.execute(insert_new_report)

        return max_report_id + 1

    def set_user_began_report_generation(self, username: str) -> None:
        update_query = (
            update(user_generate_reports_table)
            .where(user_generate_reports_table.c.username == username)
            .values(reports_generated_count=user_generate_reports_table.c.reports_generated_count + 1)
        )

        with self._db.connection() as conn:
            conn.execute(update_query)

    def set_user_finished_report_generation(self, username: str) -> None:
        update_query = (
            update(user_generate_reports_table)
            .where(user_generate_reports_table.c.username == username)
            .values(reports_generated_count=user_generate_reports_table.c.reports_generated_count - 1)
        )

        with self._db.connection() as conn:
            conn.execute(update_query)

    def count_user_reports_synchronous_generations(self, username: str) -> int:
        select_query = (
            select(user_generate_reports_table.c.reports_generated_count)
            .where(user_generate_reports_table.c.username == username)
        )

        with self._db.connection() as conn:
            count_reports_generation = conn.execute(select_query).scalar()

            if count_reports_generation is None:
                insert_query = insert(user_generate_reports_table).values(username=username)
                conn.execute(insert_query)
                count_reports_generation = 0

        return count_reports_generation

    def delete_report(self, report_id: int) -> None:
        delete_query = (
            delete(user_report_table)
            .where(user_report_table.c.report_id == report_id)
        )

        with self._db.connection() as conn:
            conn.execute(delete_query)
