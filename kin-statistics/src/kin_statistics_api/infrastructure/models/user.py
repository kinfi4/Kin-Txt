from sqlalchemy import Table, Column, String
from kin_txt_core.database import metadata


user_table = Table(
    "user",
    metadata,
    Column("username", String, primary_key=True),
    Column("password_hash", String, nullable=False),
)
