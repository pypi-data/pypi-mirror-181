#
#   Created by Ryan McDermott
#   Created on 3/16/2022
#

from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import ServiceUnavailable
from indxdatalaketools import Helpers
from indxdatalaketools.DataLakeGlobals import DATASET_OWNER
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from indxdatalaketools.Helpers import print_error
from google.cloud.bigquery.enums import EntityTypes
from indxdatalaketools.Helpers import retry_decorator


class Wrapper:
    '''
        Wrapper for Google Cloud Platform Big Query python SDK
    '''

    __google_big_query_client = None
    file_format_map = {
        'AVRO': bigquery.SourceFormat.AVRO,
        'CSV': bigquery.SourceFormat.CSV
    }

    def __init__(self):
        self.__google_big_query_client = GcpClients.instance(
        ).get_bigquery_client()

    @retry_decorator()
    def insert_to_bq_table(self, patient_data, table_name):
        '''
            Function that inserts data into a big query table
            Args:
                patient_data (list): a list of dictionaries containing  patient data
                table_name (string): the name of the table we want to insert to
            Returns:
                boolean: True if the data was inserted, False if otherwise
        '''
        try:
            errors = GcpClients.instance().get_bigquery_client(
            ).insert_rows_json(table_name, patient_data)
            if errors == []:
                return True
            print_error(errors)
            return False
        except ServiceUnavailable:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print_error(str(e))
            return False

    @retry_decorator()
    def batch_load_from_gcs(self, gcs_uri, table_destination, file_format):
        '''
            Batch loads a file from gcs into big query
            Args:
                gcs_uri (string): the gcs uri of the file we wish to load into big query
                table_destination (string): The destination table
                file_format (string): the file format we are loading into big query 
                    (AVRO, CSV)
            Returns:
                boolean: True if the operation was successful, False if otherwise
        '''
        job_config = bigquery.LoadJobConfig(
            use_avro_logical_types=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=self.file_format_map[file_format])
        try:
            load_job = self.__google_big_query_client.load_table_from_uri(
                gcs_uri, table_destination,
                job_config=job_config)  # Make an API request.
            load_job.result()
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print_error(str(e))
            return False

    def create_dataset_if_not_exist(self, dataset_id, location):
        '''
            Creates the client's Dataset if it does not already exist
            Args:
                dataset_id (string): The id of the dataset for the table
                location (string): The location of the dataset
            Returns:
                boolean: True if the dataset already exists or was created, False if otherwise
        '''
        dataset = self.get_dataset(dataset_id)

        if dataset is None:
            return False

        dataset.location = location
        # Check if dataset exists
        if self.check_if_dataset_exists(dataset_id):
            print("Dataset {} already exists, skipping this step".format(
                dataset_id))
            return True

        print("Creating dataset: " + dataset_id)

        return self.create_dataset(dataset)

    @retry_decorator()
    def get_dataset(self, dataset_id):
        '''
            Gets the dataset in bigquery
            Args:
                dataset_id (string): The dataset Id we wish to retrieve or create
            Returns:
                google.cloud.bigquery.Dataset
        '''
        try:
            return bigquery.Dataset(dataset_id)
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error('Could not retreive dataset ' + dataset_id +
                                " " + str(e))
            return None

    def create_table_if_not_exist(self,
                                  dataset_id,
                                  table_name,
                                  schema,
                                  partition=None,
                                  clustering=None):
        '''Creates the client's PATIENT table if it does not already exist

        This function also takes in optional partitions and clustering for the table to be
        created

        Args:
            dataset_id (string): The id of the dataset for the table
            table_name (string): The name of the table we wish to create
            schema (list): a list of bigquery.SchemaField representing the table schema
        Returns:
            boolean: True if the table was created or already existed, false
                if table creation failed
        '''
        # create table object
        table_id = dataset_id + "." + table_name
        table = bigquery.Table(table_id, schema=schema)
        if partition is not None:
            table.range_partitioning = bigquery.RangePartitioning(
                # To use integer range partitioning, select a top-level REQUIRED /
                # NULLABLE column with INTEGER / INT64 data type.
                field=partition,
                range_=bigquery.PartitionRange(start=0, end=4000, interval=1),
            )

        if clustering is not None:
            table.clustering_fields = clustering

        if self.check_if_table_exists(table_id):
            print(
                "Table {} already exists, skipping this step".format(table_id))
            return True

        print("Creating table " + table_id)
        return self.create_table(table)

    @retry_decorator()
    def create_table(self, table):
        '''
            Creates Big Query Table
            Args:
                table (bigquery.Table): The table we wish to create
            returns:
                bigquery.Table: The created Table
        '''
        try:
            self.__google_big_query_client.create_table(table)
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error("ERROR in creating table: " + str(e))
            return False

    @retry_decorator()
    def create_dataset(self, dataset):
        '''
            Creates Big Query Dataset
            Args:
                dataset (bigquery.Dataset): The dataset we wish to create
            returns:
                None
        '''
        try:
            self.__google_big_query_client.create_dataset(dataset, timeout=30)
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error("Could not connect to GCS client " + str(e))
            return False

    @retry_decorator()
    def check_if_table_exists(self, table_id):
        '''
            Checks if the table Id passed exists on GCP
            Args:
                dataset_id (string): The table {PROJECT_ID}.{CLIENT_UUID}.PATIENTS
                retries (int): Optional parameter for the number of retries this function will do
            Returns:
                boolean: True if the table exists, false if other wise
        '''
        try:
            self.__google_big_query_client.get_table(
                table_id)  # Make an API request.
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except NotFound:
            return False
        except Exception as e:
            print(str(e))
            return False

    @retry_decorator()
    def check_if_dataset_exists(self, dataset_id):
        '''
            Checks if the dataset ID passed exists on GCP
            Args:
                dataset_id (string): The dataset {PROJECT_ID}.{CLIENT_UUID}
            Returns:
                boolean: True if the datset exists, false if other wise
        '''
        try:
            self.__google_big_query_client.get_dataset(
                dataset_id)  # Make an API request.
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except NotFound:
            return False
        except Exception as e:
            print(str(e))
            return False

    @retry_decorator()
    def delete_table(self, table_id):
        '''
            Deletes a table
            Args:
                table_id (string): The table id (your-project.your_dataset.your_table)
            Returns:
                boolean: True if the table was deleted false if otherwise
        '''
        try:
            self.__google_big_query_client.delete_table(table_id)
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print_error('Failed to Delete table: ' + table_id + " " + str(e))
            return False

    @retry_decorator()
    def perform_query(self, query, job_config=None):
        '''Performs a bigquery query

        An optional job config can be passed, usually used when querying clustered data

        Args:
            query (string): the query we wish to perform
            job_config(google.cloud.bigquery.JobConfig): an optional job configuration for
                the query
        Returns:
            query_job: The job of the query 
        '''
        try:
            query_job = self.__google_big_query_client.query(
                query, job_config=job_config)
            rows = query_job.result()
            return rows
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error('Could not connect to GCS Big Query ' + str(e))
            return None

    def set_permissions_on_dataset(self, dataset_id, role, account):
        '''
            Function that sets the permissions of a dataset
            Args:
                dataset_id (string): The dataset
                role (string): The role we want the account to have
                account (string): The account we are giving permission to
            Returns:
                boolean: True if the permissions were set, False if otherwise
        '''
        dataset = self.get_dataset(dataset_id)
        entity_type = EntityTypes.USER_BY_EMAIL
        entries = list(dataset.access_entries)
        # need to add an owner role to the dataset to set the SA permissions
        entries.append(
            bigquery.AccessEntry(
                role='roles/bigquery.dataOwner',
                entity_type=entity_type,
                entity_id=DATASET_OWNER,
            ))
        entries.append(
            bigquery.AccessEntry(
                role=role,
                entity_type=entity_type,
                entity_id=account,
            ))

        dataset.access_entries = entries

        return self.update_dataset(dataset, ["access_entries"])

    @retry_decorator()
    def update_dataset(self, dataset, fields):
        '''
            Updates a dataset with the fields passed
            Args:
                dataset (bigquery.Dataset): The dataset we wish to update
                fields (list): list of fields we wish to update
            Returns:
                boolean: True if the dataset was updated
        '''
        try:
            self.__google_big_query_client.update_dataset(dataset, fields)
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print_error(e)
            return False
