from sqlalchemy import (
    Column,
    MetaData,
    Integer,
    DateTime,
    String,
    Table,
)

metadata = MetaData()
Profile = Table(
    "dt_credentials", metadata,
        Column('id_credential', Integer, nullable=False),
        Column('id_user', Integer, nullable=False),
        Column('profile_name', String(255)),
        Column('access_id', String(255)),
        Column('secret_access', String(255)),
        Column('date_created', DateTime),
)

