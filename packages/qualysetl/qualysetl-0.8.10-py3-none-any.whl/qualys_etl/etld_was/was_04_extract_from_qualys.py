#!/usr/bin/env python3
from pathlib import Path
import json
import gzip
import re
from qualys_etl.etld_lib import etld_lib_credentials
from qualys_etl.etld_lib import etld_lib_authentication_objects
from qualys_etl.etld_lib import etld_lib_config
from qualys_etl.etld_lib import etld_lib_functions
from qualys_etl.etld_lib import etld_lib_extract_transform_load as etld_lib_extract_transform_load


def was_webapp_extract(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, last_id=0, page_size=25):

    start_msg_was_extract(function_name='was_webapp_extract')

    payload = '{"ServiceRequest": {' \
              '"preferences": ' \
              '{' \
              '"limitResults": '  f'"{page_size}"'  ', ' \
              '"verbose": "true"' \
              '}, ' \
              '"filters": {' '"Criteria": [' \
              '{"field": "id", "operator": "GREATER", "value": '  f'"{last_id}"' + '},' \
              '{"field": "lastScan.date", "operator": "GREATER", "value": '  \
              f'"{etld_lib_config.was_webapp_last_scan_date}"' + '}' \
              ']}}}'
    if str(etld_lib_config.was_webapp_last_scan_date).startswith("2000"):
        # Get all webapps regardless of scan status.
        payload = '{"ServiceRequest": {' \
                  '"preferences": ' \
                  '{' \
                  '"limitResults": '  f'"{page_size}"'  ', ' \
                  '"verbose": "true"' \
                  '}, ' \
                  '"filters": {' '"Criteria": [' \
                  '{"field": "id", "operator": "GREATER", "value": '  f'"{last_id}"' + '}' \
                  ']}}}'


    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/search/was/webapp"
    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    etld_lib_functions.logger.info(f"api call     - URL:{url} - PAYLOAD:{payload}")
    json_file = Path(file_info_dict['next_file_path'])

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json',
        compression_method=etld_lib_config.was_open_file_compression_method)
    end_msg_was_extract(function_name='was_webapp_extract')

    was_webapp_detail_extract_controller(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, last_id=0, page_size=25)


def was_webapp_detail_extract_controller(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, last_id=0, page_size=25):
    # was_webapp_utc_run_datetime_2022-11-01T21:50:59Z_utc_last_scan_date_2022-10-25T00:00:00Z_batch_000001.json.gz
    # was_webapp_detail_utc_run_datetime_2022-11-01T21:50:59Z_utc_last_scan_date_2022-10-25T00:00:00Z_batch_000001_id_[idnum].json.gz

    start_msg_was_extract(function_name=f'was_webapp_detail_extract_{batch_number_str}')
    json_file = Path(file_info_dict['next_file_path'])
    webapp_id_list = []
    with etld_lib_config.was_open_file_compression_method(str(json_file), "rt", encoding='utf-8')  as read_file:
        json_data = json.load(read_file)
        if 'data' in  json_data['ServiceResponse']:
            for data_list_item in json_data['ServiceResponse']['data']:
                if 'WebApp' in data_list_item:
                    if 'id' in data_list_item['WebApp']:
                        webapp_id_list.append(data_list_item['WebApp']['id'])
    if len(webapp_id_list) == 0:
        etld_lib_functions.logger.info(f"No webapps scanned since {etld_lib_config.was_webapp_last_scan_date}")

    for webapp_id in webapp_id_list:

        json_file = Path(file_info_dict['next_file_path'])
        batch_number_str_with_webapp_id = f"{batch_number_str}_webapp_id_{webapp_id}"
        # was_webapp_utc_run_datetime_2022-11-01T21:50:59Z_utc_last_scan_date_2022-10-25T00:00:00Z_batch_000001.json.gz
        # was_webapp_detail_utc_run_datetime_2022-11-01T21:50:59Z_utc_last_scan_date_2022-10-25T00:00:00Z_batch_000001_webapp_id_[idnum].json.gz
        # was_finding_detail_utc_run_datetime_2022-11-01T21:50:59Z_utc_last_scan_date_2022-10-25T00:00:00Z_batch_000001_webapp_id_[idnum].json.gz
        file_info_dict['webapp_id_detail_json_file'] = str(json_file).\
            replace("/was_webapp_utc", "/was_webapp_detail_utc").\
            replace(f"_{batch_number_str}", f"_{batch_number_str_with_webapp_id}")
        file_info_dict['finding_detail_for_webapp_id_json_file'] = str(json_file). \
            replace("/was_webapp_utc", "/was_finding_detail_utc"). \
            replace(f"_{batch_number_str}", f"_{batch_number_str_with_webapp_id}")

        was_webapp_detail_extract_data_for_webapp_id(
            batch_number_str_with_webapp_id, qualys_headers_dict, cred_dict, file_info_dict, webapp_id=webapp_id)

        was_finding_detail_extract_data_for_webapp_id(
            batch_number_str_with_webapp_id, qualys_headers_dict, cred_dict, file_info_dict, webapp_id=webapp_id)

    end_msg_was_extract(function_name=f'was_webapp_detail_extract_batch_{batch_number_str}')


