1. Установите зависимости:

pip install pandas
pip install openpyxl
pip install SQLAlchemy
pip install psycopg2


2. (опционально) Выполните анализ:

AnalyseByPandas.bat


3. Выполните генерацию DDL:

GenerateDDLBySQLAlchemy.bat

На выходе получится файл PostgreSQL_DDL.txt.
Он уже представлен в этом репозитории.


4. Создайте вручную схему БД с помощью только что полученного или уже представленного в репозитории файла PostgreSQL_DDL.txt


5. Измените параметры подключения к экземпляру СУБД в файле UploadDataBySQLAlchemy.py в инструкции create_engine.


6. Выполните загрузку данных из файла Excel в СУБД:

UploadDataBySQLAlchemy.bat
