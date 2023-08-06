import os
from pathlib import Path
from qualys_etl.etld_lib import etld_lib_functions
from qualys_etl.etld_lib import etld_lib_config


def display_log_error_messages(error_messages_list):
    for error_message in error_messages_list:
        etld_lib_functions.logger.error(f"{error_message}")


def get_workflow_log_entry_dict(log_entry_line):
    log_entry_row_list = str(log_entry_line).split('|')
    log_entry_dict = {}
    if len(log_entry_row_list) == len(etld_lib_config.run_log_csv_columns()) and \
            log_entry_row_list[0].startswith("20"):
        for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
            column_name = etld_lib_config.run_log_csv_columns()[csv_index]
            log_entry_dict[f'{column_name}'] = str(log_entry_row_list[csv_index]).strip()

        log_workflow_list =  str(log_entry_dict['LOG_WORKFLOW']).split(':')
        if len(log_workflow_list) != 2:
            log_entry_dict['LOG_WORKFLOW_NAME'] = log_workflow_list[0]
            log_entry_dict['LOG_WORKFLOW_DATE'] = log_workflow_list[0]
        else:
            log_entry_dict['LOG_WORKFLOW_NAME'] = log_workflow_list[0]
            log_entry_dict['LOG_WORKFLOW_DATE'] = log_workflow_list[1]

        log_entry_dict['LOG_ROW_STRUCTURE_ISVALID'] = True
    else:
        log_entry_string = "".join(log_entry_line).strip()
        log_entry_dict['LOG_MESSAGE'] = f"UNBOUND LOG ERROR: {log_entry_string}"
        log_entry_dict['LOG_LEVEL'] = "ERROR"
        log_entry_dict['LOG_ROW_STRUCTURE_ISVALID'] = False

    return log_entry_dict


def get_workflow_log_last_entry(log_file):
    with open(str(log_file), "rb") as log_file_handle:
        try:
            log_file_handle.seek(-2, os.SEEK_END)
            while log_file_handle.read(1) != b'\n':
                log_file_handle.seek(-2, os.SEEK_CUR)
        except OSError:
            log_file_handle.seek(0)
        log_entry = log_file_handle.readline().decode()
        log_entry_dict = get_workflow_log_entry_dict(log_entry)
    return log_entry_dict


def get_workflow_log(log_file_path):
    last_log_entry_dict = get_workflow_log_last_entry(log_file_path)
    all_log_entries = []
    found_first_log_workflow = False
    if last_log_entry_dict['LOG_ROW_STRUCTURE_ISVALID']:
        with open(str(log_file_path), "rt", encoding='utf-8') as read_file:
            for log_entry_line in read_file:
                log_entry_dict = get_workflow_log_entry_dict(log_entry_line)
                if log_entry_dict['LOG_ROW_STRUCTURE_ISVALID']:
                    if str(log_entry_dict['LOG_WORKFLOW']).strip() == str(last_log_entry_dict['LOG_WORKFLOW']).strip():
                        all_log_entries.append(log_entry_dict)
                        found_first_log_workflow = True
                elif found_first_log_workflow:
                    #log_entry_dict = craft_log_out_of_bound_entry(last_log_entry_dict)
                    # Keep 'LOG_MESSAGE', 'LOG_LEVEL', change ['LOG_ROW_STRUCTURE_ISVALID'] = True
                    log_entry_dict['LOG_DATETIME'] = last_log_entry_dict['LOG_DATETIME']
                    log_entry_dict['LOG_WORKFLOW'] = last_log_entry_dict['LOG_WORKFLOW']
                    log_entry_dict['LOG_WORKFLOW_NAME'] = last_log_entry_dict['LOG_WORKFLOW_NAME']
                    log_entry_dict['LOG_WORKFLOW_DATE'] = last_log_entry_dict['LOG_WORKFLOW_DATE']
                    log_entry_dict['LOG_USERNAME'] = last_log_entry_dict['LOG_USERNAME']
                    log_entry_dict['LOG_FUNCTION'] = 'etld_lib_log_validation_out_of_bounds'
                    log_entry_dict['LOG_ROW_STRUCTURE_ISVALID'] = True
                    all_log_entries.append(log_entry_dict)
    else:
        #log_entry_dict = craft_log_out_of_bound_entry(last_log_entry_dict)
        # Completely out of bounds error.
        log_entry_dict = {
            'LOG_DATETIME': 'UNKNOWN',
            'LOG_LEVEL': 'ERROR',
            'LOG_MESSAGE': 'LAST LINE OF LOG FILE IS IN ERROR, PLEASE INVESTIGATE ISSUE',
            'LOG_WORKFLOW': 'UNKNOWN:UNKNOWN',
            'LOG_WORKFLOW_NAME': 'UNKNOWN',
            'LOG_WORKFLOW_DATE': 'UNKNOWN',
            'LOG_USERNAME': 'UNKNOWN',
            'LOG_FUNCTION': 'etld_lib_log_validation_completely_out_of_bounds',
            'LOG_ROW_STRUCTURE_ISVALID': True
        }
        all_log_entries.append(log_entry_dict)
    return all_log_entries


