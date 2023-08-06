#
#   Created by Ryan McDermott
#   Created on 3/2/2022
#   Updated on 9/30/2022: Changed class to singleton
#

from __future__ import annotations
import json

import google.auth

from google.cloud import logging
from google.cloud import storage
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1
from google.cloud import datastore
from google.cloud import pubsub_v1
from google.cloud import scheduler_v1
from google.cloud import tasks_v2
from google.cloud import secretmanager

from google.oauth2 import service_account
from google.cloud.compute_v1.services import instances
from google.cloud.compute_v1.services import zone_operations

import os.path


class GcpClients:
    """A singleton class to hold all gcs clients.

    This class hold all gcp clients to use throughout your code. 
    Pass in credentials upon first use of the GcpClients class and they will be saved. If
    a certain gcp client has not been initialized on its first "get_..." it will be initialized.
        

    Typical usage example:

        gcs_client = GcpClients.instance().get_gcs_client()
    """
    _credentials = None
    _instance = None
    _logging_client = None
    _storage_client = None
    _bigquery_client = None
    _bigquery_storage_v1_client = None
    _datastore_client = None
    _secretmanager_client = None
    _pubsub_v1_client = None
    _tasks_v2_client = None
    _scheduler_v1_client = None
    _compute_engine_instance_client = None
    _compute_engine_operation_client = None
    _account_credentials_client = None

    def __init__(self):
        '''This will throw a RunTimeError.

        Will never be able to instanciate this object.
        call GcpClients.instance() instead

        Raises:
            RuntimeError: Always raises runtime error
        '''
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, credential_file: str | None = None) -> GcpClients:
        '''singleton design pattern, call this function to get the singleton

        Static method that returns the instance of the GcpClients object. If the instance is none,
        a new GcpClients will be created. This is the only way to use the object.

        Args:
            credential_file (str, optional): The credentials used to 
                authenticate to GCP, defaults to None
        Returns:
            GcpClients: The GcpClients singleton
        Raises:
            FileNotFoundError: if the passed credentials do not exist
            ValueError: if the passed credentials file is not a json

        '''
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            if credential_file is not None and not os.path.isfile(
                    credential_file):
                raise FileNotFoundError(
                    "The Credential file path does not exist!")
            if credential_file is not None:
                # will raise ValueError if the credential file is not json
                json.load(open(credential_file))

            cls._instance._credentials = credential_file

        return cls._instance

    def get_credentials(self) -> str | None:
        ''' Gets the current credentials

        Returns:
            str | None: the credentials passed to the GcpClients Singleton
        '''
        return self._credentials

    def get_logging_client(self) -> logging.Client:
        '''Gets the authenticated GCP logging client.

        If the current logging client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            google.cloud.logging.Client: The authenticated logging client
        '''
        if self._logging_client is None:
            if self._credentials is not None:
                self._logging_client = logging.Client.\
                from_service_account_json(self._credentials)

            else:
                self._logging_client = logging.Client()
        return self._logging_client

    def get_storage_client(self) -> storage.Client:
        '''Gets the authenticated GCP storage client.

        If the current storage client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            google.cloud.storage.Client: The authenticated storage client
        '''
        if self._storage_client is None:
            if self._credentials is not None:
                self._storage_client = storage.Client.\
                from_service_account_json(self._credentials)
            else:
                self._storage_client = storage.Client()
        return self._storage_client

    def get_bigquery_client(self) -> bigquery.Client:
        '''Gets the authenticated GCP bigquery client.

        If the current bigquery client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            google.cloud.bigquery.Client: The authenticated bigquery client
        '''
        if self._bigquery_client is None:
            if self._credentials is not None:
                self._bigquery_client = bigquery.Client.\
                from_service_account_json(self._credentials)
            else:
                self._bigquery_client = bigquery.Client()
        return self._bigquery_client

    def get_bigquery_storage_v1_client(
            self) -> bigquery_storage_v1.BigQueryWriteClientClient:
        '''Gets the authenticated GCP bigquery_storage_v1 Write client.

        If the current bigquery_storage_v1 Write client has not 
        been initialized then one will be created with the credentials in the GcpClient.

        Returns:
            google.cloud.bigquery_storage_v1.BigQueryWriteClientClient: 
                The authenticated bigquery client
        '''
        if self._bigquery_storage_v1_client is None:
            if self._credentials is not None:
                self._bigquery_storage_v1_client = bigquery_storage_v1.BigQueryWriteClient.\
                from_service_account_json(self._credentials)
            else:
                self._bigquery_storage_v1_client = bigquery_storage_v1.BigQueryWriteClient(
                )
        return self._bigquery_storage_v1_client

    def get_datastore_client(self) -> datastore.Client:
        '''Gets the authenticated GCP datastore client.

        If the current datastore client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            datastore.Client: The authenticated datastore client
        '''
        if self._datastore_client is None:
            if self._credentials is not None:
                self._datastore_client = datastore.Client.\
                from_service_account_json(self._credentials)
            else:
                self._datastore_client = datastore.Client()

        return self._datastore_client

    def get_secretmanager_client(
            self) -> secretmanager.SecretManagerServiceClient:
        '''Gets the authenticated GCP secretmanager client.

        If the current secretmanager client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            secretmanager.SecretManagerServiceClient: The authenticated secretmanager client
        '''
        if self._secretmanager_client is None:
            if self._credentials is not None:
                self._secretmanager_client = secretmanager.SecretManagerServiceClient.\
                from_service_account_json(self._credentials)
            else:
                self._secretmanager_client = secretmanager.SecretManagerServiceClient(
                )

        return self._secretmanager_client

    def get_pubsub_v1_client(self) -> pubsub_v1.Client:
        '''Gets the authenticated GCP pubsub_v1 client.

        If the current pubsub_v1 client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            pubsub_v1.Client: The authenticated pubsub_v1 client
        '''
        if self._pubsub_v1_client is None:
            if self._credentials is not None:
                self._pubsub_v1_client = pubsub_v1.PublisherClient.\
                from_service_account_json(self._credentials)
            else:
                self._pubsub_v1_client = pubsub_v1.PublisherClient()

        return self._pubsub_v1_client

    def get_tasks_v2_client(self) -> tasks_v2.CloudTasksClient:
        '''Gets the authenticated GCP tasks_v2 client.

        If the current tasks_v2 client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            scheduler_v1.CloudSchedulerClient: The authenticated tasks_v2 client
        '''
        if self._tasks_v2_client is None:
            if self._credentials is not None:
                self._tasks_v2_client = tasks_v2.CloudTasksClient.\
                from_service_account_json(self._credentials)
            else:
                self._tasks_v2_client = tasks_v2.CloudTasksClient()

        return self._tasks_v2_client

    def get_scheduler_v1_client(self) -> scheduler_v1.CloudSchedulerClient:
        '''Gets the authenticated GCP scheduler_v1 client.

        If the current scheduler_v1 client has not been initialized then one will be created 
        with the credentials in the GcpClient.

        Returns:
            scheduler_v1.CloudSchedulerClient: The authenticated scheduler_v1 client
        '''
        if self._scheduler_v1_client is None:
            if self._credentials is not None:
                self._scheduler_v1_client = scheduler_v1.CloudSchedulerClient.\
                from_service_account_json(self._credentials)
            else:
                self._scheduler_v1_client = scheduler_v1.CloudSchedulerClient()

        return self._scheduler_v1_client

    def get_compute_engine_instance_client(self) -> instances.InstancesClient:
        '''Gets the authenticated GCP compute engine instance client.

        If the current compute engine instance client has not been initialized 
        then one will be created with the credentials in the GcpClient.

        Returns:
            instances.InstancesClient: The authenticated compute engine instance client
        '''
        if self._compute_engine_instance_client is None:
            if self._credentials is not None:
                self._compute_engine_instance_client = instances.InstancesClient.\
                from_service_account_json(self._credentials)
            else:
                self._compute_engine_instance_client = instances.InstancesClient(
                )

        return self._compute_engine_instance_client

    def get_compute_engine_operation_client(
            self) -> zone_operations.ZoneOperationsClient:
        '''Gets the authenticated GCP compute engine operation client.

        If the current compute engine operation client has not been initialized 
        then one will be created with the credentials in the GcpClient.

        Returns:
            zone_operations.ZoneOperationsClient: The authenticated compute engine operation client
        '''
        if self._compute_engine_operation_client is None:
            if self._credentials is not None:
                self._compute_engine_operation_client = zone_operations.ZoneOperationsClient.\
                from_service_account_json(self._credentials)
            else:
                self._compute_engine_operation_client = zone_operations.ZoneOperationsClient(
                )

        return self._compute_engine_operation_client

    def get_account_credentials_client(self) -> service_account.Credentials:
        '''Gets the authenticated GCP service account credentials.

        If the current service account credentials has not been initialized 
        then one will be created with the credentials in the GcpClient.

        Returns:
            service_account.Credentials: The authenticated service account credentials
        '''
        if self._account_credentials_client is None:
            if self._credentials is not None:
                self._account_credentials_client = service_account.Credentials.\
                from_service_account_file(filename=self._credentials,
                scopes=['https://www.googleapis.com/auth/cloud-platform'])
            else:
                account_cred, _ = google.auth.default()
                self._account_credentials_client = account_cred

        return self._account_credentials_client
