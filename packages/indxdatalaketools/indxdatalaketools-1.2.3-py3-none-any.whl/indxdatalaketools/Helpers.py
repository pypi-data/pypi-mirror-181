#
#   Created By Ryan McDermott
#   Created on 2/21/2022
#
#   Helper functions used in the datalake tools

import ast
import csv
import hashlib
import sys
import os
import time
from google.api_core.exceptions import ServiceUnavailable
import requests


class PropertiesTableException(BaseException):
    """Raised when the input value is too small"""
    pass


def read_batch_file(file_name: str) -> list:
    ''' Reads the contents of the batch file and returns a list of lists

        Args:
            file_name (str): The path of the file we are reading
        
        Returns:
            list: A list of list containing all of the information in the header
        '''
    batch_list = []
    with open(file_name, encoding="utf-8") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            batch_list.append(row)

    return batch_list


def convert_keys_in_dictionary(patient_data):
    '''
        This function converts the keys in the patient data dictionary
            To the form recognized by the API
        Args:
            - patient_data (dict): the patient data dictionary
        Returns:
            - dict: The converted dictionary
    '''
    converted_patient_data = {}

    for key, value in patient_data.items():
        new_key = key.lower().replace("_", "-")
        if "name" in new_key:
            new_key = new_key.replace("name", "-name")
        if value is None:
            continue
        converted_patient_data[new_key] = value

    return converted_patient_data


def delete_blob(blob):
    '''
        connects to GCS to delete blob passed
        Args:
            blob (google.cloud.storage.blob): The blob we wish to delete
        Returns:
            boolean: True if the blob was deleted, False if otherwise
    '''
    try:
        blob.delete()
        return True
    except Exception as e:
        print_error("Could not delete blob " + str(e))
        return False


def patch_bucket(bucket):
    '''
        Try and Catch block to determine if the bucket patch was successful
        Args: 
            bucket (google.cloud.storage.Bucket): The bucket we wish to patch
        Returns:
            boolean: True if the operation was sucesfull, False if otherwise
    '''
    try:
        bucket.patch()
        return True
    except Exception as exception:
        print_error("Bucket was unable to get patched: " + str(exception))
        return False


def patch_blob(blob):
    '''
        Try and Catch block to determine if the blob patch was successful
        Args: 
            bucket (google.cloud.storage.Blob): The blob we wish to patch
        Returns:
            boolean: True if the operation was sucesfull, False if otherwise
    '''
    try:
        blob.patch()
        return True
    except Exception as exception:
        print_error("Bucket was unable to get patched: " + str(exception))
        return False


def try_bucket_exists(bucket):
    '''
        Try catch block of checking if a GCS Bucket exists
    '''
    try:
        return bucket.exists()
    except Exception as e:
        print_error("Could not check if bucket exists: " + str(e))
        return False


def try_blob_exists(blob):
    '''
        Try catch block of checking if a GCS Blob exists
    '''
    try:
        return blob.exists()
    except Exception as e:
        print_error("Could not check if blob exists: " + str(e))
        return False


def print_error(*args, **kwargs):
    '''
        Called the same was as print, this instead prints to std err
    '''
    print(*args, file=sys.stderr, **kwargs)


def create_service_account_name(client_uuid):
    '''
        Function that creates an md5 hash of the client uuid then removes the last 8 letters of it
        and adds client to the front. this will be the name for the client service account
        Args:
            client_uuid (string): the uuid of the client
        Returns:
            string: the service account name
    '''
    md5_hash = hashlib.md5()
    encoded = client_uuid.encode()
    md5_hash.update(encoded)
    md_5_clientuuid = md5_hash.hexdigest()
    service_account_name = 'client' + str(md_5_clientuuid)[0:24]

    return service_account_name


