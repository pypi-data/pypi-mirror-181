import sqlite3
import json
from dataclasses import dataclass
from pathlib import Path
from qualys_etl.etld_lib import etld_lib_sqlite_tables
from qualys_etl.etld_lib import etld_lib_functions
from qualys_etl.etld_lib import etld_lib_config
from qualys_etl.etld_lib import etld_lib_spawn_etl


@dataclass
class EtlWorkflowValidation():
    log_file_path: Path
    sqlite_file_path: Path
    sqlite_obj: object
    type: str
    status_table_name: str
    status_table_rows: sqlite3.Row
    etl_workflow_option: str
    etl_workflow_log_list: list
    etl_workflow_log_errors_found: bool

    def __init__(self, etl_workflow_option, type='validation'):
        self.etl_workflow_log_errors_found = False
        self.etl_workflow_option = etl_workflow_option
        self.sqlite_file_path, self.log_file_path = self.get_workflow_database_log_files(etl_workflow_option)
        self.set_type(type)
        try:
            if self.sqlite_file_path.is_file():
               self.sqlite_obj = etld_lib_sqlite_tables.SqliteObj(str(self.sqlite_file_path))
               self.status_table_name = self.get_database_status_table_name(self.sqlite_obj, sqlite_file_name=self.sqlite_file_path)
               self.status_table_rows = self.get_database_status_table_rows(self.sqlite_obj, self.status_table_name, self.sqlite_file_path)

               self.log_workflow_date, \
               self.log_workflow_name, \
               self.log_file_name = \
                   self.get_log_workflow_info(self.status_table_rows)

               self.disregard_sqlite_file, \
               self.log_file_path = \
                   self.get_workflow_database_log_files(etl_workflow_option=self.log_workflow_name)
               self.etl_workflow_log_list = self.get_workflow_log(self.log_file_path, self.log_workflow_date)
               if self.test_etl_workflow_log_errors(self.etl_workflow_log_list):
                   self.log_etl_workflow_log_errors(self.etl_workflow_log_list)
                   self.etl_workflow_log_errors_found = True
            else:
                self.sqlite_obj = None
                self.status_table_name = ""
                self.status_table_rows = None
        except Exception as e:
            etld_lib_functions.logger.error(f"Exception {e}")
            exit(1)

    def get_sqlite_obj(self, sqlite_file) -> etld_lib_sqlite_tables.SqliteObj:
        sqlite_obj = None
        if sqlite_file.is_file():
            sqlite_obj = etld_lib_sqlite_tables.SqliteObj(str(self.sqlite_file_path))
        return sqlite_obj

    def set_type(self, type="validation"):
        self.type = type

    def get_workflow_database_log_files(self, etl_workflow_option: str):
        if etl_workflow_option == 'validate_etl_knowledgebase' or etl_workflow_option == 'knowledgebase_etl_workflow':
            sqlite_file = etld_lib_config.kb_sqlite_file
            log_file = etld_lib_config.kb_log_file
        elif etl_workflow_option == 'validate_etl_host_list' or etl_workflow_option == 'host_list_etl_workflow':
            sqlite_file = etld_lib_config.host_list_sqlite_file
            log_file = etld_lib_config.host_list_log_file
        elif etl_workflow_option == 'validate_etl_host_list_detection' or etl_workflow_option == 'host_list_detection_etl_workflow':
            sqlite_file = etld_lib_config.host_list_detection_sqlite_file
            log_file = etld_lib_config.host_list_detection_log_file
        elif etl_workflow_option == 'validate_etl_asset_inventory' or etl_workflow_option == 'asset_inventory_etl_workflow':
            sqlite_file = etld_lib_config.asset_inventory_sqlite_file
            log_file = etld_lib_config.asset_inventory_log_file
        elif etl_workflow_option == 'validate_etl_was' or etl_workflow_option == 'was_etl_workflow':
            sqlite_file = etld_lib_config.was_sqlite_file
            log_file = etld_lib_config.was_log_file
        else:
            raise Exception(f"Invalid option {etl_workflow_option}, please review options and rerun")

        return sqlite_file, log_file

    def get_database_status_table_name(self, sqlite_obj, sqlite_file_name, schema_name='sqlite_master') -> str:
        select_status_table_name = f"SELECT name FROM {schema_name} WHERE type ='table' AND name LIKE '%_status'"
        status_table_row = sqlite_obj.select_from_table(select_statement=select_status_table_name)
        if len(status_table_row) == 0:
            raise Exception(f"status tables missing from Database.  Rerun when database is ready. {sqlite_file_name}")
        status_table_name = status_table_row[0]['name']
        return status_table_name

    def get_database_status_table_rows(self, sqlite_obj, status_table_name, sqlite_file_name) -> sqlite3.Row:
        select_all_status_rows = f"SELECT * FROM {status_table_name}"
        all_status_rows = sqlite_obj.select_from_table(select_statement=select_all_status_rows)
        if len(all_status_rows) == 0:
            raise Exception(
                f"Could not find status rows in table {status_table_name}.  Rerun when database is ready. {sqlite_file_name}")
        return all_status_rows

    def get_log_workflow_info(self, status_table_rows: sqlite3.Row):
        log_workflow_date = ""
        log_workflow_name = ""
        log_file_name = ""
        try:
            row = status_table_rows[-1] # Get Last Row
            status_name = row['status_name']
            status_detail_dict = json.loads(row['status_detail'])
            status = status_detail_dict['STATUS']
            log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
            log_workflow_name = status_detail_dict['LOG_WORKFLOW_NAME']
            disregard_sqlite_file, log_file_name = \
                self.get_workflow_database_log_files(etl_workflow_option=log_workflow_name)
        except Exception as e:
            log_workflow_name = ""
            log_workflow_date = ""
            log_file_name = ""

        return log_workflow_date, log_workflow_name, log_file_name

    def get_workflow_log(self, log_file, log_workflow_date):

        log_list = []
        log_file_path = log_file
        log_workflow_date = log_workflow_date
        # Validate logs have no errors
        first_log_entry = []
        found_workflow_log_flag = False
        number_of_runlog_columns = len(etld_lib_config.run_log_csv_columns())

        try:
            with open(str(log_file_path), "rt", encoding='utf-8') as read_file:
                for log_line in read_file:
                    log_entry = log_line.split('|')
                    if found_workflow_log_flag:
                        pass
                    elif len(log_entry) == number_of_runlog_columns and log_workflow_date in log_entry[2]:
                        found_workflow_log_flag = True
                        first_log_entry = log_entry
                    else:
                        continue

                    log_entry_dict = {}
                    if len(log_entry) == number_of_runlog_columns and log_entry[0].startswith("20"):
                        # Normal Log
                        for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                            column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                            log_entry_dict[f'{column_name}'] = str(log_entry[csv_index]).strip()
                        if log_entry_dict['LOG_LEVEL'] == 'ERROR':
                            found_workflow_log_errors_flag = True
                    else:
                        # Error Log outside of logging. E.g. Kill Processes
                        last_log_list_entry_processed = log_list[-1]
                        for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                            column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                            log_entry_dict[f'{column_name}'] = str(last_log_list_entry_processed[column_name]).strip()
                        # for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                        #     column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                        #     log_entry_dict[f'{column_name}'] = str(first_log_entry[csv_index]).strip()
                        log_entry_string = "".join(log_entry).strip()
                        log_entry_dict['LOG_MESSAGE'] = f"UNBOUND LOG ERROR: {log_entry_string}"
                        log_entry_dict['LOG_LEVEL'] = "ERROR"
                        log_entry_dict['LOG_FUNCTION'] = "etld_lib_log_validation"
                    log_list.append(log_entry_dict)

        except Exception as e:
            etld_lib_functions.logger.error(f"exception {e}")
            exit(1)

        return log_list

    def test_etl_workflow_log_errors(self, etl_workflow_log_list):
        found_workflow_log_errors_flag = False
        for log_entry in etl_workflow_log_list:
            if 'LOG_LEVEL' in log_entry:
                if log_entry['LOG_LEVEL'] == 'ERROR':
                    found_workflow_log_errors_flag = True
                    break

        return found_workflow_log_errors_flag

    def log_etl_workflow_log_errors(self, etl_workflow_log_list):
        for log_entry in etl_workflow_log_list:
            if 'LOG_LEVEL' in log_entry:
                if log_entry['LOG_LEVEL'] == 'ERROR':
                    log_entry_dict = {}
                    for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                        column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                        log_entry_dict[f'{column_name}'] = str(log_entry[column_name]).strip()
                    etld_lib_functions.logger.error(f"ERRORS FOUND - "
                                                    f"LOG_WORKFLOW: {log_entry_dict['LOG_WORKFLOW']}, "
                                                    f"LOG_USERNAME: {log_entry_dict['LOG_USERNAME']}, "
                                                    f"LOG_FUNCTION: {log_entry_dict['LOG_FUNCTION']}, "
                                                    f"LOG_MESSAGE: {log_entry_dict['LOG_MESSAGE']}"
                                                    f"")


