# pip install SQLAlchemy
# pip install psycopg2

import pandas as pd
import numpy as np
from sqlalchemy import create_engine, insert, update, delete
from sqlalchemy.engine import result
import RwModel

df1 = pd.read_excel("razb_uch.xlsx")
engine = create_engine("postgresql://speed5:secret@localhost:5432/speed5")
conn = engine.connect()

# Delete old

conn.execute(RwModel.uch_station.delete())
conn.execute(RwModel.station.delete())
conn.execute(RwModel.okato.delete())
conn.execute(RwModel.uch.delete())
conn.execute(RwModel.dor.delete())

# Dictionary: dor (id only)

sta_dor_begin_df = df1[["DOR_BEGIN_MELK_SET"]]
sta_dor_end_df = df1[["DOR_END_MELK_SET"]]
sta_dor_df = pd.DataFrame(np.concatenate((sta_dor_begin_df.values, sta_dor_end_df.values), axis=0))
sta_dor_df.columns = ["ID"]
sta_dor_df = sta_dor_df.drop_duplicates()
for index, row in sta_dor_df.iterrows():
    v_id = int(row["ID"])
    # print(v_id)
    stmt = RwModel.dor.insert().values(
        id = v_id
    )
    r = conn.execute(stmt)

# Dictionary: uch (id only)

uch_df = df1[["ID_UCH_VOST_POL"]]
uch_df.columns = ["ID"]
uch_df = uch_df.drop_duplicates()
for index, row in uch_df.iterrows():
    v_id = int(row["ID"])
    # print(v_id)
    stmt = RwModel.uch.insert().values(
        id = v_id
    )
    r = conn.execute(stmt)

# Dictionary: okato

sta_okato_begin_df = df1[["OKATO_BEGIN_MELK_SET_NAME"]]
sta_okato_end_df = df1[["OKATO_END_MELK_SET_NAME"]]
sta_okato_df = pd.DataFrame(np.concatenate((sta_okato_begin_df.values, sta_okato_end_df.values), axis=0))
sta_okato_df.columns = ["NAME"]
sta_okato_df = sta_okato_df.drop_duplicates()
okato_name_to_id = dict()
for index, row in sta_okato_df.iterrows():
    v_name = row["NAME"].strip()
    # print(v_name)
    stmt = RwModel.okato.insert().values(
        name = v_name
    )
    r = conn.execute(stmt)
    v_id = r.inserted_primary_key[0]
    # print(v_id)
    okato_name_to_id[v_name] = v_id

# Dictionary: stations (without coordinates)

sta_st_begin_df = df1[["ESR_BEGIN_MELK_SET", "NAME_BEGIN_MELK_SET", "DOR_BEGIN_MELK_SET", "OKATO_BEGIN_MELK_SET_NAME"]]
sta_st_end_df = df1[["ESR_END_MELK_SET", "NAME_END_MELK_SET", "DOR_END_MELK_SET", "OKATO_END_MELK_SET_NAME"]]
sta_st_df = pd.DataFrame(np.concatenate((sta_st_begin_df.values, sta_st_end_df.values), axis=0))
sta_st_df.columns = ["ESR", "NAME", "DOR_ID", "OKATO_NAME"]
sta_st_df = sta_st_df.drop_duplicates()
for index, row in sta_st_df.iterrows():
    v_esr = int(row["ESR"])
    v_name = row["NAME"].strip()
    v_dor_id = int(row["DOR_ID"])
    v_okato_name = row["OKATO_NAME"].strip()
    v_okato_id = okato_name_to_id[v_okato_name]
    # print(v_esr, v_name, v_dor_id, v_okato_name, v_okato_id)
    stmt = RwModel.station.insert().values(
        esr = v_esr,
        name = v_name,
        dor_id = v_dor_id,
        okato_id = v_okato_id
    )
    r = conn.execute(stmt)

# Dictionary: stations (populate coordinates)

uch_st_begin_df = df1[["NAME_BEGIN_VOST_UCH", "ESR_BEGIN_VOST_UCH", "X_BEG_VOST_UCH", "Y_BEG_VOST_UCH"]]
uch_st_end_df = df1[["NAME_END_VOST_UCH", "ESR_END_VOST_UCH", "X_END_VOST_UCH", "Y_END_VOST_UCH"]]
uch_st_df = pd.DataFrame(np.concatenate((uch_st_begin_df.values, uch_st_end_df.values), axis=0))
uch_st_df.columns = ["NAME", "ESR", "X", "Y"]
uch_st_df = uch_st_df.drop_duplicates()
for index, row in uch_st_df.iterrows():
    v_esr = int(row["ESR"])
    v_x = float(row["X"])
    v_y = float(row["Y"])
    # print(v_esr, v_x, v_y)
    stmt = RwModel.station.update().where(RwModel.station.c.esr == v_esr).values(
        x = v_x,
        y = v_y
    )
    r = conn.execute(stmt)

# Main data

df1.sort_values(["ID_UCH_VOST_POL", "NUM_CNSI_MELK_SET"], ascending=True, inplace=True)
last_uch_id = 0
last_num = 0
last_esr_end = 0
for index, row in df1.iterrows():
    v_uch_id = int(row["ID_UCH_VOST_POL"])
    if last_uch_id != 0 and v_uch_id != last_uch_id:
        # print("E", last_uch_id, last_num + 1, last_esr_end)
        stmt = RwModel.uch_station.insert().values(
            uch_id = last_uch_id,
            num = (last_num + 1),
            esr = last_esr_end
        )
        r = conn.execute(stmt)
    v_num = int(row["NUM_CNSI_MELK_SET"])
    v_esr_begin = int(row["ESR_BEGIN_MELK_SET"])
    v_esr_end = int(row["ESR_END_MELK_SET"])
    # print("B", v_uch_id, v_num, v_esr_begin)
    stmt = RwModel.uch_station.insert().values(
        uch_id = v_uch_id,
        num = v_num,
        esr = v_esr_begin
    )
    r = conn.execute(stmt)
    last_uch_id = v_uch_id
    last_num = v_num
    last_esr_end = v_esr_end
if last_uch_id != 0:
    # print("Z", last_uch_id, last_num + 1, last_esr_end)
    stmt = RwModel.uch_station.insert().values(
        uch_id = last_uch_id,
        num = (last_num + 1),
        esr = last_esr_end
    )
    r = conn.execute(stmt)

print("Done")
