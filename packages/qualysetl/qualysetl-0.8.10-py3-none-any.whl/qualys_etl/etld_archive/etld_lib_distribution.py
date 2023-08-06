import shutil
import os
from qualys_etl.etld_lib import etld_lib_functions as etld_lib_functions


def select_latest_batch_from_sqlite_database_table():
    # TODO Select statement to extract the last batch of data from table
    pass


def create_data_distribution_directory():
    # TODO Create qetl_home/data_distribution/ directory that will contain
    # extractions of sqlite database
    #
    pass


def select_database_status_detail_to_determine_if_job_completed():
    # TODO select STATUS_DETAIL json from SQLITE database
    # determine if FINAL BATCH LOADED
    pass


def csv_repair_field_method():
    # TODO Method to repair csv fields in preparation for db loaded
    # # REPLACE SQL OPERATION - Required to prepare CSV for GLUE SQL Loader limitation on parsing CSV.
    # #
    # #     1. char(13) carriage return   - Remove Carriage Returns from results
    # #     2. char(10) line feed         - Replace line feed with space ' '
    # #     3. '|'                        - Replace pipe '|' with char(9) tab
    # #     REPLACE(REPLACE(REPLACE($COLUMN_DATA, char(13), ''), char(10), ' '), '|', char(09)) RESULTS,
    # #
    # # The Replace SQL Operation is applied to fields that have embedded characters that break Glue SQL Loader.
    # #
    # # 1. Validate previous run of QualysETL had no ERROR in log file.
    # # 2. Create backup of sqlite database naming it "host_list_detection_sqlite_backup_YYMMDDhhmmss.db
    # # 3. Execute select extract of data files to TABLE_NAME_YYMMDDhhmmss.csv for distribution to AWS Glue.
    # #
    #
    # function repair_data_field_for_aws_glue() {
    # # Create replace sql statement
    # # $1 is column name
    # # $2 is resulting column name
    # cat <<EOF
    #   SUBSTR(REPLACE(REPLACE(REPLACE($1, char(13), ''), char(10), ' '), '|', char(09)),1,$MAX_COLUMN_DATA_SIZE) $2
    # EOF
    # }

    pass


def copy_results_to_external_target(source_list=None, target=None):

    if target == 'default':
        etld_lib_functions.logger.info(f"No export_dir set: {target}")
        pass
    elif os.path.isdir(target):
        try:
            for file_path in source_list:
                if os.path.exists(file_path):
                    shutil.copy2(str(file_path), str(target), follow_symlinks=True)
                    etld_lib_functions.logger.info(f"{str(file_path)} distributed to {str(target)}")

                else:
                    etld_lib_functions.logger.warning(f"file doesn't exists:{str(file_path)} "
                                            f"cannot distribute to {str(target)}")
        except Exception as e:
            etld_lib_functions.logger.error(f"Exception: {e}")
            etld_lib_functions.logger.error(f"Error distributing files.  ")
            etld_lib_functions.logger.error(f"etld_lib_config_settings.yaml [named]_export_dir "
                                            f"directory accessibility issue: {target}")
            exit(1)
    else:
        etld_lib_functions.logger.error(f"Program aborting, etld_lib_config_settings.yaml "
                                        f"[named]_export_dir directory does not exist: {target}")
        exit(1)
