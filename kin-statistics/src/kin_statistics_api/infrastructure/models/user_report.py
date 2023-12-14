from sqlalchemy import Table, Column, String, Integer
from kin_txt_core.database import metadata


user_report_table = Table(
    "user_report",
    metadata,
    Column("username", String),
    Column("report_id", Integer),
)
