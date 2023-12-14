from sqlalchemy import Table, Column, String, Integer
from kin_txt_core.database import metadata


user_generate_reports_table = Table(
    "user_generate_reports",
    metadata,
    Column("username", String),
    Column("reports_generated_count", Integer, default=0),
)
