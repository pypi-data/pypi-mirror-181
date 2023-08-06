import datetime
import inspect
import logging
import sys
import time
import getpass
import psutil
import re
from pathlib import Path
from importlib import util as importlib_util
import qualys_etl


class StartLoggingToStdout:

    def __init__(self, log_level=logging.INFO, my_logger_prog_name=None, logging_is_on_flag=False):
        self.logging_is_on_flag = logging_is_on_flag
        self.log_level = log_level
        self.logger, \
        self.logger_datetime, \
        self.logger_iso_format_datetime, \
        self.logger_database_format_datetime, \
        self.my_logger_program_name_for_database_routine = \
            self.setup_logging_stdout(log_level, my_logger_prog_name, logging_is_on_flag=True)

        self.check_modules()
        self.check_python_version()
        self.get_sqlite_version()
        self.qetl_code_dir, \
        self.qetl_code_dir_child, \
        self.qetl_code_dir_child_api_host_list, \
        self.qetl_code_dir_child_api_knowledgebase, \
        self.qetl_code_dir_child_api_lib, \
        self.qetl_code_dir_child_api_templates = self.set_qetl_code_dir()

    # @staticmethod
    # def get_dbm_type(file_name):
    #     dbm_type = dbm.whichdb(file_name)
    #     if dbm_type == '':
    #         dbm_type = 'unknown'
    #
    #     return dbm_type

    # def flatten_nest(self, nested_data):  # Flatten nested dictionary into string
    #     def nested_items():
    #         if isinstance(nested_data, list):
    #             for key, value in enumerate(nested_data):
    #                 if isinstance(value, dict) or isinstance(value, list):
    #                     for nested_key, nested_value in self.flatten_nest(value).items():
    #                         yield str(key) + "." + nested_key, nested_value
    #                 else:
    #                     yield str(key), value
    #         else:
    #             for key, value in nested_data.items():
    #                 if isinstance(value, dict) or isinstance(value, list):
    #                     for nested_key, nested_value in self.flatten_nest(value).items():
    #                         yield key + "." + nested_key, nested_value
    #                 else:
    #                     yield key, value
    #     return dict(nested_items())
    #
    # @staticmethod
    # def remove_low_high_values(chunk):  # Remove utf-8 values other than utf-8 decimal 10, 32-126
    #     encoding = chardet.detect(chunk)['encoding']
    #     chunk = chunk.decode(encoding, 'replace')
    #     new_chunk = ''
    #     for index in range(0, len(chunk)):
    #         try:
    #             size = ord(chunk[index])
    #             if (size == 10) or (size == 9) or (127 > size > 31):
    #                 new_chunk = new_chunk + chunk[index]
    #             else:
    #                 new_chunk = new_chunk + ""
    #         except Exception as e:
    #             new_chunk = new_chunk + ""
    #     chunk = new_chunk.encode('utf-8')
    #     return chunk

    @staticmethod
    def truncate_csv_cell(max_length=32700, csv_cell="", truncated_field_list="", csv_column=""):
        if max_length == 0:
            pass
        elif len(csv_cell) > max_length:
            truncated_field_list = \
                f"{truncated_field_list}{csv_column}:{len(csv_cell):,} truncated_at: {max_length:,}\n"
            csv_cell = csv_cell[:max_length]

        return csv_cell, truncated_field_list

    def check_python_version(self):
        py_version = sys.version.split('\n')
        try:
            if (sys.version_info[0] >= 3) and (sys.version_info[1] >= 8):
               self.logger.info(f"Python version found is: {py_version}")
            else:
               self.logger.info("Error: sys.version.info failed.  Please use Python version 3.8 or greater.")
               raise ValueError(f"Python version < 3.8 found: {py_version}")
        except Exception as e:
            self.logger.error(f"Please install a version of python that can work with this product.")
            self.logger.error(f"Exception: {e}")
            exit(1)

    @staticmethod
    def get_file_size(path_to_file):
        if Path(path_to_file).is_file():
            return Path(path_to_file).stat().st_size

    @staticmethod
    def get_file_mtime(path_to_file):
        if Path(path_to_file).is_file():
            statinfo = Path(path_to_file).stat()
            return statinfo.st_mtime

    # def dbm_type_message(self, dbm_file):
    #     dbm_type = self.get_dbm_type(str(dbm_file))
    #     if dbm_type == "dbm.gnu":
    #         message = "dbm.gnu is best performing DBM, you are good to go!"
    #     else:
    #         message = f"{dbm_type} may result in errors.  Please consider moving to dbm.gnu which is optimal."
    #     return message

    def get_sqlite_version(self):
        global logger
        import sqlite3
        version_info = sqlite3.sqlite_version_info
        if (version_info[0] >= 3) and (version_info[1] >= 26):
            self.logger.info(f"SQLite version found is: {sqlite3.sqlite_version}.")
        else:
            self.logger.error(f"SQLite version {sqlite3.sqlite_version} is older than 3.31. Please upgrade sqlite.")
            exit(1)

        return sqlite3.version

    def setup_logging_stdout(self, log_level=logging.INFO, my_logger_prog_name=None, logging_is_on_flag=True):

        logging.Formatter.converter = time.gmtime
        d = datetime.datetime.utcnow()
        td = f"{d.year}{d.month:02d}{d.day:02d}{d.hour:02d}{d.minute:02d}{d.second:02d}"
        logger_datetime = td
        logger_iso_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d}T{d.hour:02d}:{d.minute:02d}:{d.second:02d}Z"
        logger_database_format_datetime = f"{d.year}-{d.month:02d}-{d.day:02d} {d.hour:02d}:{d.minute:02d}:{d.second:02d}"
        my_logger_program_name_for_database_routine = my_logger_prog_name
        username = getpass.getuser()
        prog = Path(__file__).name
        if my_logger_prog_name is not None:
            prog = my_logger_prog_name

        prog = f"{prog}: {td}"

        logging.basicConfig(format=f"%(asctime)s | %(levelname)-8s | {prog:54s} | {username:15} | %(funcName)-60s | %(message)s",
                            level=log_level,
                            )

        logger = logging.getLogger()  # Useful in qetl_manage_user when we want to set the name.
        logger.info(f"PROGRAM:     {sys.argv}")
        logger.info(f"QUALYSETL VERSION: {qualys_etl.__version__}")
        logger.info(f"LOGGING SUCCESSFULLY SETUP FOR STREAMING")
        return logger, logger_datetime, logger_iso_format_datetime, logger_database_format_datetime, my_logger_program_name_for_database_routine

    def setup_logging_to_file(self, logfile_path, log_level=logging.INFO):
        logging.Formatter.converter = time.gmtime
        logging.basicConfig(format=f"%(asctime)s - %(levelname)s - %(message)s",
                            filename=logfile_path,
                            level=log_level)
        self.logger
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"LOGGING SUCCESSFULLY SETUP TO {str(logfile_path)}")

    def lineno(self):
        return inspect.currentframe().f_back.f_lineno

    def check_modules(self):
        try:
            import requests
            import oschmod
            import yaml
            import xmltodict
            import boto3
            import base64
            import shutil
            import chardet
        except ImportError as e:
            self.logger.error(f"Missing Required Module: {e}")
            self.logger.error(f"Please review installation instructions and ensure you have all required modules installed.")
            exit(1)

    # def set_logging_level(self, log_level=logging.INFO):
    #     self.logging_level = log_level  # Set to logging.WARNING to only log Warnings and Errors.


    def set_qetl_code_dir(self,log=True): # Module Directories
        test_exec_for_qetl_code_dir = __file__
        test_spec_for_qetl_code_dir = importlib_util.find_spec("qualys_etl")  # Installed on system

        result = ""
        if test_exec_for_qetl_code_dir.__contains__("qualys_etl"):
            result = re.sub("qualys_etl.*", '', test_exec_for_qetl_code_dir)
        elif test_spec_for_qetl_code_dir is not None:
            result = re.sub("qualys_etl.*", '', test_spec_for_qetl_code_dir.origin)
        else:
            self.logger.error(f"test_exec_for_qetl_code_dir - {test_exec_for_qetl_code_dir}")
            self.logger.error(f"test_spec_for_qetl_code_dir  - {test_spec_for_qetl_code_dir}")
            self.logger.error(f"Could not determine qetl code directory location.")
            self.logger.error(f"Please execute qetl_manage_users.py to test user")
            exit(1)

        # Module Directories
        qetl_code_dir = Path(result)
        qetl_code_dir_child = Path(qetl_code_dir, "qualys_etl")
        qetl_code_dir_child_api_host_list = Path(qetl_code_dir_child, "etld_host_list")
        qetl_code_dir_child_api_knowledgebase = Path(qetl_code_dir_child, "etld_knowledgebase")
        qetl_code_dir_child_api_lib = Path(qetl_code_dir_child, "etld_lib")
        qetl_code_dir_child_api_templates = Path(qetl_code_dir_child, "etld_templates")

        # Ensure modules are on sys.path
        modules = [qetl_code_dir_child, qetl_code_dir_child_api_lib, qetl_code_dir_child_api_templates,
                   qetl_code_dir_child_api_knowledgebase, qetl_code_dir_child_api_host_list]
        for path in modules:
            if not sys.path.__contains__(str(path.absolute())):
                sys.path.insert(0, str(path))

        self.logger.info(f"qualysetl app dir    - {qetl_code_dir}")
        self.logger.info(f"qualys_etl code dir  - {qetl_code_dir_child}")
        self.logger.info(f"etld_lib             - {qetl_code_dir_child_api_lib}")
        self.logger.info(f"etld_templates       - {qetl_code_dir_child_api_templates}")
        self.logger.info(f"etld_knowledgebase   - {qetl_code_dir_child_api_knowledgebase}")
        self.logger.info(f"etld_host_list        - {qetl_code_dir_child_api_host_list}")

        return  qetl_code_dir, \
                qetl_code_dir_child, \
                qetl_code_dir_child_api_host_list, \
                qetl_code_dir_child_api_knowledgebase, \
                qetl_code_dir_child_api_lib, \
                qetl_code_dir_child_api_templates

    # def log_dbm_info(self, file_name, msg=""):
    #     if exists(str(file_name)):
    #         dbm_type = self.get_dbm_type(str(file_name))
    #         logger.info(f"{msg}dbm etl_workflow_validation_type - {dbm_type} - {str(file_name)}")
    #         if dbm_type == "dbm.gnu" or dbm_type is None:
    #             pass
    #         else:
    #             logger.info(f"{msg}dbm etl_workflow_validation_type warning - {dbm_type} may lead to inconsistent results.")
    #             logger.info(f"{msg}dbm etl_workflow_validation_type warning - {dbm_type} move to linux gnu dbm.")

    # def log_dbm_count_of_keys_found(self, file_name):
    #     if exists(str(file_name)):
    #         dbm_type = self.get_dbm_type(str(file_name))
    #         if dbm_type == "dbm.gnu" or dbm_type is None:
    #             with dbm.gnu.open(str(file_name), 'rf') as sd:
    #                 count = len(sd)
    #                 logger.info(f"keys found: {count:,} in dbm.gnu shelve: {str(file_name)}")

    def get_formatted_file_info_dict(self, file_name):
        file_path = Path(file_name)
        if file_path.is_file():
            file_size = self.human_readable_size(Path(file_name).stat().st_size)
            file_change_time = Path(file_name).stat().st_ctime
            d = datetime.datetime.fromtimestamp(file_change_time)
            td = f"{d.year}-{d.month:02d}-{d.day:02d} {d.hour:02d}:{d.minute:02d}:{d.second:02d} local timezone"
            return {'file_size': file_size, 'file_change_time': td}
        else:
            return {'file_size': '', 'file_change_time': ''}

    def human_readable_size(self, size_in_bytes):
        my_bytes = float(size_in_bytes)
        kilobytes = float(1024)
        megabytes = float(kilobytes ** 2)
        gigabytes = float(kilobytes ** 3)
        terabytes = float(kilobytes ** 4)
        petabytes = float(kilobytes ** 5)

        if my_bytes < kilobytes:
            message = 'bytes' if 0 == my_bytes > 1 else 'byte'
            return f'{my_bytes} {message}'
        elif kilobytes <= my_bytes < megabytes:
            return f'{(my_bytes / kilobytes):0.2f} kilobytes'
        elif megabytes <= my_bytes < gigabytes:
            return f'{(my_bytes / megabytes):0.2f} megabytes'
        elif gigabytes <= my_bytes < terabytes:
            return f'{(my_bytes / gigabytes):0.2f} gigabytes'
        elif terabytes <= my_bytes:
            return f'{(my_bytes / terabytes):0.2f} terabytes'
        elif petabytes <= my_bytes:
            return f'{(my_bytes / petabytes):0.2f} petabytes'

    def log_file_info(self, file_name, msg1='output file'):
        file_info = self.get_formatted_file_info_dict(file_name)
        logger.info(f"{msg1} - {str(file_name)} size: {file_info.get('file_size')} "
                    f"change time: {file_info.get('file_change_time')}")

    def file_is_locked(self, test_lock_file=None):
        # TODO determine if checking locking in each method is needed.
        # TODO note that all actions should be run through qetl_manage_user which locks the jobstream.
        try:
            if Path(test_lock_file).is_file():
                with open(test_lock_file, 'wb+') as tlf:        # If locked, exit.
                    # lock file is free
                    return False
            else:
                # lock file doesn't exist
                return False
        except Exception as e:
            return True

    def log_system_information(self, logger_method=print, data_directory="/opt/qetl/users"):
        # TODO Calculate final averages of cpu, mem usage.
        sys_stat_counters = {
            'cpu_usage_pct': self.get_cpu_usage_pct(),
            'cpu_frequency': self.get_cpu_frequency(),
            'cpu_count': self.get_cpu_count(),
            'ram_usage_pct': self.get_ram_usage_pct(),
            'ram_size_total_in_mb': self.get_ram_size_total_in_mb(),
            'ram_size_usage_in_mb': self.get_ram_size_usage_in_mb(),
            'ram_size_available_in_mb': self.get_ram_size_available_in_mb(),
            'swap_usage_pct': self.get_swap_usage_pct(),
            'swap_size_total_in_mb': self.get_swap_size_total_in_mb(),
            'swap_size_usage_in_mb': self.get_swap_size_usage_in_mb(),
            'swap_size_available_in_mb': self.get_swap_size_available_in_mb(),
            'disk_usage_pct': 0,
            'disk_size_total_in_mb': 0,
            'disk_size_usage_in_mb': 0,
            'disk_size_available_in_mb': 0,
        }

        logger_method(
            f'SYS STAT: CPU usage={sys_stat_counters["cpu_usage_pct"]} %, '
            f'frequency='
            f'{sys_stat_counters["cpu_frequency"]} MHz, '
            f'count='
            f'{sys_stat_counters["cpu_count"]}'
        )
        logger_method(
            f'SYS STAT: RAM usage='
            f'{sys_stat_counters["ram_usage_pct"]} %, '
            f'total='
            f'{sys_stat_counters["ram_size_total_in_mb"]:,.0f} MB, '
            f'used='
            f'{sys_stat_counters["ram_size_usage_in_mb"]:,.0f} MB, '
            f'available='
            f'{sys_stat_counters["ram_size_available_in_mb"]:,.0f} MB '
        )
        logger_method(
            f'SYS STAT: SWAP usage='
            f'{sys_stat_counters["swap_usage_pct"]} %, '
            f'total='
            f'{sys_stat_counters["swap_size_total_in_mb"]:,.0f} MB, '
            f'used='
            f'{sys_stat_counters["swap_size_usage_in_mb"]:,.0f} MB, '
            f'available='
            f'{sys_stat_counters["swap_size_available_in_mb"]:,.0f} MB '
        )

        try:
            disk_usage_pct = self.get_disk_usage_pct(data_dir=data_directory)
            disk_size_total_in_mb = self.get_disk_size_total_in_mb(data_dir=data_directory)
            disk_size_usage_in_mb = self.get_disk_size_usage_in_mb(data_dir=data_directory)
            disk_size_available_in_mb = self.get_disk_size_available_in_mb(data_dir=data_directory)
            sys_stat_counters['disk_usage_pct'] = disk_usage_pct
            sys_stat_counters['disk_size_total_in_mb'] = disk_size_total_in_mb
            sys_stat_counters['disk_size_usage_in_mb'] = disk_size_usage_in_mb
            sys_stat_counters['disk_size_available_in_mb'] = disk_size_available_in_mb
            logger_method(
                f'SYS STAT: DISK usage='
                f'{sys_stat_counters["disk_usage_pct"]} %, '
                f'total='
                f'{sys_stat_counters["disk_size_total_in_mb"]:,.0f} MB, '
                f'used='
                f'{sys_stat_counters["disk_size_usage_in_mb"]:,.0f} MB, '
                f'available='
                f'{sys_stat_counters["disk_size_available_in_mb"]:,.0f} MB, '
                f'path='
                f'{data_directory}, '
            )
        except Exception as e:
            pass

        return sys_stat_counters

    def if_disk_space_usage_greater_than_90_log_warning(self, logger_method=print, data_directory="/opt/qetl/users"):
        try:
            disk_size_usage_pct = int(self.get_disk_usage_pct(data_dir=data_directory))
            if disk_size_usage_pct > 90:
                logger_method(f'SYS WARNING: DISK percent usage > 90% at {disk_size_usage_pct}%')
        except Exception as e:
            pass

    def if_swap_space_total_is_zero_abort(self, logger_method=print):
        if int(self.get_swap_size_total_in_mb()) > 0:
            pass
        else:
            logger_method(f'SYS ERROR: Please contact your systems administrator to configure swap space.')
            logger_method(f'SYS ERROR: current swap space size is: {self.get_swap_size_total_in_mb():,.0f} MB, ')
            exit(1)

    def if_swap_space_total_is_low_log_warning(self, logger_method=print):
        if int(self.get_swap_size_total_in_mb()) < 4000:
            logger_method(f'SYS WARNING: SWAP size total is < 4 Gig. '
                          f'Consider increasing SWAP to support larger batch jobs and sql queries')

    def if_ram_space_size_is_low_log_warning(self, logger_method=print):
        ram_size_total_in_mb = int(self.get_ram_size_total_in_mb())
        if ram_size_total_in_mb < 8100:
            logger_method(f'SYS WARNING: RAM size total < 8 Gig.  '
                          f'Consider increasing RAM to support larger batch jobs and sql queries')


    # def proc_table(self, logger_method=print):
    #     for proc in psutil.process_iter(['pid', 'name']):
    #         if 'python' in proc.info['name']:
    #             p = psutil.Process(proc.pid)
    #             #p.open_files().count()
    #             logger_method(f'SYS STAT: PID COMMAND={proc.pid}, OPEN_FILES={p.open_files()}, CMD={p.cmdline()}')
    #             logger_method(f'PID STAT: PID CHILDREN={proc.pid}, CHILDREN={p.children(recursive=True)}')

    def get_disk_usage_pct(self, data_dir="/opt/qetl/users"):
        return psutil.disk_usage(data_dir).percent

    def get_disk_size_total_in_mb(self, data_dir="/opt/qetl/users"):
        return int(psutil.disk_usage(data_dir).total / 1024 / 1024)

    def get_disk_size_usage_in_mb(self, data_dir="/opt/qetl/users"):
        return int(psutil.disk_usage(data_dir).used / 1024 / 1024)

    def get_disk_size_available_in_mb(self, data_dir="/opt/qetl/users"):
        total_disk_space = psutil.disk_usage(data_dir).total / 1024 / 1024
        used_disk_space = psutil.disk_usage(data_dir).used / 1024 / 1024
        available_disk_space = total_disk_space - used_disk_space
        return int(available_disk_space)

    def get_cpu_usage_pct(self):
        return psutil.cpu_percent(interval=0.5)

    def get_cpu_frequency(self):
        return int(psutil.cpu_freq().current)

    def get_cpu_count(self):
        return int(psutil.cpu_count())

    def get_ram_size_usage_in_mb(self):
        return int(psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024

    def get_ram_size_total_in_mb(self):
        return int(psutil.virtual_memory().total) / 1024 / 1024

    def get_ram_usage_pct(self):
        return psutil.virtual_memory().percent

    def get_ram_size_available_in_mb(self):
        return int(psutil.virtual_memory().available) / 1024 / 1034

    def get_swap_size_usage_in_mb(self):
        return int(psutil.swap_memory().used) / 1024 / 1024

    def get_swap_size_total_in_mb(self):
        return int(psutil.swap_memory().total) / 1024 / 1024

    def get_swap_size_available_in_mb(self):
        total_swap_space = psutil.swap_memory().total / 1024 / 1024
        used_swap_space = psutil.swap_memory().used / 1024 / 1024
        available_swap_space = total_swap_space - used_swap_space
        return int(available_swap_space)

    def get_swap_usage_pct(self):
        return psutil.swap_memory().percent

class DisplayCounterToLog:

    def __init__(self, display_counter_at=10000, logger_func=None, display_counter_log_message="count"):
        self.counter = 0
        self.display_counter = 0
        self.batch_name = ''
        self.batch_number = 0
        self.batch_date = ''
        self.status_table_name = 'TABLE_NAME'
        self.status_name_column = 'TABLE_NAME_LOAD_STATUS'
        self.display_counter_at = display_counter_at
        self.logger_func = logger_func
        self.display_counter_log_message = display_counter_log_message

    def update_counter(self):
        self.counter += 1
        self.display_counter += 1

    def get_counter(self):
        return self.counter

    def get_batch_name(self):
        return self.batch_name

    def set_batch_name(self, batch_name):
        self.batch_name = batch_name

    def get_batch_number(self):
        return self.batch_number

    def get_batch_date(self):
        return self.batch_date

    def set_batch_date(self, batch_date):
        self.batch_date = batch_date

    def get_status_table_name(self):
        return self.status_table_name

    def get_status_name_column(self):
        return self.status_name_column

    def update_batch_info(self, batch_name, batch_number, batch_date, status_table_name, status_name_column):
        self.batch_name = batch_name
        self.batch_number = batch_number
        self.batch_date = batch_date
        self.status_table_name = status_table_name
        self.status_name_column = status_name_column

    def get_batch_info(self):
        return {
            'batch_name': self.batch_name,
            'batch_number': self.batch_number,
            'batch_date': self.batch_date,
            'etl_workflow_status_table_name': self.status_table_name,
            'status_name_column': self.status_name_column
        }

    def display_counter_to_log(self):
        self.update_counter()
        if self.display_counter >= self.display_counter_at:
            self.display_counter = 0
            if self.logger_func is None:
                print(f"{self.display_counter_log_message}: {self.counter:,}")
            else:
                self.logger_func(f"{self.display_counter_log_message}: {self.counter:,}")

    def display_final_counter_to_log(self):
        if self.logger_func is None:
            print(f"{self.display_counter_log_message} - Total: {self.counter:,}")
        else:
            self.logger_func(f"{self.display_counter_log_message} - Total: {self.counter:,}")


def test_obj(etld_lib_functions):
    try:
        this_prog = Path(__file__).name
        etld_lib_functions.logger.info(f"Begin testing {this_prog}")
        database_type = "DATABASE NAME"
        table_name = "TABLE NAME"
        counter_obj = DisplayCounterToLog(
            display_counter_at=5,
            logger_func=etld_lib_functions.logger.info,
            display_counter_log_message=f"rows added/updated into {database_type} "
                                        f"table {table_name}")
        counter_obj.display_counter_to_log()
        counter_obj.display_counter_to_log()
        counter_obj.display_counter_to_log()
        counter_obj.display_counter_to_log()
        counter_obj.display_counter_to_log()
        counter_obj.display_final_counter_to_log()
        etld_lib_functions.logger.info(f"End   testing {this_prog}")
    except Exception as e:
        print("Problem setting up logging.  Investigate error and rerun.")
        exit(1)


if __name__ == '__main__':
    this_prog = Path(__file__).name
    etld_lib_functions = StartLoggingToStdout(my_logger_prog_name=f"{this_prog}")


