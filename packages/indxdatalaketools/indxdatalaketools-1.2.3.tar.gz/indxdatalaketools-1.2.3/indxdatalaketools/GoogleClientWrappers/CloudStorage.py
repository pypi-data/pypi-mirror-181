#
#   Created By Ryan McDermott
#   Created on 5/4/2022
#
import google.cloud.storage
import uuid
from google.api_core.exceptions import ServiceUnavailable
from indxdatalaketools import Helpers
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from indxdatalaketools.Helpers import retry_decorator


class Wrapper:
    '''
        Wrapper for Google Cloud Storage python SDK
    '''
    __google_cloud_storage_client = None

    def __init__(self):
        self.__google_cloud_storage_client = GcpClients.instance(
        ).get_storage_client()

    def find_blobs_with_metadata(self, bucket, key, value, path_prefix=''):
        '''
            Finds every file with with the metadata matching the key and value pairs
            provided. Can also set a prefix to narrow down the available searches
            Args:
                key (string): The metadata key
                value (string): the metadata value
                path_prefix (string): blob path prefix
            Returns:
                list: list containing all blobs with mathcing metadata
        '''
        blobs = []
        for blob in self.__google_cloud_storage_client.list_blobs(
                bucket, prefix=path_prefix):
            if blob.metadata is not None and key in blob.metadata and blob.metadata[
                    key] == value:
                blobs.append(blob.name)

        return blobs

    @retry_decorator()
    def check_if_bucket_exists(self, bucket_name):
        '''
            checks if the bucket name passed exists
            Args:
                bucket_name (string): the name of the bucket
            Returns:
                boolean: True if the bucket exists, False if otherwise
        '''
        try:
            self.__google_cloud_storage_client.get_bucket(bucket_name)
            return True
        except ServiceUnavailable:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print("bucket " + bucket_name + " does not exist")
            return False

    def upload_file_to_gcs_bucket(self, mrn, file_path, prefix, client_uuid):
        '''
            uploads file to specified folder in data lake - prefix determines the folder
            args:
                mrn: str - user input mrn
                file_path: str - local file path of file to upload
                prefix: str - folder on data lake where we want file to be placed
            return:
                upload_result: boolean - true if file upload successful, false if failure encountered
        '''
        if 'gs://' in file_path:
            bucket_name = file_path.replace("gs://", '').split('/')[0]
            gcs_file_path = file_path.replace("gs://" + bucket_name + "/", '')
            blob_name = prefix + "/" + mrn + "_" + str(
                uuid.uuid4()) + "_" + file_path.split('/')[-1]
            source_bucket = self.__google_cloud_storage_client.bucket(
                bucket_name)
            destination_bucket = self.__google_cloud_storage_client.bucket(
                client_uuid)
            blob = source_bucket.blob(gcs_file_path)
            blob_copy = self.copy_blob(source_bucket, blob, destination_bucket,
                                       blob_name)

            if blob_copy is not None and blob_copy.exists():
                return blob_copy
            return False
        else:
            file_path = file_path.replace("\\", "/")
            file_name = file_path.split("/")[-1]
            blob_name = prefix + "/" + mrn + "_" + str(
                uuid.uuid4()) + "_" + file_name
            bucket = self.__google_cloud_storage_client.bucket(client_uuid)
            blob = bucket.blob(blob_name)
            upload_result = self.__upload_blob_from_local(blob, file_path)

            if not upload_result:
                return upload_result
            return blob

    @retry_decorator()
    def copy_blob(self, source_bucket: google.cloud.storage.Bucket,
                  blob: google.cloud.storage.Blob,
                  destination_bucket: google.cloud.storage.Bucket,
                  blob_name: str) -> google.cloud.storage.Blob:
        '''copies blob from one gcs location to another

        This private function is a wrapper to the gcs client copy_blob function to catch
        any exceptions during run time

        Args:
            source_bucket (google.cloud.storage.Bucket): The bucket we wish to copy from
            blob (google.cloud.storage.Blob): The gcs blob we wish to copy
            destination_bucket (google.cloud.storage.Bucket): the bucket we wish to move the blob to
            blob_name (string): the new name of the blob
        Returns:
            google.cloud.storage: The new blob copy
        '''
        try:
            return source_bucket.copy_blob(blob,
                                           destination_bucket,
                                           new_name=blob_name)
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error(e)
            return None

    @retry_decorator()
    def __upload_blob_from_local(self, blob, file_path):
        '''
            applies gcs api to upload a file from local to blob on gcs
            args:
                blob: gcs blob object
                file_path: local file path of file to be uploaded
            return:
                boolean: true is success and false if failure encountered
        '''
        try:
            blob.upload_from_filename(file_path)
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            Helpers.print_error("Could not connect to GCS client " + str(e))
            return False