def was_webapp_detail_extract_data_for_webapp_id(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, webapp_id=0):

    json_file = file_info_dict['webapp_id_detail_json_file']

    payload = {}
    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/get/was/webapp/{webapp_id}"
    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    start_msg_was_extract(function_name=f'was_webapp_detail_extract_{batch_number_str}')
    etld_lib_functions.logger.info(f"api call     - URL:{url} - PAYLOAD:{payload}")

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json',
        compression_method=etld_lib_config.was_open_file_compression_method,
        request_method='GET')
    end_msg_was_extract(function_name=f'was_webapp_detail_extract_{batch_number_str}')


def was_finding_detail_extract_data_for_webapp_id(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, webapp_id=0, page_size=1000):

    json_file = file_info_dict['finding_detail_for_webapp_id_json_file']

    start_msg_was_extract(function_name=f'was_finding_detail_extract_{batch_number_str}')

    payload = '{"ServiceRequest": {' \
              '"preferences": {"limitResults": ' \
              f'"{page_size}"' \
              ', "verbose": "true"}, ' \
              '"filters": {' '"Criteria": ' \
              '[{"field": "webApp.id", "operator": "EQUALS", "value": ' \
              f'"{webapp_id}"' + '}]}}}'

    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/search/was/finding"
    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    etld_lib_functions.logger.info(f"api call     - URL:{url} - PAYLOAD:{payload}")

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json',
        compression_method=etld_lib_config.was_open_file_compression_method)

    # NOT THIS ONE - json_file = Path(file_info_dict['next_file_path'])
    with etld_lib_config.was_open_file_compression_method(str(json_file), "rt", encoding='utf-8')  as read_file:
        json_data = json.load(read_file)
        if 'ServiceResponse' in json_data:
            if 'hasMoreRecords' in json_data['ServiceResponse']:
                if str(json_data['ServiceResponse']['hasMoreRecords']).lower() == 'true':
                    etld_lib_functions.logger.error(f"Found webapp_id: {batch_number_str} has more than page_size: {page_size} findings")
                    etld_lib_functions.logger.error(f"File: {str(json_file)}")
                    etld_lib_functions.logger.error(f"Contact your Qualys TAM to discuss solution with David Gregory.")
                    #exit(1) - do not exit, instead report error to logs and move forward.
                    # let validate log check will catch this error.
    end_msg_was_extract(function_name=f'was_finding_detail_extract_{batch_number_str}')


def was_catalog_extract(
        batch_number_str, qualys_headers_dict, cred_dict, file_info_dict, last_id=0, page_size=25):

    start_msg_was_extract(function_name='was_catalog_extract')
    filter_field = 'id'
    filter_operator = 'GREATER'
    filter_value = last_id
    payload = '{"ServiceRequest": {' \
              '"preferences": {"limitResults": ' f'"{page_size}"'  ', "verbose": "true"}, ' \
              '"filters": {' '"Criteria":  ' \
              '{"field": ' f'"{filter_field}"' ', "operator": ' f'"{filter_operator}"' ', "value": ' f'"{filter_value}"' '}' \
              '}' \
              '}}'

    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/search/was/catalog"
    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    etld_lib_functions.logger.info(f"api call     - URL:{url} - PAYLOAD:{payload}")
    json_file = Path(file_info_dict['next_file_path'])

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json',
        compression_method=etld_lib_config.was_open_file_compression_method)
    end_msg_was_extract(function_name='was_catalog_extract')


def was_webapp_extract_count(batch_number_str, qualys_headers_dict, cred_dict, file_info_dict):

    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/count/was/webapp"

    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    if str(etld_lib_config.was_webapp_last_scan_date).startswith("2000"):
        # Get all webapps regardless of scan status.
        payload = '{"ServiceRequest": {' \
                  '"filters": {' '"Criteria": [' \
                  '{"field": "id", "operator": "GREATER", "value": '  f'"0"' + '}' \
                  ']}}}'

    else:
        payload = '{"ServiceRequest": {' \
                  '"filters": {' '"Criteria": [' \
                  '{"field": "id", "operator": "GREATER", "value": '  f'"0"' + '},' \
                  '{"field": "lastScan.date", "operator": "GREATER", "value": ' \
                   f'"{etld_lib_config.was_webapp_last_scan_date}"' + '}' \
                   ']}}}'

    etld_lib_functions.logger.info(f"api call     - {url}")
    json_file = Path(file_info_dict['next_file_path'])

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json')

    was_log_count(json_file=json_file, count_type='was_webapp')


