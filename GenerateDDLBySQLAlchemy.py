# pip install SQLAlchemy

import string
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint, Index, create_mock_engine
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

metadata = MetaData()

Table("dor", metadata,
    Column("id", Integer, primary_key=True, autoincrement=False),
    CheckConstraint("id > 0", name="ck_dor_id")
)

Table("uch", metadata,
    Column("id", Integer, primary_key=True, autoincrement=False),
    CheckConstraint("id > 0", name="ck_uch_id")
)

Table("okato", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True, index=True)
)

Table("station", metadata,
    Column("esr", Integer, primary_key=True, autoincrement=False),
    Column("name", String, nullable=False),
    Column("x", DOUBLE_PRECISION, nullable=False),
    Column("y", DOUBLE_PRECISION, nullable=False),
    Column("dor_id", Integer, ForeignKey("dor.id"), nullable=False, index=True),
    Column("okato_id", Integer, ForeignKey("okato.id"), nullable=False, index=True),
    UniqueConstraint("x", "y", name="uq_station_x_y")
)

Table("uch_station", metadata,
    Column("uch_id", Integer, ForeignKey("uch.id"), nullable=False, index=True),
    Column("num", Integer, nullable=False, index=True),
    Column("esr", Integer, ForeignKey("station.esr"), nullable=False, index=True),
    CheckConstraint("num > 0", name="ck_uch_station_num"),
    UniqueConstraint("uch_id", "num", name="uq_uch_station_uch_id_num"),
    Index("ix_uch_station_uch_id_num", "uch_id", "num")
)

def dump(sql, *multiparams, **params):
    s = str(sql.compile(dialect=engine.dialect))
    s = s.strip()
    s += ";"
    print(s, file=ddl_file)
    print(file=ddl_file)

with open("PostgreSQL_DDL.txt", "w") as ddl_file:
    engine = create_mock_engine("postgresql://", dump)
    metadata.create_all(engine, checkfirst=False)
