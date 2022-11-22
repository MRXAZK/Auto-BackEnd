from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()
User = Table(
    "dt_user", metadata,
    Column('username', String(255), nullable=False),
    Column('full_name', String(255)),
    Column('email', String(255)),
    Column('hashed_password', String(255)),
    Column('disabled', String(255))
)