def was_finding_extract_count(batch_number_str, qualys_headers_dict, cred_dict, file_info_dict):

    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/count/was/finding"

    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    etld_lib_functions.logger.info(f"api call     - {url}")

    json_file = Path(file_info_dict['next_file_path'])

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload={},
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json')

    was_log_count(json_file=json_file, count_type='was_finding')


def was_catalog_extract_count(batch_number_str, qualys_headers_dict, cred_dict, file_info_dict):

    url = f"https://{cred_dict['api_fqdn_server']}/qps/rest/3.0/count/was/catalog"

    headers = {'X-Requested-With': 'qualysetl',
               'Authorization': cred_dict['authorization'],
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    payload = '{"ServiceRequest": {' \
              '"filters": {' '"Criteria": [' \
              '{"field": "id", "operator": ' \
              '"GREATER", "value": '  f'"{etld_lib_config.was_catalog_start_greater_than_last_id}"' + '}' \
                  ']}}}'

    filter_field = 'id'
    filter_operator = 'GREATER'
    filter_value = etld_lib_config.was_catalog_start_greater_than_last_id
    payload = '{"ServiceRequest": {' \
              '"filters": {' '"Criteria":  ' \
              '{"field": ' f'"{filter_field}"' ', "operator": ' f'"{filter_operator}"' ', "value": ' f'"{filter_value}"' '}' \
              '}' \
              '}}'

    etld_lib_functions.logger.info(f"api call     - URL:{url} - PAYLOAD:{payload}")
    json_file = Path(file_info_dict['next_file_path'])

    etld_lib_extract_transform_load.extract_qualys(
        try_extract_max_count=etld_lib_config.was_try_extract_max_count,
        url=url,
        headers=headers,
        payload=payload,
        http_conn_timeout=etld_lib_config.was_http_conn_timeout,
        chunk_size_calc=etld_lib_config.was_chunk_size_calc,
        output_file=json_file,
        cred_dict=cred_dict,
        qualys_headers_multiprocessing_dict=qualys_headers_dict,
        batch_number_formatted=batch_number_str,
        extract_validation_type='json')

    was_log_count(json_file=json_file, count_type='was_catalog')


def was_log_count(json_file, count_type='was_webapp'):
    try:
        # {"ServiceResponse":{"count":139,"responseCode":"SUCCESS"}}
        with etld_lib_config.was_open_file_compression_method(str(json_file), "rt", encoding='utf-8') as read_file:
            my_count_service_response = json.load(read_file)
            if 'ServiceResponse' in my_count_service_response.keys():
                my_count = my_count_service_response['ServiceResponse']
                if "responseCode" in my_count.keys():
                    if my_count['responseCode'] == 'SUCCESS':
                        etld_lib_functions.logger.info(f"{count_type} count: {my_count['count']}")
                    else:
                        raise Exception(f"{count_type} failed, responseCode: {my_count_service_response},"
                                        f" responseMessage: {my_count_service_response}")
                else:
                    raise Exception(f"{count_type} failed, responseCode: {my_count_service_response},"
                                    f" responseMessage: {my_count_service_response}")
            else:
                raise Exception(f"{count_type} failed, responseCode: {my_count_service_response},"
                                f" responseMessage: {my_count_service_response}")

    except Exception as e:
        etld_lib_functions.logger.error(f"Exception: {e}")
        etld_lib_functions.logger.error(f"{count_type} failed, responseCode: {my_count_service_response},")
        etld_lib_functions.logger.error(f"Potential JSON File corruption or api error detected: {json_file}")
        raise Exception("WAS Application Count Failed.")


def start_msg_was_extract(function_name=""):
    etld_lib_functions.logger.info(f"start {function_name}")


def end_msg_was_extract(function_name=""):
    etld_lib_functions.logger.info(f"end {function_name}")


def main(args=None):
    was_webapp_extract()


if __name__ == "__main__":
    etld_lib_functions.main(my_logger_prog_name='was_04_extract_from_qualys')
    etld_lib_config.main()
    etld_lib_credentials.main()
    etld_lib_authentication_objects.main()
    main()