def hash_contents_to_file_name(file_path, contents):
    """
        hashes the contents of the file to be used for rename the file
        Args:
            file_path (string): the path to the file, used to get extension
            contents (bytes): byte representation of the file contents
        Returns:
            string: the new file name
    """
    file_path = file_path.replace("\\", "/")
    extension = os.path.splitext(file_path)[1]
    encoded_contents = contents
    hash_contents = hashlib.sha1(encoded_contents)
    name = hash_contents.hexdigest()

    if extension == '':
        return name

    return name + extension


def patient_hash(client_id, patient_mrn_list):
    """
        This function takes the patients MRN and the client id's 
        UUID and creates a sha1 hash for the patient ID
        Args:
            client_id (string): The clients UUID
            patient_mrn_list (list of string): a list of Patient MRN 
        Returns:
            list: The list of strings containing all of the patient Id's 
    """
    patient_hash_list = []
    for patient in patient_mrn_list:
        for i in range(len(patient)):
            if patient[i] != '0':
                patient = patient[i:]
                break
        if patient == 'UNKNOWN':
            patient_hash_list.append('UNKNOWN')
        client_patient = client_id.strip() + patient.strip()
        encoded_patient = client_patient.encode()
        hash_patient = hashlib.sha1(encoded_patient)
        patient_id = hash_patient.hexdigest()
        patient_hash_list.append(patient_id)

    return patient_hash_list


def determine_json_structure(json_data):
    """
        determines if meta data is a string object or a filepath
        Args:
            metadata (string): either file path, json string of metadata, or dictionary
        Returns:
            dict: dictionary depiction of metadata
    """
    # json data is None, or empty string
    if json_data is None or (isinstance(json_data, str) and json_data == ""):
        return {}

    # is already json instance
    if isinstance(json_data, dict) or isinstance(json_data, list):
        return json_data

    # json string
    if "{" in json_data or '[' in json_data:
        result = ast.literal_eval(json_data)
        return result
    else:
        # file path, open
        with open(json_data, 'r', encoding='UTF-8') as file:
            data = file.read()
            result = ast.literal_eval(data)
        return result


def retry_decorator(retries: int = 5, backoff_in_seconds: int = 1):
    ''' Decorator to retry a function on a 503 ServiceUnavailable exception

    This retry decorator uses exponential back off with a default value of 5 retries
    and 1 second for backoff

    Args:
        func (function): the function we wish to use the retry strategy on
        retries (int): optional paramter with the number of retries for the client call
        backoff_in_seconds (int): optional parameter the number of seconds to wait initially

    Returns:
        function: the wrapped function
    '''

    def rd(func):

        def retry(*args, **kwargs):
            for x in range(0, retries):
                try:
                    returned_value = func(*args, **kwargs)
                    break
                except ServiceUnavailable:
                    # exponential backoff
                    sleep = (backoff_in_seconds * 2**x)
                    time.sleep(sleep)
                except requests.exceptions.HTTPError:
                    sleep = (backoff_in_seconds * 2**x)
                    time.sleep(sleep)
                    returned_value = None
                except PropertiesTableException:
                    sleep = (backoff_in_seconds * 2**x)
                    time.sleep(sleep)
                    returned_value = None

            return returned_value

        return retry

    return rd


@retry_decorator()
def create_get_request(url, params={}, headers={}):
    """
        Creates a request to the url and returns the response in a dictionary
        Args:
            url (string): The requestes url
            params (dict): The parameters in the Url
            headers (dict): The values in the ehader
        Returns:
            dict: Response data in dictionary form
    """
    try:
        r = requests.get(url=url, params=params, headers=headers)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        print_error('get request to ' + url + ' failed ' + str(err))
        raise requests.exceptions.HTTPError()


@retry_decorator()
def create_post_request(url, body, params={}, headers={}):
    """
        Creates a request to the url and returns the response in a dictionary
        Args:
            url (string): The requestes url
            params (dict): The parameters in the Url
            headers (dict): The values in the ehader
            body ()
        Returns:
            dict: Response data in dictionary form
    """
    try:
        r = requests.post(url=url, params=params, headers=headers, data=body)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as err:
        print_error('post request to ' + url + ' failed ' + str(err))
        raise requests.exceptions.HTTPError()