def test_workflow_spawned_process_ended(all_log_entries: list):
    etl_workflow_completed = False
    error_messages_list = []
    for log_entry_dict in all_log_entries:
        if log_entry_dict['LOG_FUNCTION'] == 'spawned_process_ended':
            etl_workflow_completed = True

    if etl_workflow_completed:
        pass
    else:
        error_messages_list.append(f"ERROR: Job did not complete, spawned_process_ended function not found.")

    return etl_workflow_completed


def test_workflow_log_no_errors_found_thus_far(all_log_entries: list):
    etl_workflow_valid_flag = True
    error_messages_list = []
    for log_entry_dict in all_log_entries:
        if log_entry_dict['LOG_LEVEL'] == 'ERROR':
            error_messages_list.append(f"ERROR: {log_entry_dict['LOG_MESSAGE']}")
            etl_workflow_valid_flag = False

    if etl_workflow_valid_flag:
        etld_lib_functions.logger.info(f"Passed Tests: {all_log_entries[0]['LOG_WORKFLOW']} ")
    else:
        display_log_error_messages(error_messages_list=error_messages_list)

    return etl_workflow_valid_flag


def test_workflow_log_completed_successfully(all_log_entries: list):
    etl_workflow_valid_flag = True
    error_messages_list = []
    for log_entry_dict in all_log_entries:
        if log_entry_dict['LOG_LEVEL'] == 'ERROR':
            error_messages_list.append(f"ERROR: {log_entry_dict['LOG_MESSAGE']}")
            etl_workflow_valid_flag = False

    if etl_workflow_valid_flag:
        etld_lib_functions.logger.info(f"Passed Tests: {all_log_entries[0]['LOG_WORKFLOW']} ")
    else:
        display_log_error_messages(error_messages_list=error_messages_list)

    if test_workflow_spawned_process_ended(all_log_entries):
        etl_workflow_valid_flag = False

    return etl_workflow_valid_flag


def validate_log_has_no_errors(etl_workflow_option):
    etl_workflow_location_dict = \
        etld_lib_config.get_etl_workflow_data_location_dict(etl_workflow_option)
    all_log_entries = get_workflow_log(log_file_path=Path(etl_workflow_location_dict['log_file']))
    return test_workflow_log_completed_successfully(all_log_entries)


def validate_log_has_no_errors_prior_to_distribution(etl_workflow_option):
    # Called by in process programs before end of job.
    etl_workflow_location_dict = \
        etld_lib_config.get_etl_workflow_data_location_dict(etl_workflow_option)
    all_log_entries = get_workflow_log(log_file_path=Path(etl_workflow_location_dict['log_file']))
    return test_workflow_log_no_errors_found_thus_far(all_log_entries)


def main_validate_log_has_no_errors(etl_workflow):
    etld_lib_functions.main(my_logger_prog_name='main_validate_log_has_no_errors')
    etld_lib_config.main()
    passed_all_tests = validate_log_has_no_errors(etl_workflow_option=etl_workflow)
    if passed_all_tests:
       pass
    else:
       exit(2)

    return passed_all_tests


def main_validate_all_logs_have_no_errors():
    etld_lib_functions.main(my_logger_prog_name='main_validate_all_logs_have_no_errors')
    etld_lib_config.main()
    main()


def main():
    final_exit_status = 0
    for etl_workflow in etld_lib_config.etl_workflow_list:
        passed_all_tests = \
            validate_log_has_no_errors(etl_workflow_option=etl_workflow)
        if passed_all_tests:
            pass
        else:
            final_exit_status = 2
    exit(final_exit_status)


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='etld_lib_log_validation')
    etld_lib_config.main()
    main()

