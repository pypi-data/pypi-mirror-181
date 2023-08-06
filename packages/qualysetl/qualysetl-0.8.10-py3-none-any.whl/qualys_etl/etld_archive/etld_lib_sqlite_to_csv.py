import os
import oschmod
import sqlite3
import csv
import re
from pathlib import Path
from qualys_etl.etld_lib import etld_lib_functions
from qualys_etl.etld_lib import etld_lib_config
from qualys_etl.etld_lib import etld_lib_extract_transform_load

class SqliteTabletoCsvFile():

    def __init__(self,
                 source_database_path,
                 source_sql_select_statement,
                 source_sql_table_name,
                 target_csv_path,
                 target_csv_data_directory
                 ):
        self.source_database_path = source_database_path
        self.target_csv_path = target_csv_path
        self.source_sql_select_statement = source_sql_select_statement
        self.source_sql_table_name  = source_sql_table_name
        self.target_csv_data_directory = target_csv_data_directory
        if not source_database_path.exists():
            raise Exception(f"Database Path does not exist - {str(source_database_path)}, rerun when ready.")
        if not target_csv_data_directory.is_dir():
            self.create_directory(target_csv_data_directory)

    def create_directory(self, dir_path=None):
        try:
            if dir_path is not None:
                os.makedirs(dir_path, exist_ok=True)
                oschmod.set_mode(dir_path, "a+rwx,g-rwx,o-rwx")
        except Exception as e:
            raise Exception(f"Could not create directory {dir_path}")

    def get_database_connection(self, database):
        connect = None
        try:
            connect = sqlite3.connect(database)
        except sqlite3.DatabaseError as e:
            raise Exception(f"Database connection unsuccessful to - {database}")
        return connect

    def get_pragma(self, connect, table_name):
        sqlPragma = f'PRAGMA table_info({table_name})'
        try:
            cursor = connect.cursor()
            cursor.execute(sqlPragma)
            result = cursor.fetchall()
            cursor.close()
        except sqlite3.DatabaseError as e:
            raise Exception(f"Exception: {e} - Could not obtain pragma for table: {table_name}.")
        return result

    def prepare_headers_from_sqlite(self, cursor):
        headers = [i[0] for i in cursor.description]
        return headers

    def get_csv_writer(self, csv_file, csv_open_method=open):
        csv_writer = csv.writer(csv_open_method(csv_file, 'w', newline=''),
                             delimiter=',', lineterminator='\n',
                             quoting=csv.QUOTE_NONE, escapechar='\\')
        return csv_writer

    def prepare_csv_row(self, headers, result, pragma, max_size) -> list:
        row_fields = []
        for idx, fieldname in enumerate(headers):
            field_data = result[idx]
            if pragma[idx][2] == 'INTEGER':
                field_data = str(result[idx]).strip()
                if not str(result[idx]).isnumeric():
                    field_data = '0'
            else:
                if str(field_data).__contains__('\,'):
                    field_data = re.sub('\\\,', '\;', field_data)
            row_fields.append(f"{str(field_data)[0:int(max_size)]}")
        return row_fields

    def create_csv_from_sqlite_select_statement(self, connect, csv_file, sqlSelect, pragma, max_size=10000000000):
        try:
            cursor = connect.cursor()
            cursor.execute(sqlSelect)

            headers = self.prepare_headers_from_sqlite(cursor)
            csvFile = self.get_csv_writer(csv_file)
            csvFile.writerow(headers)

            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                row_fields = self.prepare_csv_row(headers, result, pragma, max_size)
                csvFile.writerow(row_fields)
        except sqlite3.DatabaseError as e:
            raise Exception(f"Exception: {e} - sqlite3.DatabaseError - data export unsuccessful.")
        except Exception as e:
            raise Exception(f"Exception {e} - Other file error, data export unsuccessful.")
        finally:
            connect.close()

    def main(self):
        try:
            with sqlite3.connect(str(self.source_database_path)) as connect_db:
                sql_table_pragma = self.get_pragma(connect_db, self.source_sql_table_name)
                self.create_csv_from_sqlite_select_statement(
                    connect=connect_db,
                    csv_file=str(self.target_csv_path),
                    sqlSelect=self.source_sql_select_statement, pragma=sql_table_pragma)
        except sqlite3.DatabaseError as e:
            raise Exception(f"Exception: {e} - sqlite3.DatabaseError - data export unsuccessful.")
        except Exception as e:
            print(f'Exception {e}, aborted')
            exit(1)
        finally:
            connect_db.close()


if __name__ == "__main__":

    #
    # batch_number_str = "batch_000001"
    # batch_date = etld_lib_extract_transform_load.get_batch_date_from_filename(xml_file)
    # file_info_dict = \
    #     etld_lib_config.prepare_extract_batch_file_name(
    #         next_batch_number_str=batch_number_str,
    #         next_batch_date=batch_date,
    #         extract_dir=etld_lib_config.host_list_extract_dir,
    #         file_name_type="host_list",
    #         file_name_option="vm_processed_after",
    #         file_name_option_date=etld_lib_config.host_list_vm_processed_after,
    #         compression_method=etld_lib_config.host_list_open_file_compression_method
    #     )

    # sql_table_name = "Q_Host_List_Detection_QIDS"
    # csv_output_file_name = "q_host_list_detection_qids.csv"
    # database_input_file_name = "host_list_detection_sqlite.db"

    sql_table_name = "Q_KnowledgeBase"
    csv_output_file_name = "kb.csv"
    database_input_file_name = "kb_sqlite.db"
    home_directory = Path('/opt/qetl/users/tamab_dt4/qetl_home/')
    data_directory = Path('/opt/qetl/users/tamab_dt4/qetl_home/data')
    data_archive_directory = Path('/opt/qetl/users/tamab_dt4/qetl_home/data_archive')
    if not home_directory.is_dir():
        raise Exception(f"Home Directory Path Not Found, {str(home_directory)} - Please rerun when ready")

    sql_select_statement = f"SELECT * FROM {sql_table_name}"
    csv_path = Path(data_archive_directory, csv_output_file_name)
    database_path = Path(data_directory, database_input_file_name)
    sqlite_to_csv_file_obj = SqliteTabletoCsvFile(
        source_database_path=database_path,
        target_csv_path=csv_path,
        source_sql_select_statement=sql_select_statement,
        target_csv_data_directory=data_archive_directory,
        source_sql_table_name=sql_table_name
    )
