# pip install --upgrade pip
# pip install pandas
# pip install openpyxl

import pandas as pd 
import numpy as np

df1 = pd.read_excel("razb_uch.xlsx")

df1_info_file = open("AnalyseResult/df1_info.txt", "w+")
df1.info(buf=df1_info_file)
df1_info_file.close()

df1.describe().to_excel("AnalyseResult/df1_describe.xlsx")

with open("AnalyseResult/df1_unique.txt", "w") as df1_unique_file:
    for columnname in df1.columns.tolist():
        print(file=df1_unique_file);
        print(columnname + ":", file=df1_unique_file);
        print(df1[columnname].unique(), file=df1_unique_file)

# Uch begin

# Это неполный справочник станций, но содержит координаты указанных станций
uch_st_begin_df = df1[["NAME_BEGIN_VOST_UCH", "ESR_BEGIN_VOST_UCH", "X_BEG_VOST_UCH", "Y_BEG_VOST_UCH"]]
uch_st_begin_df = uch_st_begin_df.drop_duplicates()
assert uch_st_begin_df["NAME_BEGIN_VOST_UCH"].is_unique
assert uch_st_begin_df["ESR_BEGIN_VOST_UCH"].is_unique
assert uch_st_begin_df.set_index(["X_BEG_VOST_UCH", "Y_BEG_VOST_UCH"]).index.is_unique
uch_st_begin_df.to_excel("AnalyseResult/uch_st_begin_df.xlsx")

# Uch end

# Это неполный справочник станций, но содержит координаты указанных станций
uch_st_end_df = df1[["NAME_END_VOST_UCH", "ESR_END_VOST_UCH", "X_END_VOST_UCH", "Y_END_VOST_UCH"]]
uch_st_end_df = uch_st_end_df.drop_duplicates()
assert uch_st_end_df["NAME_END_VOST_UCH"].is_unique
assert uch_st_end_df["ESR_END_VOST_UCH"].is_unique
assert uch_st_end_df.set_index(["X_END_VOST_UCH", "Y_END_VOST_UCH"]).index.is_unique
uch_st_end_df.to_excel("AnalyseResult/uch_st_end_df.xlsx")

# Uch begin + end

# Справочник участков (содержит только идентификатор участка)
uch_df = df1[["ID_UCH_VOST_POL"]]
uch_df.columns = ["ID"]
uch_df = uch_df.drop_duplicates()
assert uch_df["ID"].is_unique
uch_df.to_excel("AnalyseResult/uch_df.xlsx")

# Это неполный справочник станций, но содержит координаты указанных станций
uch_st_df = pd.DataFrame(np.concatenate((uch_st_begin_df.values, uch_st_end_df.values), axis=0))
uch_st_df.columns = ["NAME", "ESR", "X", "Y"]
uch_st_df = uch_st_df.drop_duplicates()
uch_st_df.sort_values("ESR", ascending=True, inplace=True)
assert uch_st_df["NAME"].is_unique
assert uch_st_df["ESR"].is_unique
assert uch_st_df.set_index(["X", "Y"]).index.is_unique
uch_st_df.to_excel("AnalyseResult/uch_st_df.xlsx")

# Sta begin

# Часть справочника дорог
sta_dor_begin_df = df1[["DOR_BEGIN_MELK_SET"]]
sta_dor_begin_df = sta_dor_begin_df.drop_duplicates()
assert sta_dor_begin_df["DOR_BEGIN_MELK_SET"].is_unique
sta_dor_begin_df.to_excel("AnalyseResult/sta_dor_begin_df.xlsx")

# Часть справочника ОКАТО
sta_okato_begin_df = df1[["OKATO_BEGIN_MELK_SET_NAME"]]
sta_okato_begin_df = sta_okato_begin_df.drop_duplicates()
assert sta_okato_begin_df["OKATO_BEGIN_MELK_SET_NAME"].is_unique
sta_okato_begin_df.to_excel("AnalyseResult/sta_okato_begin_df.xlsx")

# Часть справочника станций без их координат
sta_st_begin_df = df1[["NAME_BEGIN_MELK_SET", "ESR_BEGIN_MELK_SET"]]
sta_st_begin_df = sta_st_begin_df.drop_duplicates()
sta_st_begin_df.sort_values("ESR_BEGIN_MELK_SET", ascending=True, inplace=True)
assert sta_st_begin_df["ESR_BEGIN_MELK_SET"].is_unique
sta_st_begin_df.to_excel("AnalyseResult/sta_st_begin_df.xlsx")

# Sta end

# Часть справочника дорог
sta_dor_end_df = df1[["DOR_END_MELK_SET"]]
sta_dor_end_df = sta_dor_end_df.drop_duplicates()
assert sta_dor_end_df["DOR_END_MELK_SET"].is_unique
sta_dor_end_df.to_excel("AnalyseResult/sta_dor_end_df.xlsx")

# Часть справочника ОКАТО
sta_okato_end_df = df1[["OKATO_END_MELK_SET_NAME"]]
sta_okato_end_df = sta_okato_end_df.drop_duplicates()
assert sta_okato_end_df["OKATO_END_MELK_SET_NAME"].is_unique
sta_okato_end_df.to_excel("AnalyseResult/sta_okato_end_df.xlsx")

# Часть справочника станций без их координат
sta_st_end_df = df1[["NAME_END_MELK_SET", "ESR_END_MELK_SET"]]
sta_st_end_df = sta_st_end_df.drop_duplicates()
sta_st_end_df.sort_values("ESR_END_MELK_SET", ascending=True, inplace=True)
assert sta_st_end_df["ESR_END_MELK_SET"].is_unique
sta_st_end_df.to_excel("AnalyseResult/sta_st_end_df.xlsx")

# Sta begin + end

# Полный справочник дорог
sta_dor_df = pd.DataFrame(np.concatenate((sta_dor_begin_df.values, sta_dor_end_df.values), axis=0))
sta_dor_df.columns = ["DOR_ID"]
sta_dor_df = sta_dor_df.drop_duplicates()
sta_dor_df.sort_values("DOR_ID", ascending=True, inplace=True)
assert sta_dor_df["DOR_ID"].is_unique
sta_dor_df.to_excel("AnalyseResult/sta_dor_df.xlsx")

# Полный справочник ОКАТО
# При импорте в БД дополнительно нужно будет автоматически генерировать суррогатный Primary Key
sta_okato_df = pd.DataFrame(np.concatenate((sta_okato_begin_df.values, sta_okato_end_df.values), axis=0))
sta_okato_df.columns = ["OKATO_NAME"]
sta_okato_df = sta_okato_df.drop_duplicates()
sta_okato_df.sort_values("OKATO_NAME", ascending=True, inplace=True)
assert sta_okato_df["OKATO_NAME"].is_unique
sta_okato_df.to_excel("AnalyseResult/sta_okato_df.xlsx")

# Полный справочник станций без их координат
# После импорта этого справочника в БД нужно дополнительно для некоторых станций импортировать их координаты из справочника uch_st_df
sta_st_df = pd.DataFrame(np.concatenate((sta_st_begin_df.values, sta_st_end_df.values), axis=0))
sta_st_df.columns = ["NAME", "ESR"]
sta_st_df = sta_st_df.drop_duplicates()
sta_st_df.sort_values("ESR", ascending=True, inplace=True)
assert sta_st_df["ESR"].is_unique
sta_st_df.to_excel("AnalyseResult/sta_st_df.xlsx")

# Остальные поля:
# NUM_CNSI_MELK_SET - порядковый номер станции в заданном участке, 1..N
