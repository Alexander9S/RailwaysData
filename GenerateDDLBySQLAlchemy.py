# pip install SQLAlchemy

from sqlalchemy import create_mock_engine
import RwModel

def dump(sql, *multiparams, **params):
    s = str(sql.compile(dialect=engine.dialect))
    s = s.strip()
    s += ";"
    print(s, file=ddl_file)
    print(file=ddl_file)

with open("PostgreSQL_DDL.txt", "w") as ddl_file:
    engine = create_mock_engine("postgresql://", dump)
    RwModel.metadata.create_all(engine, checkfirst=False)