#
# ARCHIVE
#
# @dataclass
# class EtlWorkflowValidation():
#     etl_workflow_log_file_path: Path
#     etl_workflow_sqlite_file_path: Path
#     etl_workflow_sqlite_obj: sqlite3
#     etl_workflow_validation_type: str
#     etl_workflow_status_table_name: str
#     etl_workflow_status_table_rows: sqlite3.Row
#     etl_workflow_option: str
#     etl_workflow_log_list: list
#     etl_workflow_log_errors_found: bool
#     etl_database_errors_found = bool
#     #
#     # if testing modules do not process log file where logs are sent to stdout.
#     # if Database Status Workflow Number and Last Line of Log File workflow number do not match, fail.
#     # if ERROR in log workflow number, fail.
#     # if out of bounds error ( python dump ) in section of last log entries, fail.
#     # if display_final_counter not found in last log entries, fail.
#     # if final time not found in last log entries, fail.
#     #
#
#
#     def __init__(self, etl_workflow_option, type='validation'):
#         self.etl_workflow_log_errors_found = False
#         self.etl_database_errors_found = False
#         self.etl_workflow_option = etl_workflow_option
#         self.etl_workflow_sqlite_file_path, \
#         self.etl_workflow_log_file_path = \
#             self.get_workflow_database_log_files(etl_workflow_option)
#         self.set_type(type)
#
#         def test_last_logs(etl_workflow_option):
#             etld_workflow_data_location_dict = \
#                 etld_lib_config.get_etl_workflow_data_location_dict(etl_workflow_option)
#             etl_workflow = etld_workflow_data_location_dict['etl_workflow']
#             self.etl_workflow_log_list = \
#                 self.get_workflow_log(self.etl_workflow_log_file_path,
#                                       self.log_workflow_date,
#                                       validate_last_log_entry=True)
#             test_etl_workflow_log_success_passed = \
#                 self.test_etl_workflow_log_success(
#                     etl_workflow_log_list=self.etl_workflow_log_list,
#                     etl_workflow_option=etl_workflow,
#                 )
#
#         try:
#             # GET DATABASE STATUS TABLE INFORMATION
#             if self.etl_workflow_sqlite_file_path.is_file():
#                 self.etl_workflow_sqlite_obj = \
#                     etld_lib_sqlite_tables.SqliteObj(str(self.etl_workflow_sqlite_file_path))
#
#                 self.etl_workflow_status_table_name =  \
#                     self.get_database_status_table_name(
#                         self.etl_workflow_sqlite_obj,
#                         sqlite_file_name=self.etl_workflow_sqlite_file_path)
#
#                 self.etl_workflow_status_table_rows = \
#                     self.get_database_status_table_rows(
#                         self.etl_workflow_sqlite_obj,
#                         self.etl_workflow_status_table_name,
#                         self.etl_workflow_sqlite_file_path)
#
#                 self.log_workflow_date, \
#                 self.log_workflow_name, \
#                 self.log_file_name = \
#                     self.get_log_workflow_info(self.etl_workflow_status_table_rows)
#
#                 self.disregard_sqlite_file, \
#                 self.etl_workflow_log_file_path = \
#                     self.get_workflow_database_log_files(etl_workflow_option=self.log_workflow_name)
#
#                 self.etl_workflow_log_list = \
#                     self.get_workflow_log(self.etl_workflow_log_file_path, self.log_workflow_date)
#
#                 etl_test_workflow_no_logs = etld_lib_config.get_etl_workflow_data_location_dict(self.log_workflow_name)
#                 # check if validate_etl workflow, then change
#                 if etl_workflow_option.__contains__("validate_etl"):
#                     self.etl_workflow_log_list = \
#                         self.get_workflow_log(self.etl_workflow_log_file_path, self.log_workflow_date, validate_last_log_entry=True)
#                     etld_workflow_data_location_dict = \
#                         etld_lib_config.get_etl_workflow_data_location_dict(etl_workflow_option)
#                     etl_workflow = etld_workflow_data_location_dict['etl_workflow']
#                     test_etl_workflow_log_success_passed = \
#                         self.test_etl_workflow_log_success(
#                             etl_workflow_log_list=self.etl_workflow_log_list,
#                             etl_workflow_option=etl_workflow,
#                         )
#                 elif etl_test_workflow_no_logs['etl_test_workflow_no_logs']:
#                     test_etl_workflow_log_success_passed = True
#                 else:
#                     test_etl_workflow_log_success_passed = \
#                         self.test_etl_workflow_log_success(
#                             etl_workflow_log_list=self.etl_workflow_log_list,
#                             etl_workflow_option=self.log_workflow_name,
#                         )
#                 test_all_tables_loaded_successfully_passed = \
#                     self.test_all_tables_loaded_successfully(self.etl_workflow_status_table_rows)
#
#                 if test_etl_workflow_log_success_passed:
#                     self.etl_workflow_log_errors_found = False
#                 else:
#                     self.etl_workflow_log_errors_found = True
#                     self.log_etl_workflow_log_errors(self.etl_workflow_log_list)
#
#                 if test_all_tables_loaded_successfully_passed:
#                     self.etl_database_errors_found = False
#                 else:
#                     self.etl_database_errors_found = True
#
#             else:
#                 self.etl_workflow_log_errors_found = True
#                 self.etl_database_errors_found = True
#                 self.etl_workflow_sqlite_obj = None
#                 self.etl_workflow_status_table_name = ""
#                 self.etl_workflow_status_table_rows = None
#                 raise Exception(f"Database Could Not Be Found: {str(self.etl_workflow_sqlite_file_path)}")
#
#         except Exception as e:
#             etld_lib_functions.logger.error(f"Exception {e}")
#             raise Exception(f"Database: {etl_workflow_option}")
#
#     def get_sqlite_obj(self, sqlite_file) -> etld_lib_sqlite_tables.SqliteObj:
#         sqlite_obj = None
#         if sqlite_file.is_file():
#             sqlite_obj = etld_lib_sqlite_tables.SqliteObj(str(self.etl_workflow_sqlite_file_path))
#         return sqlite_obj
#
#     def set_type(self, type="validation"):
#         self.etl_workflow_validation_type = type
#
#     def get_workflow_database_log_files(self, etl_workflow_option: str):
#         workflow_data_location_dict = etld_lib_config.get_etl_workflow_data_location_dict(etl_workflow_option)
#         if len(workflow_data_location_dict) > 0:
#             sqlite_file = workflow_data_location_dict['sqlite_file']
#             log_file = workflow_data_location_dict['log_file']
#         else:
#             raise Exception(f"Invalid option {etl_workflow_option}, please review options and rerun")
#
#         # if etl_workflow_option == 'validate_etl_knowledgebase' or etl_workflow_option == 'knowledgebase_etl_workflow':
#         #     sqlite_file = etld_lib_config.kb_sqlite_file
#         #     log_file = etld_lib_config.kb_log_file
#         # elif etl_workflow_option == 'validate_etl_host_list' or etl_workflow_option == 'host_list_etl_workflow':
#         #     sqlite_file = etld_lib_config.host_list_sqlite_file
#         #     log_file = etld_lib_config.host_list_log_file
#         # elif etl_workflow_option == 'validate_etl_host_list_detection' or etl_workflow_option == 'host_list_detection_etl_workflow':
#         #     sqlite_file = etld_lib_config.host_list_detection_sqlite_file
#         #     log_file = etld_lib_config.host_list_detection_log_file
#         # elif etl_workflow_option == 'validate_etl_asset_inventory' or etl_workflow_option == 'asset_inventory_etl_workflow':
#         #     sqlite_file = etld_lib_config.asset_inventory_sqlite_file
#         #     log_file = etld_lib_config.asset_inventory_log_file
#         # elif etl_workflow_option == 'validate_etl_was' or etl_workflow_option == 'was_etl_workflow':
#         #     sqlite_file = etld_lib_config.was_sqlite_file
#         #     log_file = etld_lib_config.was_log_file
#         # else:
#         #     raise Exception(f"Invalid option {etl_workflow_option}, please review options and rerun")
#
#         return sqlite_file, log_file
#
#     def get_database_status_table_name(self, sqlite_obj, sqlite_file_name, schema_name='sqlite_master') -> str:
#         select_status_table_name = f"SELECT name FROM {schema_name} WHERE type ='table' AND name LIKE '%_status'"
#         status_table_row = sqlite_obj.select_from_table(select_statement=select_status_table_name)
#         if len(status_table_row) == 0:
#             raise Exception(f"status tables missing from Database.  Rerun when database is ready. {sqlite_file_name}")
#         status_table_name = status_table_row[0]['name']
#         return status_table_name
#
#     def get_database_status_table_rows(self, sqlite_obj, status_table_name, sqlite_file_name) -> sqlite3.Row:
#         select_all_status_rows = f"SELECT * FROM {status_table_name}"
#         all_status_rows = sqlite_obj.select_from_table(select_statement=select_all_status_rows)
#         if len(all_status_rows) == 0:
#             raise Exception(
#                 f"Could not find status rows in table {status_table_name}.  Rerun when database is ready. {sqlite_file_name}")
#         return all_status_rows
#
#     def get_log_workflow_info(self, status_table_rows: sqlite3.Row):
#         log_workflow_date = ""
#         log_workflow_name = ""
#         log_file_name = ""
#         try:
#             row = status_table_rows[-1] # Get Last Row
#             status_name = row['status_name']
#             status_detail_dict = json.loads(row['status_detail'])
#             status = status_detail_dict['STATUS']
#             log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
#             log_workflow_name = status_detail_dict['LOG_WORKFLOW_NAME']
#             disregard_sqlite_file, log_file_name = \
#                 self.get_workflow_database_log_files(etl_workflow_option=log_workflow_name)
#         except Exception as e:
#             etld_lib_functions.logger.error(f"ERROR get_log_workflow_info")
#             etld_lib_functions.logger.error(f"ERROR Exception {e}")
#             log_workflow_name = ""
#             log_workflow_date = ""
#             log_file_name = ""
#
#         return log_workflow_date, log_workflow_name, log_file_name
#
#     def get_workflow_log_last_entry(self, log_file):
#         with open(str(log_file), "rb") as file:
#             try:
#                 file.seek(-2, os.SEEK_END)
#                 while file.read(1) != b'\n':
#                     file.seek(-2, os.SEEK_CUR)
#             except OSError:
#                 file.seek(0)
#             log_entry = file.readline().decode()
#             log_entry_row_list = str(log_entry).split('|')
#             log_entry_dict = {}
#             if len(log_entry_row_list) == len(etld_lib_config.run_log_csv_columns()) and \
#                     log_entry_row_list[0].startswith("20"):
#                 # Normal Log
#                 for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                     column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                     log_entry_dict[f'{column_name}'] = str(log_entry_row_list[csv_index]).strip()
#                 log_entry_dict['LOG_WORKFLOW_NAME'], log_entry_dict['LOG_WORKFLOW_DATE'] = str(log_entry_dict['LOG_WORKFLOW']).split(':')
#         return log_entry_dict
#
#     def get_workflow_log(self, log_file, log_workflow_date, validate_last_log_entry=False):
#         if validate_last_log_entry:
#             last_log_entry_dict = self.get_workflow_log_last_entry(log_file)
#             log_workflow_date = last_log_entry_dict['LOG_WORKFLOW_DATE']
#
#         log_list = []
#         log_file_path = log_file
#         log_workflow_date = log_workflow_date
#         # Validate logs have no errors
#         first_log_entry = []
#         found_workflow_log_flag = False
#         number_of_runlog_columns = len(etld_lib_config.run_log_csv_columns())
#
#         try:
#             with open(str(log_file_path), "rt", encoding='utf-8') as read_file:
#                 for log_line in read_file:
#                     log_entry = log_line.split('|')
#                     if found_workflow_log_flag:
#                         pass
#                     elif len(log_entry) == number_of_runlog_columns and log_workflow_date in log_entry[2]:
#                         found_workflow_log_flag = True
#                         first_log_entry = log_entry
#                     else:
#                         continue
#
#                     log_entry_dict = {}
#                     if len(log_entry) == number_of_runlog_columns and log_entry[0].startswith("20"):
#                         # Normal Log
#                         for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                             column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                             log_entry_dict[f'{column_name}'] = str(log_entry[csv_index]).strip()
#                         if log_entry_dict['LOG_LEVEL'] == 'ERROR':
#                             found_workflow_log_errors_flag = True
#                     else:
#                         # Error Log outside of logging. E.g. Kill Processes
#                         last_log_list_entry_processed = log_list[-1]
#                         for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                             column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                             log_entry_dict[f'{column_name}'] = str(last_log_list_entry_processed[column_name]).strip()
#                         # for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                         #     column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                         #     log_entry_dict[f'{column_name}'] = str(first_log_entry[csv_index]).strip()
#                         log_entry_string = "".join(log_entry).strip()
#                         log_entry_dict['LOG_MESSAGE'] = f"UNBOUND LOG ERROR: {log_entry_string}"
#                         log_entry_dict['LOG_LEVEL'] = "ERROR"
#                         log_entry_dict['LOG_FUNCTION'] = "etld_lib_log_validation"
#                     log_list.append(log_entry_dict)
#
#         except Exception as e:
#             etld_lib_functions.logger.error(f"exception {e}")
#             raise Exception("Errror in get_workflow_log")
#
#         return log_list
#
#     def test_all_tables_loaded_successfully(self, status_table_rows: sqlite3.Row):
#         all_tables_loaded_successfully_flag = False
#         try:
#             for row in status_table_rows:
#                 status_name = row['status_name']
#                 if str(status_name).__contains__("ALL_TABLES_LOADED_SUCCESSFULLY"):
#                     all_tables_loaded_successfully_flag = True
#         except Exception as e:
#             all_tables_loaded_successfully_flag = False
#
#         return all_tables_loaded_successfully_flag
#
#     def test_etl_workflow_log_success(self, etl_workflow_log_list, etl_workflow_option):
#         success_flag = False
#         for log_entry in etl_workflow_log_list:
#             if 'LOG_LEVEL' in log_entry:
#                 if log_entry['LOG_LEVEL'] == 'ERROR':
#                     success_flag = False
#                     break
#                 else:
#                     success_flag = True
#         if len(etl_workflow_log_list) > 0:
#             pass
#         else:
#            # TESTING, no logs available.
#            if etl_workflow_option.__contains__('_0'):
#                # function knowledgebase_05_transform_load_xml_to_sqlite
#                success_flag = True
#
#         return success_flag
#
#     def log_etl_workflow_log_errors(self, etl_workflow_log_list):
#         for log_entry in etl_workflow_log_list:
#             if 'LOG_LEVEL' in log_entry:
#                 if log_entry['LOG_LEVEL'] == 'ERROR':
#                     log_entry_dict = {}
#                     for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                         column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                         log_entry_dict[f'{column_name}'] = str(log_entry[column_name]).strip()
#                     etld_lib_functions.logger.error(f"ERRORS FOUND - "
#                                                     f"LOG_WORKFLOW: {log_entry_dict['LOG_WORKFLOW']}, "
#                                                     f"LOG_USERNAME: {log_entry_dict['LOG_USERNAME']}, "
#                                                     f"LOG_FUNCTION: {log_entry_dict['LOG_FUNCTION']}, "
#                                                     f"LOG_MESSAGE: {log_entry_dict['LOG_MESSAGE']}"
#                                                     f"")
#
#     def log_etl_workflow_function_results(self, etl_workflow_log_list, log_function):
#         found_log_function = False
#         message_text = ""
#         first_log_entry = []
#         if len(etl_workflow_log_list) > 0:
#            first_log_entry = etl_workflow_log_list[0]
#         else:
#             etld_lib_functions.logger.error(f"NO LOG ENTRIES FOUND FOR {self.etl_workflow_option}")
#             raise Exception("error in log_etl_workflow_function_results")
#
#         log_entry_dict = {'LOG_WORKFLOW': "", 'LOG_USERNAME': "", 'LOG_FUNCTION': "", 'LOG_MESSAGE': ""}
#         for log_entry in etl_workflow_log_list:
#             if 'LOG_LEVEL' in log_entry and \
#                     log_entry['LOG_LEVEL'] == 'INFO' and \
#                     log_function in log_entry['LOG_FUNCTION']:
#                     found_log_function = True
#                     log_entry_dict = {'LOG_WORKFLOW': "",
#                                       'LOG_USERNAME': "",
#                                       'LOG_FUNCTION': "",
#                                       'LOG_MESSAGE': ""}
#                     for csv_index in range(len(etld_lib_config.run_log_csv_columns())):
#                         column_name = etld_lib_config.run_log_csv_columns()[csv_index]
#                         log_entry_dict[f'{column_name}'] = str(log_entry[column_name]).strip()
#                     message_text = f"{log_entry['LOG_FUNCTION']} - "\
#                                    f"LOG_WORKFLOW: {log_entry_dict['LOG_WORKFLOW']}, "\
#                                    f"LOG_USERNAME: {log_entry_dict['LOG_USERNAME']}, "\
#                                    f"LOG_FUNCTION: {log_entry_dict['LOG_FUNCTION']}, "\
#                                    f"LOG_MESSAGE: {log_entry_dict['LOG_MESSAGE']}"\
#                                    f""
#         if found_log_function:
#             etld_lib_functions.logger.info(message_text)
#         else:
#             message_text = f"LOG_FUNCTION: {log_function}  NOT FOUND IN LOGGING - " \
#                            f"LOG_WORKFLOW: {log_entry_dict['LOG_WORKFLOW']}, " \
#                            f"LOG_USERNAME: {log_entry_dict['LOG_USERNAME']}, " \
#                            f"LOG_FUNCTION: {log_entry_dict['LOG_FUNCTION']}, " \
#                            f"LOG_MESSAGE: {log_entry_dict['LOG_MESSAGE']}" \
#                            f""
#             etld_lib_functions.logger.warning(message_text)
#
#         return found_log_function
#
#
# def test_etl_workflow(etl_workflow):
#
#     passed_all_tests = False
#
#     try:
#         etl_obj = EtlWorkflowValidation(etl_workflow_option=etl_workflow)
#         if etl_obj.etl_workflow_sqlite_obj is None:
#             etld_lib_functions.logger.error(
#                 f"etl_workflow_option{etl_workflow} "
#                 f"database {etl_obj.etl_workflow_sqlite_file_path} not found")
#             passed_all_tests = False
#         else:
#             for row in etl_obj.etl_workflow_status_table_rows:
#                 status_name = row['status_name']
#                 status_detail_dict = json.loads(row['status_detail'])
#                 status = status_detail_dict['STATUS']
#                 log_workflow_date = status_detail_dict['LOG_WORKFLOW_DATE']
#                 log_workflow_name = status_detail_dict['LOG_WORKFLOW_NAME']
#                 etl_workflow_log_path = etl_obj.etl_workflow_log_file_path
#                 if etl_obj.etl_workflow_log_errors_found:
#                     etl_workflow_log_message = "log file has errors, do not process data."
#                     passed_all_tests = False
#                 elif len(etl_obj.etl_workflow_log_list) == 0:
#                     etl_test_workflow_no_logs = \
#                         etld_lib_config.get_etl_workflow_data_location_dict(etl_obj.log_workflow_name)
#                     if etl_test_workflow_no_logs['etl_test_workflow_no_logs']:
#                         etl_workflow_log_message = "testing only, log files are not analyzed."
#                         passed_all_tests = True
#                     else:
#                         etl_workflow_log_message = "error, NO LOG ENTRIES FOUND IN LOGFILE, see logfile."
#                         passed_all_tests = False
#                 else:
#                     etl_workflow_log_message = "LOG CHECK"
#                     passed_all_tests = True
#
#                 if passed_all_tests:
#                     pass_or_fail_message = "SUCCESS"
#                     log_function = etld_lib_functions.logger.info
#                 else:
#                     pass_or_fail_message = "ERROR"
#                     log_function = etld_lib_functions.logger.error
#
#                 log_function(
#                     f""
#                     f"{pass_or_fail_message} {etl_workflow}, "
#                     f"log_workflow_date {log_workflow_date}, "
#                     f"log_workflow_path {str(etl_workflow_log_path)}, "
#                     f"{pass_or_fail_message} {etl_workflow_log_message}, "
#                     f"workflow_that_updated_table: {log_workflow_name}, "
#                     f"results {status}, "
#                     f"table_status {etl_obj.etl_workflow_status_table_name}, "
#                     f"tables_tested {status_name} "
#                 )
#
#     except Exception as e:
#         passed_all_tests = False
#         etld_lib_functions.logger.error(
#             f"ERROR: {etl_workflow}, failed - "
#             f"Exception {e} - "
#         )
#
#     return passed_all_tests
#
#
# def test_etl_workflow_from_qetl_manage_user(etl_workflow):
#     etld_lib_functions.main(my_logger_prog_name=etl_workflow)
#     etld_lib_config.main()
#     passed_all_tests = \
#         test_etl_workflow(etl_workflow)
#     return passed_all_tests
