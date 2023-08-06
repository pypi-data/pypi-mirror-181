#!/usr/bin/env python3
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass

from qualys_etl.etld_lib import etld_lib_config
from qualys_etl.etld_lib import etld_lib_functions
from qualys_etl.etld_lib import etld_lib_sqlite_tables


def get_etl_validation_option_settings(etl_option: str) -> dict:
    if etl_option == 'validate_etl_knowledgebase' or etl_option == 'knowledgebase_etl_workflow':
        sqlite_file = etld_lib_config.kb_sqlite_file
        log_file = etld_lib_config.kb_log_file
    elif etl_option == 'validate_etl_host_list' or etl_option == 'host_list_etl_workflow':
        sqlite_file = etld_lib_config.host_list_sqlite_file
        log_file = etld_lib_config.host_list_log_file
    elif etl_option == 'validate_etl_host_list_detection' or etl_option == 'host_list_detection_etl_workflow':
        sqlite_file = etld_lib_config.host_list_detection_sqlite_file
        log_file = etld_lib_config.host_list_detection_log_file
    elif etl_option == 'validate_etl_asset_inventory' or etl_option == 'asset_inventory_etl_workflow':
        sqlite_file = etld_lib_config.asset_inventory_sqlite_file
        log_file = etld_lib_config.asset_inventory_log_file
    elif etl_option == 'validate_etl_was' or etl_option == 'was_etl_workflow':
        sqlite_file = etld_lib_config.was_sqlite_file
        log_file = etld_lib_config.was_log_file
    else:
        raise Exception(f"Invalid option {etl_option}, please review options and rerun")

    return {'etl_workflow_sqlite_file_path': sqlite_file, 'etl_workflow_log_file_path': log_file, 'etl_workflow_validation_type': 'validate', 'etl_validation_option': etl_option}

def get_status_table_name(sqlite_obj, sqlite_file_name) -> str:
    # Get Status Table
    schema_name = 'sqlite_master'
    select_status_table_name = f"SELECT name FROM {schema_name} WHERE etl_workflow_validation_type ='table' AND name LIKE '%_status'"
    status_table_row = sqlite_obj.select_from_table(select_statement=select_status_table_name)
    if len(status_table_row) == 0:
        raise Exception(f"status tables missing from Database.  Rerun when database is ready. {sqlite_file_name}")
    status_table_name = status_table_row[0]['name']

    return status_table_name

def get_status_table_results(sqlite_obj, status_table_name, sqlite_file_name):
    select_status_of_last_run = f"SELECT * FROM {status_table_name} WHERE status_name == 'ALL_TABLES_LOADED_SUCCESSFULLY'"
    all_tables_loaded_successfully_status_row = sqlite_obj.select_from_table(select_statement=select_status_of_last_run)
    select_all_status_rows = f"SELECT * FROM {status_table_name}"
    all_status_rows = sqlite_obj.select_from_table(select_statement=select_all_status_rows)
    if len(all_status_rows) == 0:
        raise Exception(f"Could not find status rows in table {status_table_name}.  Rerun when database is ready. {sqlite_file_name}")

    return all_tables_loaded_successfully_status_row, all_status_rows


def get_status_table_rows(sqlite_obj, status_table_name) -> sqlite3.Row:
    select_rows = f"SELECT * FROM {status_table_name}"
    rows = sqlite_obj.select_from_table(select_statement=select_rows)
    return rows

def get_rows_from_keys(row: sqlite3.Row, keys: list) -> dict:
    row_dict = {}
    for key in keys:
        if key in row.keys():
            row_dict[key] = row[key]
        else:
            row_dict[key] = ""
    return row_dict


def get_database_status(etl_option_dict: dict):
    sqlite_file_name = str(etl_option_dict['etl_workflow_sqlite_file_path'])
    sqlite_obj = etld_lib_sqlite_tables.SqliteObj(sqlite_file=sqlite_file_name)
    status_table_name = get_status_table_name(sqlite_obj, sqlite_file_name)
    all_tables_loaded_successfully_status_row, all_status_rows  = \
        get_status_table_results(sqlite_obj, status_table_name, sqlite_file_name)
    if len(all_tables_loaded_successfully_status_row) == 1:
        all_tables_loaded_successfully_dict = \
            get_rows_from_keys(all_tables_loaded_successfully_status_row[0], etld_lib_config.status_table_csv_columns())
        all_tables_loaded_successfully_status_detail_dict = json.loads(all_tables_loaded_successfully_dict['STATUS_DETAIL'])
        all_tables_loaded_successfully_dict['LAST_BATCH_PROCESSED'] =  all_tables_loaded_successfully_status_row[0]['LAST_BATCH_PROCESSED']