def main():
    etl_obj_list = []
    final_exit_status = 0
    for etl_workflow in etld_lib_spawn_etl.etl_workflow_list:
        etl_obj = EtlWorkflowValidation(etl_workflow_option=etl_workflow)
        if etl_obj.sqlite_obj is None:
            etld_lib_functions.logger.warning(f"etl_workflow_option{etl_workflow} database {etl_obj.sqlite_file_path} not found")
        else:
            etl_obj_list.append(etl_obj)
            for row in etl_obj.status_table_rows:
                status_name = row['status_name']
                status_detail_dict = json.loads(row['status_detail'])
                status = status_detail_dict['STATUS']
                log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
                log_workflow_name = status_detail_dict['LOG_WORKFLOW_NAME']
                if etl_obj.etl_workflow_log_errors_found:
                   etl_workflow_log_message = "log file has errors, do not process data."
                   final_exit_status = 2
                   etld_lib_functions.logger.error(f""
                                               f"etl run results: {etl_workflow_log_message}, "
                                               f"status_table_name: {etl_obj.status_table_name}, "
                                               f"workflow_that_updated_table: {log_workflow_name}, "
                                               f"log_workflow_date: {log_workflow_date}, "
                                               f"status_name: {status_name}, "
                                               f"status: {status} "
                                               )
                else:
                   etl_workflow_log_message = "true, successful run"

                   etld_lib_functions.logger.info(f""
                                               f"etl run results: {etl_workflow_log_message}, "
                                               f"status_table_name: {etl_obj.status_table_name}, "
                                               f"workflow_that_updated_table: {log_workflow_name}, "
                                               f"log_workflow_date: {log_workflow_date}, "
                                               f"status_name: {status_name}, "
                                               f"status: {status} "
                                               )
    exit(final_exit_status)

if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='validate_latest_etl_workflows')
    etld_lib_config.main()
    main()


