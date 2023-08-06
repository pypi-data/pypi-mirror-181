#
#   Created by Ryan McDermott
#   Created on 3/11/2022
#

import datetime

from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage_v1 import writer
from google.protobuf import descriptor_pb2

from indxdatalaketools import Helpers
from indxdatalaketools.GoogleClientWrappers import BigQuery
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients


class Client:
    ''' Class that inserts data into the changelog table '''
    client_uuid = ''
    table_fields = [
        "CLIENT_ID", "BUCKET_ID", "FILE_PATH", "FILE_NAME", "ACTION",
        "ACTION_AT", "REPLICATED", "REPLICATED_AT"
    ]

    __big_query_wrapper = None

    def __init__(self, client_uuid):
        '''
            Init function that sets up client credentials, uuid, 
            and google api clients used to insert items to the Patients table
            Args:
                google_clients          (ApiClients): object containing all Google Api Clients
                client_uuid             (string): The client's uuid
            Returns:
                None
        '''
        self.client_uuid = client_uuid
        logging_client = GcpClients.instance().get_logging_client()
        self.__changelog_insert_logger = logging_client.logger(
            client_uuid + '-changelog-logger')
        self.__big_query_wrapper = BigQuery.Wrapper()

    def insert_to_changelog_table(self, blob, action):
        ''' 
            Inserts information from an uploaded blob to the changelog table
            Args:
                blob (google.cloud.storage.Blob): The blob that was uploaded
            Returns:
                boolean: True if the data was inserted into the changelog table
        '''
        blob_data_dict = self.__create_upload_dict(blob, action)
        dataset_id = 'SNAPSHOTS_' + self.__transform_client_id()
        today = self.__get_date_today()

        return self.__insert_data_to_changelog(dataset_id, today,
                                               blob_data_dict)

    def __create_upload_dict(self, blob, action):
        '''
            Creates a dictionary with all of the data for the table
            Args:
                blob   (google.cloud.storage.Blob): The blob that was 
                    created, updated, or deleted
                action (string): the action being taken
            Returns:
                dict: The dictionary containing all of the data
        '''
        time_now = self.__get_datetime_now()

        client_id = self.client_uuid
        bucket_id = self.client_uuid
        file_path = blob.metadata['FILE_PATH']
        file_name = str(blob.name).split('/')[-1]
        action_at = time_now
        replicated = False

        return {
            'CLIENT_ID': client_id,
            'BUCKET_ID': bucket_id,
            'FILE_PATH': file_path,
            'FILE_NAME': file_name,
            'ACTION': action,
            'ACTION_AT': action_at,
            'REPLICATED': replicated
        }

    def __get_datetime_now(self):
        '''
            Gets the current datetime for now and returns it
            Returns:
                datetime: The datetime of now
        '''
        now = datetime.datetime.utcnow()
        time_now_string = now.strftime('%Y-%m-%d %H:%M:%S')

        return time_now_string

    def __transform_client_id(self):
        '''
            Transforms the client id to contain no dashes and have all
            letters uppercase:
            Args:
                None
            Returns:
                string: transformed string
        '''
        client_id = self.client_uuid
        client_id = client_id.replace('-', '')
        client_id = client_id.upper()

        return client_id

    def __get_date_today(self):
        '''
            creates a date string in YYYYMMDD format by using the date today 
            Returns:
                string: Date today in YYYYMMDD format
        '''
        today = datetime.datetime.utcnow()
        today_date = today.date()
        today = today_date.strftime('%Y%m%d')

        return str(today)

    def __insert_data_to_changelog(self, dataset_id, table_name,
                                   changelog_data):
        '''
            Function that inserts data into the changelog table
            Args:
                dataset_id        (string): The id of the data set
                table_name        (string): The name of the table
                changelog_data    (dict): The Patients Data
            Returns
                Boolean: True if the request worked, false if other wise
        '''
        return self.__big_query_wrapper.insert_to_bq_table(
            [changelog_data],
            'indx-data-services.' + dataset_id + '.' + table_name)