def get_status_table_rows_list(etl_option_settings_obj):

    all_tables_loaded_successfully_flag = False
    status_table_rows_list = []
    status_detail_dict = {}

    try:
        sqlite_obj = etld_lib_sqlite_tables.SqliteObj(sqlite_file=str(etl_option_settings_obj.etl_workflow_sqlite_file_path))

        # GET STATUS TABLE NAME FROM SQLITE SCHEMA
        status_table_name = get_status_table_name(sqlite_obj, sqlite_file_name)

        # GET STATUS TABLE ROWS
        status_table_rows = get_status_table_rows(sqlite_obj=sqlite_obj, status_table_name=status_table_name)

        # GET WORKFLOW FROM FIRST ROW
        status_name = ""
        status_detail = ""
        log_location_dict = {}
        if len(status_table_rows) > 0:
            status_name = status_table_rows[0]['STATUS_NAME']
            status_detail = status_table_rows[0]['STATUS_DETAIL']
            status_detail_dict = json.loads(status_detail)
            log_location_dict = get_etl_validation_option_settings(status_detail_dict['LOG_WORKFLOW_NAME'])
            log_file_path = log_location_dict['etl_workflow_log_file_path']
            log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
        else:
            etld_lib_functions.logger.error(f"No entries in table: {status_table_name} to analyze")
            etld_lib_functions.logger.error(f"Database in unknown state.  Please review database: {sqlite_file_name}")
            exit(1)

        # GET ALL_TABLES_LOADED_SUCCESSFULLY STATUS
        all_tables_loaded_successfully_status_row = None
        all_tables_loaded_successfully_dict = {}
        status_table_rows_list = []
        for status_table_row in status_table_rows:
            status_table_rows_list.append(status_table_row)
            if 'STATUS_NAME' in status_table_row.keys():
                if 'ALL_TABLES_LOADED_SUCCESSFULLY' in status_table_row['STATUS_NAME']:
                    all_tables_loaded_successfully_status_row = status_table_row
                    all_tables_loaded_successfully_dict = \
                        get_rows_from_keys(status_table_row, etld_lib_config.status_table_csv_columns())
                    all_tables_loaded_successfully_status_detail_dict = \
                        json.loads(all_tables_loaded_successfully_dict['STATUS_DETAIL'])
                    all_tables_loaded_successfully_flag = True

        sqlite_obj.close_connection()
    except Exception as e:
        etld_lib_functions.logger.error(f"exception {e}")
        exit(1)

    return all_tables_loaded_successfully_flag, status_table_rows_list, status_detail_dict


def get_etl_option_workflow_log(etl_option_dict: dict):

    log_list = []
    all_tables_loaded_successfully_flag = False
    log_file_path = etl_option_dict['etl_workflow_log_file_path']
    log_workflow_date = etl_option_dict['log_workflow_date']

    try:
        # Validate logs have no errors
        first_log_entry = []
        found_workflow_log_flag = False
        found_workflow_log_errors_flag = False
        log_list = []
        number_of_runlog_columns = len(etld_lib_config.run_log_csv_columns())

        with open(str(log_file_path), "rt", encoding='utf-8') as read_file:
            for log_line in read_file:
                log_entry = log_line.split('|')

                if found_workflow_log_flag:
                    pass
                elif len(log_entry) == number_of_runlog_columns:
                    if log_workflow_date in log_entry[2]:
                        found_workflow_log_flag = True
                        first_log_entry = log_entry
                else:
                    continue

                log_entry_dict = {}
                if len(log_entry) == number_of_runlog_columns:
                    # Normal Log
                    for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                        column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                        log_entry_dict[f'{column_name}'] =  str(log_entry[csv_index]).strip()
                    if log_entry_dict['LOG_LEVEL'] == 'ERROR':
                        found_workflow_log_errors_flag = True
                else:
                    # Error Log outside of logging. E.g. Kill Processes
                    for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
                        column_name = etld_lib_config.run_log_csv_columns()[csv_index]
                        log_entry_dict[f'{column_name}'] =  str(first_log_entry[csv_index]).strip()
                    log_entry_string = "".join(log_entry).strip()
                    log_entry_dict['LOG_MESSAGE'] = f"UNBOUND LOG ERROR: {log_entry_string}"
                    log_entry_dict['LOG_LEVEL'] = "ERROR"
                    log_entry_dict['LOG_FUNCTION'] = "main_validate_log_has_no_errors"
                    found_workflow_log_errors_flag = True
                log_list.append(log_entry_dict)

    except Exception as e:
        etld_lib_functions.logger.error(f"exception {e}")
        exit(1)

    return log_list, all_tables_loaded_successfully_flag


def update_status_table_with_log_data():
    pass


def validate_no_errors_found_in_workflow_logs(log_list):
    valid_workflow_flag = True
    for log_entry in log_list:
        if log_entry['LOG_LEVEL'] == 'ERROR':
            etld_lib_functions.logger.error(f"workflow: {log_entry['LOG_WORKFLOW']} - MESSAGE - {log_entry['LOG_MESSAGE']}")
            valid_workflow_flag = False

    return valid_workflow_flag


