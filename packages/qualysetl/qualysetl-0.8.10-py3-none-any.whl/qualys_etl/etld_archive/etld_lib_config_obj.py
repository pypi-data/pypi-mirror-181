from pathlib import Path
import os
import oschmod
import gzip
import re
import yaml
import resource
from qualys_etl.etld_lib import etld_lib_datetime
from qualys_etl.etld_archive import etld_lib_functions_obj


class EtldLibConfigObj:

    def __init__(self, etld_lib_functions):
        self.qetl_code_dir = etld_lib_functions.qetl_code_dir
        self.qetl_code_dir_child = etld_lib_functions.qetl_code_dir_child
        self.etld_lib_functions = None
        self.qetl_create_user_dirs_ok_flag = False      # Automatically create unknown user directories default - False
        self.qetl_manage_user_selected_datetime = None  # Initialize qetl_manage_user datetime to None
        self.system_usage_counters = []                 # Initialize system usage counters dictionary

    def prepare_extract_batch_file_name(self, next_batch_number_str='batch_000001',
                                        next_batch_date='1970-01-01T00:00:00Z',
                                        extract_dir=None,
                                        file_name_type="host_list_detection",
                                        file_name_option="vm_processed_after",
                                        file_name_option_date='1970-01-01T00:00:00Z',
                                        file_extension="xml",
                                        compression_method=open):

        next_batch_number = int(next_batch_number_str.split("_")[1])
        next_file_name = f"{file_name_type}" \
                         f"_utc_run_datetime_" \
                         f"{next_batch_date}" \
                         f"_utc_" \
                         f"{file_name_option}" \
                         f"_" \
                         f"{file_name_option_date}" \
                         f"_" \
                         f"{next_batch_number_str}.{file_extension}"
        if compression_method == gzip.open:
            next_file_name = next_file_name + ".gz"
        next_file_path = Path(extract_dir, next_file_name)
        return {
                'next_batch_number': next_batch_number,
                'next_batch_number_str': next_batch_number_str,
                'next_file_name': next_file_name,
                'next_file_path': next_file_path
                }


    def create_directory(self, dir_path=None):
        if dir_path is not None:
            os.makedirs(dir_path, exist_ok=True)
            oschmod.set_mode(dir_path, "a+rwx,g-rwx,o-rwx")


    def remove_old_files(self, dir_path=None,
                         dir_search_glob=None,
                         other_files_list: list = [],
                         other_files_list_exclusions: list = []):
        if dir_path is None or dir_search_glob is None:
            return True

        if Path(dir_path).is_dir() is not True:
            self.create_directory(dir_path)

        if Path(dir_path).is_dir():
            file_list = list(Path(dir_path).glob(dir_search_glob))
            count_files = len(file_list)
            etld_lib_functions.logger.info(f"Removing {count_files} old files from dir: {dir_path}")
            try:
                for file_name in file_list:
                    if Path(file_name).is_file():
                        etld_lib_functions.logger.info(f"Removing old file: {str(file_name)}")
                        Path(file_name).unlink()
            except OSError as e:
                etld_lib_functions.logger.error(f"{e}")
                exit(1)
        try:
            for file_name in other_files_list:
                if file_name in other_files_list_exclusions:
                    pass
                else:
                    if Path(file_name).is_file():
                        etld_lib_functions.logger.info(f"Removing old file: {str(file_name)}")
                        Path(file_name).unlink()

        except Exception as e:
            etld_lib_functions.logger.error(f"{e}")
            exit(1)


    def get_attribute_from_config_settings(self, key, default_value):
        if key in self.etld_lib_config_settings_yaml_dict.keys():
            return self.etld_lib_config_settings_yaml_dict.get(key)
        else:
            return default_value

    def get_open_file_compression_method_from_config_settings(self, key):
        compression_method = gzip.open
        return compression_method

    def set_api_payload(self, payload_default: dict, payload_option_from_config):
        payload_option = self.get_attribute_from_config_settings(payload_option_from_config, 'default')
        if isinstance(payload_option, dict):
            payload = self.get_attribute_from_config_settings(payload_option_from_config, {})
            for key in payload_default:
                if key not in payload.keys():
                    payload[key] = payload_default[key]
        else:
            payload = payload_default
        return payload

    def setup_qualys_etl_user_home_env_variables(self):
        if os.environ.keys().__contains__("qualys_etl_user_home") is not True:
            # qetl_all_users_dir = Path(Path.home(), 'opt', 'qetl', 'users')
            # qetl_user_root_dir = Path(Path.home(), 'opt', 'qetl', 'users', 'default_user')
            # qetl_user_home_dir = Path(qetl_user_root_dir, 'qetl_home')
            # Entry is now qetl_manage_user.  If qualys_etl_user_home env is not set, then abort.
            try:
                etld_lib_functions.logger.error(f"Error, no qualys_etl_user_home.")
                etld_lib_functions.logger.error(f"Ensure you are running qetl_manage_user to run your job")
                etld_lib_functions.logger.error(f"see qetl_manage_user -h for options.")
                exit(1)
            except AttributeError as e:
                print(f"Error, no qualys_etl_user_home.")
                print(f"Ensure you are using opt/qetl/users as part of your path")
                print(f"see qetl_manage_user -h for options.")
                print(f"Exception {e}")
                exit(1)
        else:
            self.qualys_etl_user_home_env_var = Path(os.environ.get("qualys_etl_user_home"))
            # Strip qetl_home if the user accidentally added it.
            self.qualys_etl_user_home_env_var = \
                Path(re.sub("/qetl_home.*$", "", str(self.qualys_etl_user_home_env_var)))
            # Ensure prefix is opt/qetl/users
            if self.qualys_etl_user_home_env_var.parent.name == 'users' and \
                    self.qualys_etl_user_home_env_var.parent.parent.name == 'qetl' and \
                    self.qualys_etl_user_home_env_var.parent.parent.parent.name == 'opt':
                # Valid directory ${USER DIR}/opt/qetl/users/{QualysUser}/qetl_home
                self.qetl_all_users_dir = self.qualys_etl_user_home_env_var.parent
                self.qetl_user_root_dir = self.qualys_etl_user_home_env_var
                self.qetl_user_home_dir = Path(self.qualys_etl_user_home_env_var, 'qetl_home')
            else:
                # User directory not set correctly to include opt/qetl/users, abort
                try:
                    etld_lib_functions.logger.error(f"error setting user home directory: {self.qualys_etl_user_home_env_var}")
                    etld_lib_functions.logger.error(f"Ensure you are using opt/qetl/users as part of your path")
                    etld_lib_functions.logger.error(f"see qetl_manage_user -h for options.")
                    exit(1)
                except AttributeError as e:
                    print(f"error setting user home directory: {self.qualys_etl_user_home_env_var}")
                    print(f"Ensure you are using opt/qetl/users as part of your path")
                    print(f"see qetl_manage_user -h for options.")
                    print(f"Exception {e}")
                    exit(1)

        self.qetl_user_data_dir = Path(self.qetl_user_home_dir, "data")
        self.qetl_user_log_dir = Path(self.qetl_user_home_dir, "log")
        self.qetl_user_config_dir = Path(self.qetl_user_home_dir, "config")
        self.qetl_user_cred_dir = Path(self.qetl_user_home_dir, "cred")
        self.qetl_user_bin_dir = Path(self.qetl_user_home_dir, "bin")
        self.validate_char_qetl_user_home_dir(self.qetl_user_home_dir)

    def set_path_qetl_user_home_dir(self):
        self.setup_qualys_etl_user_home_env_variables()
        self.setup_kb_vars()
        self.setup_host_list_vars()
        self.setup_host_list_detection_vars()
        self.setup_asset_inventory_vars()
        self.setup_was_vars()
        self.setup_test_system_vars()


    def create_user_data_dirs(self):
        # global qetl_create_user_dirs_ok_flag  # False.  Set to true by qetl_manage_user
        if self.qetl_create_user_dirs_ok_flag is True:
            try:
                os.makedirs(self.qetl_user_home_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_home_dir, "a+rwx,g-rwx,o-rwx")
                os.makedirs(self.qetl_user_data_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_data_dir, "a+rwx,g-rwx,o-rwx")
                os.makedirs(self.qetl_user_log_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_log_dir, "a+rwx,g-rwx,o-rwx")
                os.makedirs(self.qetl_user_config_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_config_dir, "a+rwx,g-rwx,o-rwx")
                os.makedirs(self.qetl_user_cred_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_cred_dir, "a+rwx,g-rwx,o-rwx")
                os.makedirs(self.qetl_user_bin_dir, exist_ok=True)
                oschmod.set_mode(self.qetl_user_bin_dir, "a+rwx,g-rwx,o-rwx")
            except Exception as e:
                etld_lib_functions.logger.error(
                    f"error creating qetl home directories.  check permissions on "
                    f"{str(self.qetl_user_home_dir.parent.parent)}")
                etld_lib_functions.logger.error(
                    f"determine if permissions on file allow creating directories "
                    f"{str(self.qetl_user_home_dir.parent.parent)}")
                etld_lib_functions.logger.error(f"Exception: {e}")
                exit(1)

        elif Path(self.qetl_user_home_dir).is_dir() and \
            Path(self.qetl_user_log_dir).is_dir() and \
                Path(self.qetl_user_config_dir).is_dir() and \
                Path(self.qetl_user_cred_dir).is_dir() and \
                Path(self.qetl_user_bin_dir).is_dir() and \
                Path(self.qetl_user_data_dir).is_dir():
            pass
        else:
            try:
                etld_lib_functions.logger.error(
                    f"error with qetl home directories. "
                    f" Check {str(self.qetl_user_home_dir)} for data,config,log,bin,cred directories exist.")
                etld_lib_functions.logger.error(
                    f"Use qetl_manage_user -h to create your qetl "
                    f"user home directories if they don't exists.")
                exit(1)
            except AttributeError as ae:
                print(f"error with qetl home directories. "
                      f" Check {str(self.qetl_user_home_dir)} for data,config,log,bin,cred directories exist.")
                print(f"Use qetl_manage_user -h to create your qetl user home directories if they don't exists.")
                print(f"Exception {ae}")
                exit(1)

    def validate_char_qetl_user_home_dir(self, p: Path):
        p_match = re.fullmatch(r"[_A-Za-z0-9/]+", str(p))
        if etld_lib_functions.logging_is_on_flag is False:
            logging_method = print
        else:
            logging_method = etld_lib_functions.logger.error

        if p_match is None:
            logging_method(f"see qetl_manage_user -h, malformed parent directory: {p}")
            logging_method(f" Characters other than [_A-Za-z0-9/]+ found: {str(p)}")
            exit(1)
        if p.name != 'qetl_home':
            logging_method(f"see qetl_manage_user -h, malformed parent directory: {p}")
            logging_method(f" qetl_home not found: {str(p)}")
            exit(1)
        if p.parent.parent.name != 'users':
            logging_method(f"see qetl_manage_user -h, malformed parent directory: {p}")
            logging_method(f" users not found in parent: {str(p)}")
            exit(1)
        if p.parent.parent.parent.name != 'qetl':
            logging_method(f"see qetl_manage_user -h, malformed parent directory: {p}")
            logging_method(f" qetl not found in parent: {str(p)}")
            exit(1)
        if p.parent.parent.parent.parent.name != 'opt':
            logging_method(f"see qetl_manage_user -h, malformed parent directory: {p}")
            logging_method(f" opt not found in parent: {str(p)}")
            exit(1)

    # DATA ENVIRONMENT AND DIRECTORIES
    #
    # Data Directory Structures and contents are:
    #  - qetl_user_home_dir
    #  - qetl_user_home_dir/qetl_home/data - All XML, JSON, CSV, SQLITE Data
    #  - qetl_user_home_dir/qetl_home/log  - Optional Logs Location
    #  - qetl_user_home_dir/qetl_home/config - date configurations for knowledgebase, host list and host list detection
    #  - qetl_user_home_dir/qetl_home/cred   - Qualys Credentials Directory, ensure this is secure.
    #  - qetl_user_home_dir/qetl_home/bin    - Initial Canned Scripts for Qualys API User



    def load_etld_lib_config_settings_yaml(self):
    # Create Default YAML if it doesn't exist.
        self.qetl_user_config_settings_yaml_file = Path(self.qetl_user_config_dir, "etld_config_settings.yaml")
        if not Path.is_file(self.qetl_user_config_settings_yaml_file):  # api_home/cred/etld_config_settings.yaml
            etld_lib_config_template = \
                Path(self.qetl_code_dir, "qualys_etl", "etld_templates", "etld_config_settings.yaml")
            # Get Template
            with open(str(etld_lib_config_template), "r", encoding='utf-8') as etld_lib_config_template_f:
                etld_lib_config_template_string = etld_lib_config_template_f.read()

            # Write etld_lib_config_template_string to users directory.
            with open(self.qetl_user_config_settings_yaml_file, 'w', encoding='utf-8') as acf:
                local_date = etld_lib_datetime.get_local_date()  # Add date updated to file
                etld_lib_config_template_string = re.sub('\$DATE', local_date, etld_lib_config_template_string)
                acf.write(etld_lib_config_template_string)

        oschmod.set_mode(str(self.qetl_user_config_settings_yaml_file), "u+rw,u-x,go-rwx")
    # Read YAML into global etld_lib_config_settings_yaml_dict
        try:
            with open(self.qetl_user_config_settings_yaml_file, 'r', encoding='utf-8') as etld_lib_config_yaml_file:
                self.etld_lib_config_settings_yaml_dict = yaml.safe_load(etld_lib_config_yaml_file)
                for key in self.etld_lib_config_settings_yaml_dict.keys():
                    etld_lib_functions.logger.info(
                        f"etld_config_settings.yaml - {key}: {self.etld_lib_config_settings_yaml_dict.get(key)} ")
        except Exception as e:
            etld_lib_functions.logger.error(f"etld_config_settings.yaml Exception: {e}")
            exit(1)


    def setup_test_system_vars(self):
        self.test_system_log_file = Path(self.qetl_user_log_dir, "test_system.log")
        self.test_system_lock_file = Path(self.qetl_user_log_dir, ".test_system.lock")
        self.test_system_log_rotate_file = Path(self.qetl_user_log_dir, "test_system.1.log")


    def get_kb_user_config(self):
        def set_kb_last_modified_after():
            # global kb_last_modified_after
            self.kb_last_modified_after = self.get_attribute_from_config_settings('kb_last_modified_after', 'default')
            if self.qetl_manage_user_selected_datetime is not None:
                self.kb_last_modified_after = self.qetl_manage_user_selected_datetime
                etld_lib_functions.logger.info(f"kb_last_modified_after set by qetl_manage_user "
                                               f"-d option - {self.kb_last_modified_after}")
            elif self.kb_last_modified_after == 'default':
                # kb_last_modified_after = etld_lib_datetime.get_utc_date_minus_days(7)
                # Keep default so knowledgebase_04_extract can set the date to max_date found in database.
                pass
            else:
                etld_lib_functions.logger.info(f"kb_last_modified_after yaml - {self.kb_last_modified_after}")

            if self.kb_last_modified_after == 'default':
                pass
            elif etld_lib_datetime.is_valid_qualys_datetime_format(self.kb_last_modified_after) is False:
                etld_lib_functions.logger.error(f"kb_last_modified_after date is not in correct form "
                                                f"(YYYY-MM-DDThh:mm:ssZ) date is {self.kb_last_modified_after}")

        self.kb_payload_option = \
            {'action': 'list', 'details': 'All', 'show_disabled_flag': '1', 'show_qid_change_log': '1',
             'show_supported_modules_info': '1', 'show_pci_reasons': '1'}

        self.kb_extract_dir = Path(self.kb_data_dir, "knowledgebase_extract_dir")
        self.kb_extract_dir_file_search_blob = 'kb_utc*'
        self.kb_export_dir = self.get_attribute_from_config_settings('kb_export_dir', 'default')
        set_kb_last_modified_after()
        self.kb_csv_truncate_cell_limit = 0  # get_attribute_from_config_settings('kb_csv_truncate_cell_limit', 0)
        self.kb_present_csv_cell_as_json = self.get_attribute_from_config_settings('kb_present_csv_cell_as_json', True)
        self.kb_truncation_limit = \
            self.get_attribute_from_config_settings('kb_truncation_limit', '0')
        self.kb_chunk_size_calc = int(self.get_attribute_from_config_settings('kb_chunk_size_calc', '20480'))
        self.kb_try_extract_max_count = int(self.get_attribute_from_config_settings('kb_try_extract_max_count', '30'))
        self.kb_http_conn_timeout = int(self.get_attribute_from_config_settings('kb_http_conn_timeout', '900'))
        self.kb_open_file_compression_method = \
            self.get_open_file_compression_method_from_config_settings('kb_open_file_compression_method')

        etld_lib_functions.logger.info(f"knowledgeBase config - {self.qetl_user_config_settings_yaml_file}")
        etld_lib_functions.logger.info(f"kb_export_dir yaml   - {self.kb_export_dir}")


    def setup_kb_vars(self):
        self.kb_data_dir = self.qetl_user_data_dir
        self.kb_bin_dir = self.qetl_user_bin_dir
        self.kb_xml_file = Path(self.kb_data_dir, "kb.xml")
        self.kb_shelve_file = Path(self.kb_data_dir, "kb_shelve")
        self.kb_sqlite_file = Path(self.kb_data_dir, "kb_sqlite.db")
        self.kb_cve_qid_file = Path(self.kb_data_dir, "kb_cve_qid_map.csv")
        self.kb_cve_qid_map_shelve = Path(self.kb_data_dir, "kb_cve_qid_map_shelve")
        self.kb_csv_file = Path(self.kb_data_dir, "kb.csv")
        self.kb_json_file = Path(self.kb_data_dir, "kb.json")
        self.kb_log_file = Path(self.qetl_user_log_dir, "kb.log")
        self.kb_log_table_name = 'Q_KnowledgeBase_RUN_LOG'
        self.kb_lock_file = Path(self.qetl_user_log_dir, ".kb.lock")
        self.kb_log_rotate_file = Path(self.qetl_user_log_dir, "kb.1.log")
        self.kb_table_name = 'Q_KnowledgeBase'
        self.kb_table_name_cve_list_view = 'Q_KnowledgeBase_CVE_LIST'
        self.kb_table_name_merge_new_data = 'Q_KnowledgeBase_Merge_New_Data'
        self.kb_status_table_name = 'Q_KnowledgeBase_Status'
        self.kb_data_files = [self.kb_xml_file, self.kb_shelve_file, self.kb_sqlite_file,
                              self.kb_cve_qid_file, self.kb_cve_qid_map_shelve, self.kb_csv_file,
                              self.kb_json_file]


    def get_host_list_user_config(self):
        # global host_list_data_dir
        # global host_list_export_dir
        # global qetl_user_config_settings_yaml_file
        # global host_list_vm_processed_after
        # global host_list_payload_option
        # global qetl_manage_user_selected_datetime
        # global host_list_csv_truncate_cell_limit
        # global host_list_sqlite_file
        # global host_list_present_csv_cell_as_json
        # global host_list_xml_to_sqlite_via_multiprocessing
        # global host_list_chunk_size_calc
        # global host_list_try_extract_max_count
        # global host_list_http_conn_timeout
        # global host_list_api_payload
        # global host_list_open_file_compression_method
        # global host_list_test_system_flag
        # global host_list_test_number_of_files_to_extract

        def set_host_list_vm_processed_after():
            # global host_list_vm_processed_after
            self.host_list_vm_processed_after = self.get_attribute_from_config_settings('host_list_vm_processed_after', 'default')
            if self.qetl_manage_user_selected_datetime is not None:
                self.host_list_vm_processed_after = self.qetl_manage_user_selected_datetime
                etld_lib_functions.logger.info(f"host_list_vm_processed_after set by qetl_manage_user -d option - "
                                               f"{self.host_list_vm_processed_after}")
            elif self.host_list_vm_processed_after == 'default':
                self.host_list_vm_processed_after = etld_lib_datetime.get_utc_date_minus_days(7)
            else:
                etld_lib_functions.logger.info(f"host_list_vm_processed_after yaml - {self.host_list_vm_processed_after}")

            if not etld_lib_datetime.is_valid_qualys_datetime_format(self.host_list_vm_processed_after):
                etld_lib_functions.logger.error(
                    f"Format Error host_list_vm_processed_after: {self.host_list_vm_processed_after} ")
                exit(1)

            if str(self.host_list_vm_processed_after).__contains__("1970"):  # Don't add date to process all data.
                return {}
            else:
                return {'vm_processed_after': self.host_list_vm_processed_after}

        def set_host_list_api_payload():
           # global host_list_api_payload
           # global host_list_payload_option

            self.host_list_payload_default = {'action': 'list', 'details': 'All',
                                              'truncation_limit': '25000', 'show_tags': '1',
                                              'show_cloud_tags': '1', 'show_asset_id': '1', 'host_metadata': 'all'}
            self.host_list_payload_option = self.get_attribute_from_config_settings('host_list_payload_option', 'default')
            self.host_list_api_payload = self.set_api_payload(self.host_list_payload_default, 'host_list_payload_option')
            self.host_list_show_tags = self.get_attribute_from_config_settings('host_list_show_tags', '1')  # Legacy support
            if self.host_list_show_tags == '0':
                self.host_list_api_payload.update({'show_tags': '0'})
            self.host_list_api_payload.update(set_host_list_vm_processed_after())

        self.host_list_data_dir = self.qetl_user_data_dir
        self.host_list_export_dir = self.get_attribute_from_config_settings('host_list_export_dir', 'default')
        self.host_list_xml_to_sqlite_via_multiprocessing = \
            self.get_attribute_from_config_settings('host_list_xml_to_sqlite_via_multiprocessing', True)
        self.host_list_csv_truncate_cell_limit = 0
        # self.get_attribute_from_config_settings('host_list_csv_truncate_cell_limit', '0')

        self.host_list_present_csv_cell_as_json = self.get_attribute_from_config_settings('host_list_present_csv_cell_as_json', True)
        self.host_list_chunk_size_calc = int(self.get_attribute_from_config_settings('host_list_chunk_size_calc', '20480'))
        self.host_list_try_extract_max_count = int(self.get_attribute_from_config_settings('host_list_try_extract_max_count', '30'))
        self.host_list_http_conn_timeout = int(self.get_attribute_from_config_settings('host_list_http_conn_timeout', '900'))
        self.host_list_open_file_compression_method = \
            self.get_open_file_compression_method_from_config_settings('host_list_open_file_compression_method')
        self.host_list_test_system_flag = \
            self.get_attribute_from_config_settings('host_list_test_system_flag', False)
        self.host_list_test_number_of_files_to_extract = \
            self.get_attribute_from_config_settings('host_list_test_number_of_files_to_extract', 2)
        set_host_list_api_payload()
        etld_lib_functions.logger.info(f"host list config - {self.qetl_user_config_settings_yaml_file}")
        etld_lib_functions.logger.info(f"host_list_export_dir - {self.host_list_export_dir}")


    def setup_host_list_vars(self):
        # global qetl_user_data_dir
        # global host_list_data_dir
        # global host_list_extract_dir
        # global host_list_extract_dir_file_search_blob
        # # TODO eliminate these variables
        # global host_list_xml_file_list
        # global host_list_other_xml_file
        # global host_list_ec2_xml_file
        # global host_list_gcp_xml_file
        # global host_list_azure_xml_file
        # global host_list_shelve_file
        #
        # global host_list_sqlite_file
        # global host_list_csv_file
        # global host_list_json_file
        # global host_list_log_file
        # global host_list_lock_file
        # global host_list_log_rotate_file
        # global host_list_table_name
        # global host_list_status_table_name
        # global host_list_data_files

        self.host_list_data_dir = self.qetl_user_data_dir
        self.host_list_extract_dir = Path(self.host_list_data_dir, "host_list_extract_dir")
        self.host_list_extract_dir_file_search_blob = 'host_list_utc*'
        self.host_list_other_xml_file = Path(self.host_list_data_dir, "host_list_other_file.xml")
        self.host_list_ec2_xml_file = Path(self.host_list_data_dir, "host_list_ec2_file.xml")
        self.host_list_gcp_xml_file = Path(self.host_list_data_dir, "host_list_gcp_file.xml")
        self.host_list_azure_xml_file = Path(self.host_list_data_dir, "host_list_azure_file.xml")
        self.host_list_xml_file_list = [self.host_list_other_xml_file, self.host_list_ec2_xml_file,
                                   self.host_list_gcp_xml_file, self.host_list_azure_xml_file]
        self.host_list_shelve_file = Path(self.host_list_data_dir, "host_list_shelve")
        self.host_list_sqlite_file = Path(self.host_list_data_dir, "host_list_sqlite.db")
        self.host_list_csv_file = Path(self.host_list_data_dir, "host_list.csv")
        self.host_list_json_file = Path(self.host_list_data_dir, "host_list.json")
        self.host_list_log_file = Path(self.qetl_user_log_dir, "host_list.log")
        self.host_list_lock_file = Path(self.qetl_user_log_dir, ".host_list.lock")
        self.host_list_log_rotate_file = Path(self.qetl_user_log_dir, "host_list.1.log")
        self.host_list_table_name = 'Q_Host_List'
        self.host_list_status_table_name = 'Q_Host_List_Status'
        self.host_list_data_files = [self.host_list_other_xml_file, self.host_list_ec2_xml_file,
                                     self.host_list_gcp_xml_file, self.host_list_azure_xml_file,
                                     self.host_list_shelve_file, self.host_list_sqlite_file,
                                     self.host_list_csv_file, self.host_list_json_file]


    def get_host_list_detection_user_config(self):
        # global host_list_detection_data_dir
        # global host_list_detection_export_dir
        # global host_list_detection_vm_processed_after
        # global host_list_detection_payload_option
        # global host_list_detection_concurrency_limit
        # global host_list_detection_multi_proc_batch_size
        # global host_list_detection_limit_hosts
        # global host_list_detection_csv_truncate_cell_limit
        # global qetl_user_config_settings_yaml_file
        # global qetl_manage_user_selected_datetime
        # global host_list_vm_processed_after
        # global host_list_detection_present_csv_cell_as_json
        # global host_list_detection_chunk_size_calc
        # global host_list_detection_try_extract_max_count
        # global host_list_detection_http_conn_timeout
        # global host_list_detection_api_payload
        # global host_list_detection_open_file_compression_method
        # global host_list_detection_xml_to_sqlite_via_multiprocessing

        def set_host_list_detection_vm_processed_after():
            # global host_list_detection_vm_processed_after
            # global host_list_vm_processed_after

            self.host_list_detection_vm_processed_after = \
                self.get_attribute_from_config_settings('host_list_detection_vm_processed_after', 'default')
            if self.qetl_manage_user_selected_datetime is not None:
                self.host_list_detection_vm_processed_after = self.qetl_manage_user_selected_datetime
                self.host_list_vm_processed_after = self.qetl_manage_user_selected_datetime
                etld_lib_functions.logger.info(f"host_list_detection_vm_processed_after and host_list_vm_processed_after "
                                               f"set by qetl_manage_user -d option")
            # FOR TESTING
            elif self.host_list_detection_vm_processed_after == 'default':
                self.host_list_detection_vm_processed_after = etld_lib_datetime.get_utc_date_minus_days(1)

            if not etld_lib_datetime.is_valid_qualys_datetime_format(self.host_list_detection_vm_processed_after):
                etld_lib_functions.logger.error(f"Format Error host_list_detection_vm_processed_after: "
                                                f"{self.host_list_detection_vm_processed_after} ")
                exit(1)

            etld_lib_functions.logger.info(f"host_list_vm_processed_after: {self.host_list_detection_vm_processed_after}")
            etld_lib_functions.logger.info(
                f"host_list_detection_vm_processed_after: {self.host_list_detection_vm_processed_after}")

            if str(self.host_list_detection_vm_processed_after).__contains__("1970"):  # Don't add date to process all data.
                return {}
            else:
                return {'vm_processed_after': self.host_list_detection_vm_processed_after}

        def set_host_detection_list_api_payload():
            # global host_list_detection_api_payload
            # global host_list_detection_payload_option
            # global host_list_detection_multi_proc_batch_size
            # global host_list_detection_limit_hosts

            self.host_list_detection_payload_default = \
                {'action': 'list', 'show_asset_id': '1', 'show_reopened_info': '1', 'show_tags': '0', 'show_results': '1',
                 'show_igs': '1', 'status': 'Active,New,Re-Opened,Fixed', 'arf_kernel_filter': '1',
                 'arf_service_filter': '0', 'arf_config_filter': '0', 'include_ignored': '1', 'include_disabled': '1',
                 'truncation_limit': '0'}

            self.host_list_detection_payload_option = self.get_attribute_from_config_settings('host_list_detection_payload_option',
                                                                                    'default')
            self.host_list_detection_api_payload = self.set_api_payload(self.host_list_detection_payload_default,
                                                              'host_list_detection_payload_option')
            self.host_list_detection_discarded_vm_processed_after_date = set_host_list_detection_vm_processed_after()

            self.host_list_detection_multi_proc_batch_size = \
                self.get_attribute_from_config_settings('host_list_detection_multi_proc_batch_size', '1000')

            if int(self.host_list_detection_multi_proc_batch_size) > 2000:
                etld_lib_functions.logger.info(f"reset batch_size_max to 2000.")
                etld_lib_functions.logger.info(
                    f" user select batch_size_max was {self.host_list_detection_multi_proc_batch_size}.")
                self.host_list_detection_multi_proc_batch_size = 2000
            elif int(self.host_list_detection_multi_proc_batch_size) > 100:
                etld_lib_functions.logger.info(f"reset batch_size_max to {self.host_list_detection_multi_proc_batch_size}.")
                etld_lib_functions.logger.info(
                    f" user select batch_size_max is {self.host_list_detection_multi_proc_batch_size}.")
                self.host_list_detection_multi_proc_batch_size = int(self.host_list_detection_multi_proc_batch_size)
            else:
                etld_lib_functions.logger.info(f"reset batch_size_max to 100.")
                etld_lib_functions.logger.info(f" user select batch_size_max is "
                                               f"{self.host_list_detection_multi_proc_batch_size},"
                                               f"but is not within range. 100 - 2000.  Reset to 100")
                self.host_list_detection_multi_proc_batch_size = 100

            self.host_list_detection_limit_hosts = \
                self.get_attribute_from_config_settings('host_list_detection_limit_hosts', '0')

        self.host_list_detection_data_dir = self.qetl_user_data_dir
        self.host_list_detection_export_dir = \
            self.get_attribute_from_config_settings('host_list_detection_export_dir', 'default')
        self.host_list_detection_csv_truncate_cell_limit = '0'
        # get_attribute_from_config_settings('host_list_detection_csv_truncate_cell_limit', '0')

        self.host_list_detection_payload_option = self.get_attribute_from_config_settings('host_list_detection_payload_option', '')
        self.host_list_detection_concurrency_limit = \
            self.get_attribute_from_config_settings('host_list_detection_concurrency_limit', '2')
        self.host_list_detection_present_csv_cell_as_json = \
            self.get_attribute_from_config_settings('host_list_detection_present_csv_cell_as_json', True)
        self.host_list_detection_xml_to_sqlite_via_multiprocessing = \
            self.get_attribute_from_config_settings('host_list_xml_to_sqlite_via_multiprocessing', True)
        self.host_list_detection_payload_option = \
            self.get_attribute_from_config_settings('host_list_detection_payload_option', 'notags')
        self.host_list_detection_chunk_size_calc = \
            int(self.get_attribute_from_config_settings('host_list_detection_chunk_size_calc', '20480'))
        self.host_list_detection_try_extract_max_count = \
            int(self.get_attribute_from_config_settings('host_list_detection_try_extract_max_count', '30'))
        self.host_list_detection_http_conn_timeout = \
            int(self.get_attribute_from_config_settings('host_list_detection_http_conn_timeout', '900'))
        self.host_list_detection_open_file_compression_method = \
            self.get_open_file_compression_method_from_config_settings('host_list_detection_open_file_compression_method')

        set_host_detection_list_api_payload()

        etld_lib_functions.logger.info(f"host list detection config - {self.qetl_user_config_settings_yaml_file}")
        etld_lib_functions.logger.info(f"host_list_detection_export_dir - {self.host_list_detection_export_dir}")
        etld_lib_functions.logger.info(f"host_list_detection_concurrency_limit - {self.host_list_detection_concurrency_limit}")
        etld_lib_functions.logger.info(f"host_list_detection_multi_proc_batch_size - "
                                       f"{self.host_list_detection_multi_proc_batch_size}")
        etld_lib_functions.logger.info(f"host_list_api_payload - {self.host_list_api_payload}")
        etld_lib_functions.logger.info(f"host_list_detection_api_payload - {self.host_list_detection_api_payload}")


    def setup_host_list_detection_vars(self):
        # global qetl_user_data_dir
        # global host_list_detection_data_dir
        # global host_list_detection_xml_file
        # global host_list_detection_extract_dir
        # global host_list_detection_extract_dir_file_search_blob
        # global host_list_detection_shelve_file
        # global host_list_detection_sqlite_file
        # global host_list_detection_csv_file
        # global host_list_detection_csv_truncate_cell_limit
        # global host_list_detection_json_file
        # global host_list_detection_log_file
        # global host_list_detection_lock_file
        # global host_list_detection_log_rotate_file
        # global host_list_detection_table_view_name
        # global host_list_detection_status_table_name
        # global host_list_detection_hosts_table_name
        # global host_list_detection_q_knowledgebase_in_host_list_detection
        # global host_list_detection_qids_table_name
        # global host_list_detection_data_files

        self.host_list_detection_data_dir = Path(self.qetl_user_data_dir)
        self.host_list_detection_extract_dir = Path(self.host_list_detection_data_dir, "host_list_detection_extract_dir")
        self.host_list_detection_extract_dir_file_search_blob = "host_list_detection_utc*"
        self.host_list_detection_shelve_file = Path(self.host_list_detection_data_dir, "host_list_detection_shelve")
        self.host_list_detection_sqlite_file = Path(self.host_list_detection_data_dir, "host_list_detection_sqlite.db")
        self.host_list_detection_csv_file = Path(self.host_list_detection_data_dir, "host_list_detection.csv")
        self.host_list_detection_json_file = Path(self.host_list_detection_data_dir, "host_list_detection.json")
        self.host_list_detection_log_file = Path(self.qetl_user_log_dir, "host_list_detection.log")
        self.host_list_detection_lock_file = Path(self.qetl_user_log_dir, ".host_list_detection.lock")
        self.host_list_detection_log_rotate_file = Path(self.qetl_user_log_dir, "host_list_detection.1.log")
        self.host_list_detection_table_view_name = 'Q_Host_List_Detection'
        self.host_list_detection_status_table_name = 'Q_Host_List_Detection_Status'
        self.host_list_detection_hosts_table_name = 'Q_Host_List_Detection_HOSTS'
        self.host_list_detection_qids_table_name = 'Q_Host_List_Detection_QIDS'
        self.host_list_detection_q_knowledgebase_in_host_list_detection = 'Q_KnowledgeBase_In_Host_List_Detection'
        self.host_list_detection_data_files = [self.host_list_detection_shelve_file,
                                               self.host_list_detection_sqlite_file,
                                               self.host_list_detection_csv_file,
                                               self.host_list_detection_json_file]


    def get_asset_inventory_user_config(self):
        # global asset_inventory_data_dir
        # global asset_inventory_export_dir
        # global asset_inventory_asset_last_updated
        # global asset_inventory_payload_option
        # global asset_inventory_concurrency_limit
        # global asset_inventory_multi_proc_batch_size
        # global asset_inventory_limit_hosts
        # global asset_inventory_present_csv_cell_as_json
        # global asset_inventory_csv_truncate_cell_limit
        # global qetl_user_config_settings_yaml_file
        # global qetl_manage_user_selected_datetime
        # global asset_inventory_json_to_sqlite_via_multiprocessing
        # global asset_inventory_chunk_size_calc
        # global asset_inventory_try_extract_max_count
        # global asset_inventory_http_conn_timeout
        # global asset_inventory_open_file_compression_method
        # global asset_inventory_test_system_flag
        # global asset_inventory_test_number_of_files_to_extract
        # global asset_inventory_last_seen_asset_id_for_restart

        def set_asset_inventory_last_updated():
            # global asset_inventory_asset_last_updated
            if self.qetl_manage_user_selected_datetime is not None:
                self.asset_inventory_asset_last_updated = self.qetl_manage_user_selected_datetime
                etld_lib_functions.logger.info(f"asset_inventory_asset_last_updated set by qetl_manage_user -d option")
            elif self.asset_inventory_asset_last_updated == 'default':
                self.asset_inventory_asset_last_updated = etld_lib_datetime.get_utc_date_minus_days(1)
                etld_lib_functions.logger.info(f"asset_inventory_asset_last_updated default set to utc.now minus 1 days")

            etld_lib_functions.logger.info(f"asset_inventory_asset_last_updated - "
                                           f"{self.asset_inventory_asset_last_updated}")

        self.asset_inventory_data_dir = self.qetl_user_data_dir
        self.asset_inventory_export_dir = \
            self.get_attribute_from_config_settings('asset_inventory_export_dir', 'default')
        self.asset_inventory_csv_truncate_cell_limit = '0'
        # self.get_attribute_from_config_settings('asset_inventory_csv_truncate_cell_limit', '0')
        self.asset_inventory_asset_last_updated = \
            self.get_attribute_from_config_settings('asset_inventory_asset_last_updated', 'default')
        self.asset_inventory_payload_option = self.get_attribute_from_config_settings('asset_inventory_payload_option', '')
        self.asset_inventory_concurrency_limit = self.get_attribute_from_config_settings('asset_inventory_concurrency_limit', '2')
        self.asset_inventory_multi_proc_batch_size = \
            self.get_attribute_from_config_settings('asset_inventory_multi_proc_batch_size', '300')
        self.asset_inventory_limit_hosts = \
            self.get_attribute_from_config_settings('asset_inventory_limit_hosts', '300')
        self.asset_inventory_json_to_sqlite_via_multiprocessing = \
            self.get_attribute_from_config_settings('asset_inventory_json_to_sqlite_via_multiprocessing', True)
        self.asset_inventory_present_csv_cell_as_json = \
            self.get_attribute_from_config_settings('asset_inventory_present_csv_cell_as_json', True)
        self.asset_inventory_chunk_size_calc = \
            int(self.get_attribute_from_config_settings('asset_inventory_chunk_size_calc', '20480'))
        self.asset_inventory_try_extract_max_count = \
            int(self.get_attribute_from_config_settings('asset_inventory_try_extract_max_count', '30'))
        self.asset_inventory_http_conn_timeout = \
            int(self.get_attribute_from_config_settings('asset_inventory_http_conn_timeout', '900'))
        self.asset_inventory_open_file_compression_method = \
            self.get_open_file_compression_method_from_config_settings('asset_inventory_open_file_compression_method')
        self.asset_inventory_test_system_flag = self.get_attribute_from_config_settings('asset_inventory_test_system_flag', False)
        self.asset_inventory_test_number_of_files_to_extract = \
            self.get_attribute_from_config_settings('asset_inventory_test_number_of_files_to_extract', 3)
        self.asset_inventory_last_seen_asset_id_for_restart = \
            self.get_attribute_from_config_settings('asset_inventory_last_seen_asset_id_for_restart', 0)
        set_asset_inventory_last_updated()

        etld_lib_functions.logger.info(f"asset inventory config - {self.qetl_user_config_settings_yaml_file}")
        etld_lib_functions.logger.info(f"asset_inventory_export_dir yaml - {self.asset_inventory_export_dir}")
        etld_lib_functions.logger.info(f"asset_inventory_extract_dir yaml - {self.asset_inventory_extract_dir}")
        etld_lib_functions.logger.info(f"asset_inventory_concurrency_limit yaml - {self.asset_inventory_concurrency_limit}")
        etld_lib_functions.logger.info(
            f"asset_inventory_multi_proc_batch_size yaml - {self.asset_inventory_multi_proc_batch_size}")
        etld_lib_functions.logger.info(
            f"asset_inventory_csv_truncate_cell_limit set to zero by program.")


    def setup_asset_inventory_vars(self):
        # global qetl_user_data_dir
        # global asset_inventory_data_dir
        # global asset_inventory_json_batch_file
        # global asset_inventory_extract_dir
        # global asset_inventory_extract_dir_file_search_blob
        # global asset_inventory_extract_dir_file_search_blob_two
        # global asset_inventory_shelve_file
        # global asset_inventory_shelve_software_assetid_file
        # global asset_inventory_shelve_software_unique_file
        # global asset_inventory_shelve_software_os_unique_file
        # global asset_inventory_sqlite_file
        # global asset_inventory_csv_file
        # global asset_inventory_csv_software_assetid_file
        # global asset_inventory_csv_software_unique_file
        # global asset_inventory_csv_software_os_unique_file
        # global asset_inventory_csv_truncate_cell_limit
        # global asset_inventory_json_file
        # global asset_inventory_log_file
        # global asset_inventory_lock_file
        # global asset_inventory_log_rotate_file
        # global asset_inventory_table_name
        # global asset_inventory_status_table_name
        # global asset_inventory_table_name_software_assetid
        # global asset_inventory_table_name_software_unique
        # global asset_inventory_table_name_software_os_unique
        # global asset_inventory_data_files
        # global asset_inventory_temp_shelve_file

        self.asset_inventory_data_dir = Path(self.qetl_user_data_dir)
        self.asset_inventory_extract_dir = Path(self.asset_inventory_data_dir, "asset_inventory_extract_dir")
        self.asset_inventory_extract_dir_file_search_blob = "asset_inventory_utc*"
        self.asset_inventory_extract_dir_file_search_blob_two = "asset_inventory_count_utc*"
        self.asset_inventory_temp_shelve_file = Path(self.asset_inventory_extract_dir, "asset_inventory_temp_shelve.db")
        self.asset_inventory_shelve_file = Path(self.asset_inventory_data_dir, "asset_inventory_shelve")
        self.asset_inventory_shelve_software_assetid_file = \
            Path(self.asset_inventory_data_dir, "asset_inventory_shelve_software_assetid")

        self.asset_inventory_shelve_software_unique_file = \
            Path(self.asset_inventory_data_dir, "asset_inventory_shelve_software_unique")
        self.asset_inventory_shelve_software_os_unique_file = \
            Path(self.asset_inventory_data_dir, "asset_inventory_shelve_software_os_unique")

        self.asset_inventory_sqlite_file = Path(self.asset_inventory_data_dir, "asset_inventory_sqlite.db")
        self.asset_inventory_csv_file = Path(self.asset_inventory_data_dir, "asset_inventory.csv")
        self.asset_inventory_csv_software_assetid_file = Path(self.asset_inventory_data_dir, "asset_inventory_software_assetid.csv")
        self.asset_inventory_csv_software_unique_file = Path(self.asset_inventory_data_dir, "asset_inventory_software_unique.csv")
        self.asset_inventory_csv_software_os_unique_file = \
            Path(self.asset_inventory_data_dir, "asset_inventory_software_os_unique.csv")
        self.asset_inventory_json_file = Path(self.asset_inventory_data_dir, "asset_inventory.json")
        self.asset_inventory_log_file = Path(self.qetl_user_log_dir, "asset_inventory.log")
        self.asset_inventory_lock_file = Path(self.qetl_user_log_dir, ".asset_inventory.lock")
        self.asset_inventory_log_rotate_file = Path(self.qetl_user_log_dir, "asset_inventory.1.log")
        self.asset_inventory_table_name = 'Q_Asset_Inventory'
        self.asset_inventory_status_table_name = 'Q_Asset_Inventory_Status'
        self.asset_inventory_table_name_software_assetid = 'Q_Asset_Inventory_Software_AssetId'
        self.asset_inventory_table_name_software_unique = 'Q_Asset_Inventory_Software_Unique'
        self.asset_inventory_table_name_software_os_unique = 'Q_Asset_Inventory_Software_OS_Unique'
        self.asset_inventory_data_files = [self.asset_inventory_shelve_file, self.asset_inventory_sqlite_file,
                                      self.asset_inventory_csv_file, self.asset_inventory_csv_software_unique_file,
                                      self.asset_inventory_csv_software_assetid_file, self.asset_inventory_json_file,
                                      self.asset_inventory_shelve_software_assetid_file,
                                      self.asset_inventory_shelve_software_unique_file,
                                      self.asset_inventory_shelve_software_os_unique_file]


    def get_was_user_config(self):
        # global was_data_dir
        # global was_export_dir
        # global was_webapp_last_scan_date
        # global was_payload_option
        # global was_concurrency_limit
        # global was_multi_proc_batch_size
        # global was_limit_hosts
        # global qetl_user_config_settings_yaml_file
        # global qetl_manage_user_selected_datetime
        # global was_json_to_sqlite_via_multiprocessing
        # global was_chunk_size_calc
        # global was_try_extract_max_count
        # global was_http_conn_timeout
        # global was_open_file_compression_method
        # global was_test_system_flag
        # global was_test_number_of_files_to_extract

        def set_was_webapp_last_scan_date():
            # global was_webapp_last_scan_date
            if self.qetl_manage_user_selected_datetime is not None:
                self.was_webapp_last_scan_date = self.qetl_manage_user_selected_datetime
                if self.was_webapp_last_scan_date.startswith("20"):
                    etld_lib_functions.logger.info(f"was_webapp_last_scan_date set by qetl_manage_user -d option")
                else:
                    self.was_webapp_last_scan_date = "2000-01-01T00:00:00Z"
                    etld_lib_functions.logger.info(f"was_webapp_last_scan_date reset to "
                                                   f"2000-01-01T00:00:00Z.  Reset from qetl_manage_user -d option")
            elif self.was_webapp_last_scan_date == 'default':
                self.was_webapp_last_scan_date = etld_lib_datetime.get_utc_date_minus_days(365)
                etld_lib_functions.logger.info(f"was_webapp_last_scan_date default set to utc.now minus 365 days")

            etld_lib_functions.logger.info(f"was_webapp_last_scan_date - "
                                           f"{self.was_webapp_last_scan_date}")

        self.was_data_dir = self.qetl_user_data_dir
        self.was_export_dir = \
            self.get_attribute_from_config_settings('was_export_dir', 'default')
        self.was_webapp_last_scan_date = \
            self.get_attribute_from_config_settings('was_webapp_last_scan_date', 'default')
        self.was_payload_option = self.get_attribute_from_config_settings('was_payload_option', '')
        self.was_multi_proc_batch_size = \
            self.get_attribute_from_config_settings('was_multi_proc_batch_size', '300')
        self.was_limit_hosts = \
            self.get_attribute_from_config_settings('was_limit_hosts', '300')
        self.was_json_to_sqlite_via_multiprocessing = \
            self.get_attribute_from_config_settings('was_json_to_sqlite_via_multiprocessing', True)
        self.was_chunk_size_calc = \
            int(self.get_attribute_from_config_settings('was_chunk_size_calc', '20480'))
        self.was_try_extract_max_count = \
            int(self.get_attribute_from_config_settings('was_try_extract_max_count', '30'))
        self.was_http_conn_timeout = \
            int(self.get_attribute_from_config_settings('was_http_conn_timeout', '900'))
        self.was_open_file_compression_method = \
            self.get_open_file_compression_method_from_config_settings('was_open_file_compression_method')
        self.was_test_system_flag = self.get_attribute_from_config_settings('was_test_system_flag', False)
        self.was_test_number_of_files_to_extract = \
            self.get_attribute_from_config_settings('was_test_number_of_files_to_extract', 3)
        set_was_webapp_last_scan_date()

        etld_lib_functions.logger.info(f"was_export_dir - {self.was_export_dir}")
        etld_lib_functions.logger.info(f"was_extract_dir - {self.was_extract_dir}")


    def setup_was_vars(self):
        # global qetl_user_data_dir
        # global was_data_dir
        # global was_extract_dir
        # global was_extract_dir_file_search_blob
        # global was_extract_dir_file_search_blob_webapp
        # global was_extract_dir_file_search_blob_webapp_detail
        # global was_extract_dir_file_search_blob_finding
        # global was_extract_dir_file_search_blob_finding_detail
        # global was_extract_dir_file_search_blob_catalog
        # global was_extract_dir_file_search_blob_webapp_count
        # global was_extract_dir_file_search_blob_finding_count
        # global was_extract_dir_file_search_blob_catalog_count
        # global was_sqlite_file
        # global was_log_file
        # global was_lock_file
        # global was_log_rotate_file
        # global was_status_table_name
        # global was_webapp_table_name
        # global was_catalog_table_name
        # global was_finding_table_name
        # global was_q_knowledgebase_in_was_finding_table
        # global was_data_files

        self.was_data_dir = Path(self.qetl_user_data_dir)
        self.was_extract_dir = Path(self.was_data_dir, "was_extract_dir")
        self.was_extract_dir_file_search_blob = "was_*_utc_*"
        self.was_extract_dir_file_search_blob_webapp = "was_webapp_utc_*"
        self.was_extract_dir_file_search_blob_webapp_detail = "was_webapp_detail_utc_*"
        self.was_extract_dir_file_search_blob_finding = "was_finding_utc_*"
        self.was_extract_dir_file_search_blob_finding_detail = "was_finding_detail_utc_*"
        self.was_extract_dir_file_search_blob_catalog = "was_catalog_utc_*"
        self.was_extract_dir_file_search_blob_webapp_count = "was_count_webapp_utc_*"
        self.was_extract_dir_file_search_blob_finding_count = "was_count_finding_utc_*"
        self.was_extract_dir_file_search_blob_catalog_count = "was_count_catalog_utc_*"
        self.was_sqlite_file = Path(self.was_data_dir, "was_sqlite.db")
        self.was_log_file = Path(self.qetl_user_log_dir, "was.log")
        self.was_lock_file = Path(self.qetl_user_log_dir, ".was.lock")
        self.was_log_rotate_file = Path(self.qetl_user_log_dir, "was.1.log")
        self.was_q_knowledgebase_in_was_finding_table = 'Q_KnowledgeBase_In_Q_WAS_FINDING'
        self.was_webapp_table_name = 'Q_WAS_WebApp'
        self.was_catalog_table_name = 'Q_WAS_Catalog'
        self.was_finding_table_name = 'Q_WAS_Finding'

        self.was_status_table_name = 'Q_WAS_Status'
        self.was_data_files = [self.was_sqlite_file]


    def setup_completed(self):
        # global setup_completed_flag
        self.setup_completed_flag = True


    def setup_requests_module_tls_verify_status(self):
        # global requests_module_tls_verify_status

        if 'requests_module_tls_verify_status' in self.etld_lib_config_settings_yaml_dict:
            self.requests_module_tls_verify_status = self.etld_lib_config_settings_yaml_dict.get('requests_module_tls_verify_status')
        else:
            self.requests_module_tls_verify_status = True

        if self.requests_module_tls_verify_status is True or self.requests_module_tls_verify_status is False:
            pass
        else:
            self.requests_module_tls_verify_status = True
            etld_lib_functions.logger.warn(f"requests_module_tls_verify_status defaulting to True")

        if self.requests_module_tls_verify_status is False:
            etld_lib_functions.logger.warn(f"requests_module_tls_verify_status in etld_config.yaml is set "
                                           f"to: {self.requests_module_tls_verify_status} "
                                           f"You have selected to not verify tls certificates, subjecting your application "
                                           f"to man in the middle attacks.  Please repair your certificate issue and "
                                           f"reset requests_module_tls_verify_status in etld_config.yaml to True. ")


    @staticmethod
    def run_log_csv_columns():
        csv_columns = ['LOG_DATETIME', 'LOG_LEVEL', 'LOG_WORKFLOW', 'LOG_USERNAME',
                       'LOG_FUNCTION', 'LOG_MESSAGE']
        return csv_columns


    @staticmethod
    def run_log_csv_column_types():
        csv_columns = {
        }
        return csv_columns


    @staticmethod
    def kb_csv_columns():
        csv_columns = ['QID', 'TITLE', 'VULN_TYPE', 'SEVERITY_LEVEL', 'CATEGORY', 'LAST_SERVICE_MODIFICATION_DATETIME',
                       'PUBLISHED_DATETIME', 'PATCHABLE', 'DIAGNOSIS', 'CONSEQUENCE', 'SOLUTION', 'PCI_FLAG',
                       'SUPPORTED_MODULES', 'IS_DISABLED',
                       'CVE_LIST', 'THREAT_INTELLIGENCE', 'CORRELATION', 'BUGTRAQ_LIST', 'SOFTWARE_LIST',
                       'VENDOR_REFERENCE_LIST', 'CVSS', 'CVSS_V3', 'CHANGE_LOG_LIST', 'DISCOVERY', 'PCI_REASONS',
                       'BATCH_DATE', 'BATCH_NUMBER'
                       ]

        return csv_columns


    @staticmethod
    def kb_csv_column_types():

        csv_columns = {
            'QID': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def host_list_csv_columns():  # Return list of csv columns

        csv_columns = [
            'ID', 'ASSET_ID', 'IP', 'IPV6', 'TRACKING_METHOD', 'NETWORK_ID', 'DNS', 'DNS_DATA', 'CLOUD_PROVIDER',
            'CLOUD_SERVICE', 'CLOUD_RESOURCE_ID', 'EC2_INSTANCE_ID', 'NETBIOS', 'OS', 'QG_HOSTID', 'TAGS', 'METADATA',
            'CLOUD_PROVIDER_TAGS', 'LAST_VULN_SCAN_DATETIME', 'LAST_VM_SCANNED_DATE', 'LAST_VM_SCANNED_DURATION',
            'LAST_VM_AUTH_SCANNED_DATE', 'LAST_VM_AUTH_SCANNED_DURATION', 'LAST_COMPLIANCE_SCAN_DATETIME', 'OWNER',
            'COMMENTS', 'USER_DEF', 'ASSET_GROUP_IDS', 'ASSET_RISK_SCORE', 'ASSET_CRITICALITY_SCORE', 'ARS_FACTORS',
            'BATCH_DATE', 'BATCH_NUMBER'
        ]

        return csv_columns


    @staticmethod
    def host_list_csv_column_types():

        csv_columns = {
            'ID': 'INTEGER', 'ASSET_ID': 'INTEGER', 'BATCH_NUMBER': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def host_list_detection_host_csv_columns():  # Return list of csv columns
       # < !ELEMENT
       # HOST_LIST(HOST +) > <!ELEMENT
       # HOST(
       # ID, ASSET_ID?, IP?, IPV6?, TRACKING_METHOD?, NETWORK_ID?, OS?, OS_CPE?, DNS?, DNS_DATA?, CLOUD_PROVIDER?,
       # CLOUD_SERVICE?, CLOUD_RESOURCE_ID?, EC2_INSTANCE_ID?, NETBIOS?, QG_HOSTID?,
       # LAST_SCAN_DATETIME?, LAST_VM_SCANNED_DATE?, LAST_VM_SCANNED_DURATION?, LAST_VM_AUTH_SCANNED_DATE?,
       # LAST_VM_AUTH_SCANNED_DURATION?, LAST_PC_SCANNED_DATE?,
       # TAGS?, METADATA?, CLOUD_PROVIDER_TAGS?, DETECTION_LIST) >

       # csv_columns = [
       #     'ID', 'ASSET_ID', 'IP', 'IPV6', 'TRACKING_METHOD', 'NETWORK_ID', 'OS', 'OS_CPE', 'DNS', 'DNS_DATA',
       #     'CLOUD_PROVIDER', 'CLOUD_SERVICE', 'CLOUD_RESOURCE_ID', 'EC2_INSTANCE_ID', 'NETBIOS', 'QG_HOSTID',
       #     'LAST_SCAN_DATETIME', 'LAST_VM_SCANNED_DATE', 'LAST_VM_SCANNED_DURATION',
       #     'LAST_VM_AUTH_SCANNED_DATE', 'LAST_VM_AUTH_SCANNED_DURATION', 'LAST_PC_SCANNED_DATE',
       #     'TAGS', 'METADATA', 'CLOUD_PROVIDER_TAGS', 'BATCH_DATE', 'BATCH_NUMBER'
       # ]

        csv_columns = [
                       'ID', 'ASSET_ID', 'IP', 'IPV6', 'TRACKING_METHOD', 'NETWORK_ID', 'OS', 'OS_CPE', 'DNS', 'DNS_DATA',
                       'NETBIOS', 'QG_HOSTID',
                       'LAST_SCAN_DATETIME', 'LAST_VM_SCANNED_DATE', 'LAST_VM_SCANNED_DURATION',
                       'LAST_VM_AUTH_SCANNED_DATE', 'LAST_VM_AUTH_SCANNED_DURATION', 'LAST_PC_SCANNED_DATE',
                       'BATCH_DATE', 'BATCH_NUMBER'
                       ]
        return csv_columns


    @staticmethod
    def host_list_detection_host_csv_column_types():  # Return list of csv columns
        csv_columns = {
            'ID': 'INTEGER', 'ASSET_ID': 'INTEGER', 'BATCH_NUMBER': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def host_list_detection_qids_csv_columns():  # Return list of csv columns
        # < !ELEMENT
        # DETECTION_LIST(DETECTION +) > <!ELEMENT
        # DETECTION(
        # QID, TYPE, SEVERITY?, PORT?, PROTOCOL?, FQDN?, SSL?, INSTANCE?, RESULTS?, STATUS?,
        # FIRST_FOUND_DATETIME?, LAST_FOUND_DATETIME?, TIMES_FOUND?, LAST_TEST_DATETIME?, LAST_UPDATE_DATETIME?,
        # LAST_FIXED_DATETIME?, FIRST_REOPENED_DATETIME?, LAST_REOPENED_DATETIME?, TIMES_REOPENED?, SERVICE?,
        # IS_IGNORED?, IS_DISABLED?, AFFECT_RUNNING_KERNEL?, AFFECT_RUNNING_SERVICE?, AFFECT_EXPLOITABLE_CONFIG?,
        # LAST_PROCESSED_DATETIME?
        csv_columns = [
                       'ID', 'ASSET_ID', 'QID', 'TYPE', 'STATUS', 'PORT', 'PROTOCOL', 'SEVERITY', 'FQDN', 'SSL', 'INSTANCE',
                       'LAST_PROCESSED_DATETIME', 'FIRST_FOUND_DATETIME', 'LAST_FOUND_DATETIME', 'TIMES_FOUND',
                       'LAST_TEST_DATETIME', 'LAST_UPDATE_DATETIME', 'LAST_FIXED_DATETIME', 'FIRST_REOPENED_DATETIME',
                       'LAST_REOPENED_DATETIME', 'TIMES_REOPENED', 'SERVICE', 'IS_IGNORED', 'IS_DISABLED',
                       'AFFECT_RUNNING_KERNEL', 'AFFECT_RUNNING_SERVICE', 'AFFECT_EXPLOITABLE_CONFIG',
                       'QDS', 'QDS_FACTORS',
                       'RESULTS', 'BATCH_DATE', 'BATCH_NUMBER'
                      ]
        return csv_columns

    @staticmethod
    def host_list_detection_qids_csv_column_types():  # Return list of csv columns
        csv_columns = {
            'ID': 'INTEGER', 'ASSET_ID': 'INTEGER', 'QID': 'INTEGER', 'BATCH_NUMBER': 'INTEGER',
            'TIMES_REOPENED': 'INTEGER', 'TIMES_FOUND': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def asset_inventory_csv_columns():  # Return list of csv columns updated 0.6.111

        csv_columns = [
            'assetId', 'assetUUID', 'hostId', 'lastModifiedDate', 'agentId', 'createdDate', 'sensorLastUpdatedDate',
            'sensor_lastVMScanDate', 'sensor_lastComplianceScanDate', 'sensor_lastFullScanDate', 'inventory_createdDate',
            'inventory_lastUpdatedDate', 'agent_lastActivityDate', 'agent_lastCheckedInDate', 'agent_lastInventoryDate',
            'assetType', 'address', 'dnsName', 'assetName', 'netbiosName', 'timeZone', 'biosDescription', 'lastBoot',
            'totalMemory', 'cpuCount', 'lastLoggedOnUser', 'domainRole', 'hwUUID', 'biosSerialNumber', 'biosAssetTag', 'isContainerHost',
            'operatingSystem', 'hardware', 'userAccountListData', 'openPortListData', 'volumeListData',
            'networkInterfaceListData', 'softwareListData', 'provider', 'cloudProvider', 'agent', 'sensor', 'container',
            'inventory', 'activity', 'tagList', 'serviceList', 'lastLocation', 'criticality',
            'businessInformation', 'assignedLocation', 'businessAppListData',
            'riskScore', 'passiveSensor', 'domain', 'subdomain', 'whois', 'isp', 'asn',
            'processor', 'missingSoftware', 'TRUNCATED_FIELD_LIST'
                       ]
        return csv_columns


    @staticmethod
    def asset_inventory_csv_column_types():

        csv_columns = {
            'assetId': 'INTEGER', 'hostId': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def asset_inventory_software_assetid_csv_columns():

        csv_columns = [
            'assetId', 'fullName'
        ]
        return csv_columns


    @staticmethod
    def asset_inventory_software_assetid_csv_column_types():

        csv_columns = {
            'assetId': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def asset_inventory_software_unique_csv_columns():
        csv_columns = [
            'fullName'
        ]
        return csv_columns


    @staticmethod
    def asset_inventory_software_os_unique_csv_columns():
        csv_columns = [
            'fullName', 'osName',
            'isIgnored', 'ignoredReason', 'category', 'gaDate', 'eolDate', 'eosDate',
            'stage', 'lifeCycleConfidence', 'eolSupportStage', 'eosSupportStage'
        ]
        return csv_columns


    @staticmethod
    def was_webapp_csv_columns():
        csv_columns = [
            'id', 'name', 'url', 'os', 'owner', 'scope', 'subDomain', 'domains', 'uris', 'attributes', 'defaultProfile',
            'defaultScanner', 'defaultScannerTags', 'scannerLocked', 'progressiveScanning', 'redundancyLinks',
            'maxRedundancyLinks', 'urlBlacklist', 'urlWhitelist', 'postDataBlacklist', 'logoutRegexList', 'authRecords',
            'dnsOverrides', 'useRobots', 'useSitemap', 'headers', 'malwareMonitoring', 'malwareNotification',
            'malwareTaskId', 'malwareScheduling', 'tags', 'comments', 'isScheduled', 'lastScan', 'createdBy',
            'createdDate', 'updatedBy', 'updatedDate', 'screenshot', 'proxy', 'config', 'crawlingScripts',
            'lastScanStatus', 'removeFromSubscription', 'reactivateIfExists', 'postmanCollection', 'swaggerFile'
        ]
        return csv_columns


    @staticmethod
    def was_webapp_csv_column_types():

        csv_columns = {
            'id': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def was_finding_csv_columns():
        # "Finding": {
        #     "webApp": {
        #         "id": 78440423,
        #         "tags": {
        #             "list": [
        #                 {
        #                     "Tag": {
        #                         "name": "Web Application Assets",
        #                         "id": 7472465
        #                     }
        #                 }
        #             ],
        #             "count": 1
        #         },
        #         "url": "http://owaspbwa/bWAPP/login.php",
        #         "name": "bWAPP"
        #     },
        #     "id": 149802,
        #     "url": "http://owaspbwa/bWAPP/login.php",
        #     "lastDetectedDate": "2018-07-03T20:06:11Z",
        #     "qid": 0,
        #     "etl_workflow_validation_type": "VULNERABILITY",
        #     "status": "NEW",
        #     "timesDetected": 1,
        #     "potential": "false",
        #     "findingType": "BURP",
        #     "lastTestedDate": "2018-07-03T20:06:11Z",
        #     "firstDetectedDate": "2018-07-03T20:06:11Z",
        #     "isIgnored": "false",
        #     "severity": "5",
        #     "uniqueId": "e5028940-ffe9-4a6d-90c8-68724b96ed89"
        # }

        # csv_columns = [
        #     'id', 'webApp_id', 'webApp_name', 'webApp_tags', 'webApp_url',
        #     'url', 'lastDetectedDate', 'qid', 'etl_workflow_validation_type', 'status', 'timesDetected',
        #     'potential', 'findingType', 'lastTestedDate', 'firstDetectedDate', 'isIgnored',
        #     'severity', 'uniqueId'
        # ]
        # Note: group_0 and function_0 contain "group" and "function" data for DB Compatability.
        csv_columns = [
            'id', 'webApp_id', 'webApp_name', 'webApp_tags', 'webApp_url', 'uniqueId',
            'qid', 'name', 'etl_workflow_validation_type', 'potential', 'findingType', 'group_0',
            'cwe', 'owasp', 'wasc', 'param', 'function_0', 'content', 'resultList', 'severity',
            'originalSeverity', 'url', 'status', 'firstDetectedDate', 'lastDetectedDate',
            'timesDetected', 'webApp', 'patch', 'isIgnored', 'ignoredReason', 'ignoredBy',
            'ignoredDate', 'ignoredComment', 'reactivateIn', 'reactivateDate', 'externalRef',
            'severityComment', 'editedSeverityUser', 'editedSeverityDate', 'retest',
            'sslData', 'cvssV3', 'history', 'updatedDate'
        ]
        return csv_columns


    @staticmethod
    def was_finding_csv_column_types():

        csv_columns = {
            'webApp_id': 'INTEGER', 'id': 'INTEGER', 'severity': 'INTEGER', 'timesDetected': 'INTEGER', 'qid': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def was_catalog_csv_columns():
        # {
        #     "Catalog": {
        #         "fqdn": "ks355837.kimsufi.com",
        #         "updatedDate": "2022-01-18T19:45:09Z",
        #         "id": 11403514,
        #         "source": "VM_SCAN",
        #         "operatingSystem": "Ubuntu / Linux 2.6.x",
        #         "port": "443",
        #         "createdDate": "2021-08-31T18:11:41Z",
        #         "status": "NEW",
        #         "ipAddress": "91.121.138.65",
        #         "updatedBy": {
        #             "firstName": "John Delaroderie",
        #             "id": 84004451,
        #             "lastName": "TAM-LAB",
        #             "username": "tamde_hd1"
        #         }
        #     }
        # },

        csv_columns = [
            'id', 'ipAddress', 'fqdn', 'port', 'operatingSystem', 'source', 'status',
            'createdDate', 'updatedDate', 'updatedBy'
        ]
        return csv_columns


    @staticmethod
    def was_catalog_csv_column_types():

        csv_columns = {
            'id': 'INTEGER'
        }
        return csv_columns


    @staticmethod
    def status_table_csv_columns():  # Return list of csv columns

        csv_columns = [
            'STATUS_NAME', 'STATUS_DETAIL', 'LAST_BATCH_PROCESSED'
        ]
        return csv_columns


    @staticmethod
    def status_table_csv_column_types():

        csv_columns = {
            'LAST_BATCH_PROCESSED': 'TEXT'
        }
        return csv_columns


    def set_limit_open_files_to_hard_limit_for_multiprocessing_pipes(self, module_function="limit_open_files", logger_method=print):
        # Host List Detection accumulates pipes open during processing.
        # Until addressed, ensure open files is set to hard limit.
        limit_soft, limit_hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger_method(f"limit_open_files before: {module_function} limit_soft={limit_soft}, limit_hard={limit_hard}")
        resource.setrlimit(resource.RLIMIT_NOFILE, (limit_hard, limit_hard))
        limit_soft, limit_hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        logger_method(f"limit_open_files after:  {module_function} limit_soft={limit_soft}, limit_hard={limit_hard}")


    def total_system_stats_cpu_ram_swap_disk(self, sys_stat: dict):
        #global system_usage_counters
        self.system_usage_counters.append(sys_stat)


    def log_system_stats_cpu_ram_swap_disk(self):
        # global system_usage_counters
        self.system_stat = etld_lib_functions.log_system_information(
            data_directory=self.qetl_user_home_dir,
            logger_method=etld_lib_functions.logger.info)

        self.system_usage_counters.append(self.system_stat)

        etld_lib_functions.if_disk_space_usage_greater_than_90_log_warning(
            data_directory=self.qetl_user_home_dir,
            logger_method=etld_lib_functions.logger.warn)


    def check_swap_space(self):
        etld_lib_functions.if_swap_space_total_is_low_log_warning(
            logger_method=etld_lib_functions.logger.warn
        )


    def check_ram_space(self):
        etld_lib_functions.if_ram_space_size_is_low_log_warning(
            logger_method=etld_lib_functions.logger.warn
        )

    def get_qetl_code_dir(self):
        self.qetl_code_dir = etld_lib_functions.qetl_code_dir
        self.qetl_code_dir_child = etld_lib_functions.qetl_code_dir_child

    def setup_user_home_directories(self):
        # TODO setup home directories before logging so
        # TODO we can reference paths in qetl_manage_user before logging is turned on.
        # Directory Structure
        #  ${ANYDIR}/opt/qetl/users/${NAME OF USER}/qetl_home
        #
        #  qetl_user_root_dir = ${ANYDIR}/opt/qetl/users/{$NAME OF USER} = directory of a qetl user.
        #                       Ex. /home/dgregory/opt/qetl/users/{$NAME OF USER}
        #                       Ex. /opt/qetl/users/{$NAME OF USER}
        #  qetl_user_home_dir = ${ANYDIR}/opt/qetl/users/{$NAME OF USER}/qetl_home
        #                       Ex. /home/dgregory/opt/qetl/users/quays01/qetl_home
        #
        # Top level directories
        # global qetl_all_users_dir            # opt/qetl/users
        # global qetl_user_root_dir            # Parent directory for qetl_user_home_dir
        # global qualys_etl_user_home_env_var  # Environment variable set to qualys_etl_user_home
        # global qetl_user_home_dir            # Home directory for api data, config, credentials, logs.
        # # Directories holding a users data
        # global qetl_user_data_dir            # xml,json,csv,sqlite,shelve data
        # global qetl_user_log_dir             # logs
        # global qetl_user_config_dir          # configuration
        # global qetl_user_cred_dir            # credentials
        # global qetl_user_bin_dir             # TODO determine what to do with qetl_user_bin_dir
        #
        # global qetl_user_config_settings_yaml_file
        # global qetl_user_config_settings_yaml
        #
        # global qetl_code_dir                 # Parent Directory of qualys_etl code dir.
        # global qetl_user_default_config      # Initial configuration populated into qetl_user_config_dir

        self.set_path_qetl_user_home_dir()
        self.create_user_data_dirs()

        etld_lib_functions.logger.info(f"parent user app dir  - {str(self.qetl_user_root_dir)}")
        etld_lib_functions.logger.info(f"user home directory  - {str(self.qetl_user_home_dir)}")
        etld_lib_functions.logger.info(f"qetl_all_users_dir   - All users dir       - {self.qetl_all_users_dir}")
        etld_lib_functions.logger.info(f"qetl_user_root_dir   - User root dir       - {self.qetl_user_root_dir}")
        etld_lib_functions.logger.info(f"qetl_user_home_dir   - qualys user         - {self.qetl_user_home_dir}")
        etld_lib_functions.logger.info(f"qetl_user_data_dir   - xml,json,csv,sqlite - {self.qetl_user_data_dir}")
        etld_lib_functions.logger.info(f"qetl_user_log_dir    - log files           - {self.qetl_user_log_dir}")
        etld_lib_functions.logger.info(f"qetl_user_config_dir - yaml configuration  - {self.qetl_user_config_dir}")
        etld_lib_functions.logger.info(f"qetl_user_cred_dir   - yaml credentials    - {self.qetl_user_cred_dir}")
        etld_lib_functions.logger.info(f"qetl_user_bin_dir    - etl scripts         - {self.qetl_user_bin_dir}")

    def main(self):

        self.get_qetl_code_dir()
        self.setup_user_home_directories()

        self.load_etld_lib_config_settings_yaml()
        self.setup_requests_module_tls_verify_status()

        self.setup_kb_vars()
        self.get_kb_user_config()

        self.setup_host_list_vars()
        self.get_host_list_user_config()

        self.setup_host_list_detection_vars()
        self.get_host_list_detection_user_config()

        self.setup_asset_inventory_vars()
        self.get_asset_inventory_user_config()

        self.setup_was_vars()
        self.get_was_user_config()

        self.setup_test_system_vars()

        self.set_limit_open_files_to_hard_limit_for_multiprocessing_pipes(logger_method=etld_lib_functions.logger.info)
        self.log_system_stats_cpu_ram_swap_disk()
        self.setup_completed()

def test_obj():
    try:
        this_prog = Path(__file__).name
        etld_lib_functions.logger.info(f"Begin testing {this_prog}")
        etld_lib_config.set_path_qetl_user_home_dir()

        database_type = "DATABASE NAME"
        table_name = "TABLE NAME"
        counter_obj = etld_lib_functions_obj.DisplayCounterToLog(
            display_counter_at=1,
            logger_func=etld_lib_functions.logger.info,
            display_counter_log_message=f"rows added/updated into {database_type} "
                                        f"table {table_name}")
        counter_obj.update_counter()
        counter_obj.display_counter_to_log()
        counter_obj.update_counter()
        counter_obj.display_counter_to_log()
        counter_obj.display_final_counter_to_log()
        etld_lib_functions.logger.info(f"End   testing {this_prog}")
    except Exception as e:
        etld_lib_functions.logger.info(f"Problem setting up logging.  Investigate error and rerun. Exception: {e}")
        exit(1)

if __name__ == '__main__':
    this_prog = Path(__file__).name
    etld_lib_functions = etld_lib_functions_obj.StartLoggingToStdout(my_logger_prog_name=f"{this_prog}")
    etld_lib_config = EtldLibConfigObj(etld_lib_functions)
    etld_lib_config.set_path_qetl_user_home_dir()
    etld_lib_config.main()
    test_obj()