def validate_display_final_counter_message_found_in_workflow_logs(log_list):
    display_final_counter_message_found_in_workflow_logs_flag = False
    for log_item in log_list:
        if 'display_final_counter' in log_item['LOG_FUNCTION']:
            display_final_counter_message_found_in_workflow_logs_flag = True

    return display_final_counter_message_found_in_workflow_logs_flag


def validate_spawned_process_ended_message_found_in_workflow_logs(log_list):
    validate_spawned_process_ended_message_found_in_workflow_logs_flag = False
    if 'spawned_process_ended' in log_list[-1]['LOG_FUNCTION']:
        validate_spawned_process_ended_message_found_in_workflow_logs_flag = True
    return validate_spawned_process_ended_message_found_in_workflow_logs_flag

@dataclass
class EtlWorkflowConfiguration():
    def __init__(self):
        self.etl_validation_option: str
        self.log_file: Path
        self.sqlite_file: Path
        self.sqlite_obj: object
        self.type: str

    def __pos__(self):
        self.sqlite_obj = etld_lib_sqlite_tables.SqliteObj(str(self.sqlite_file))




def main(etl_validation_option):
    etl_option_settings_dict = get_etl_validation_option_settings(etl_validation_option)
    etl_option_settings_obj = EtlWorkflowConfiguration()
    etl_option_settings_obj.etl_validation_option = etl_option_settings_dict['etl_validation_option']
    etl_option_settings_obj.log_file = etl_option_settings_dict['etl_workflow_log_file_path']
    etl_option_settings_obj.sqlite_file = etl_option_settings_dict['etl_workflow_sqlite_file_path']
    etl_option_settings_obj.type = etl_option_settings_dict['etl_workflow_validation_type']
    etl_option_settings_obj.sqlite_obj = etld_lib_sqlite_tables.SqliteObj(sqlite_file=str(etl_option_settings_obj.sqlite_file))

    all_tests_for_validation_passed_flag = False
    validate_spawned_process_ended_message_found_in_workflow_logs_flag = False
    validate_display_final_counter_message_found_in_workflow_logs_flag = False
    validate_no_errors_found_in_workflow_logs_flag = False
    all_tables_updated_successfully_row_found_in_status_table_flag = False
    status_table_rows_list = []

    if etl_option_settings_obj.type == 'validate':

        all_tables_updated_successfully_row_found_in_status_table_flag, status_table_rows_list, status_detail_dict =  \
            get_status_table_rows_list(etl_option_settings_obj)

        log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
        etl_option_settings_obj.log_workflow_date = log_workflow_date

        log_list, all_tables_updated_successfully_row_found_in_status_table_flag = \
            get_etl_option_workflow_log(etl_option_settings_dict)


        validate_spawned_process_ended_message_found_in_workflow_logs_flag = \
            validate_spawned_process_ended_message_found_in_workflow_logs(log_list)

        validate_display_final_counter_message_found_in_workflow_logs_flag = \
            validate_display_final_counter_message_found_in_workflow_logs(log_list)

        validate_no_errors_found_in_workflow_logs_flag = \
            validate_no_errors_found_in_workflow_logs(log_list)

        if validate_no_errors_found_in_workflow_logs_flag and \
                validate_spawned_process_ended_message_found_in_workflow_logs_flag and \
                validate_display_final_counter_message_found_in_workflow_logs_flag and \
                all_tables_updated_successfully_row_found_in_status_table_flag:
            etld_lib_functions.logger.info(f"successful run log "
                                           f"for {etl_option_settings_dict}, workflow {log_workflow_date}")
            all_tests_for_validation_passed_flag = True
        else:
            if validate_no_errors_found_in_workflow_logs_flag:
                etld_lib_functions.logger.info(f"logfile success - found no errors "
                                               f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            else:
                etld_lib_functions.logger.error(f"logfile failure - found errors "
                                                f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")

            if validate_spawned_process_ended_message_found_in_workflow_logs_flag:
                etld_lib_functions.logger.error(f"log success - found spawned_process_ended function "
                                                f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            else:
                etld_lib_functions.logger.error(f"log failure - could not find spawned_process_ended function "
                                                f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            if validate_display_final_counter_message_found_in_workflow_logs_flag:
                etld_lib_functions.logger.error(f"log success - found display_final_counter function "
                                                f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            else:
                etld_lib_functions.logger.error(f"log failure - could not find display_final_counter function "
                                                f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")

        if all_tests_for_validation_passed_flag:
            etld_lib_functions.logger.info(f"All Tests Passed "
                                           f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            exit(0)
        else:
            etld_lib_functions.logger.error(f"Tests Failed "
                                             f"for: {etl_option_settings_dict}, workflow {log_workflow_date}")
            exit(1)


if __name__ == '__main__':
    etld_lib_functions.main(my_logger_prog_name="etl_validate")
    etld_lib_config.main()
    main(etl_validation_option="validate_etl_was")
