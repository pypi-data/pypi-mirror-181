#
#   Created by Ryan McDermott
#   Created on 5/12/2022
#

import datetime
import time
from indxdatalaketools import DataLakeGlobals
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from indxdatalaketools.PropertiesDBApi import Properties
from indxdatalaketools.ArgumentValidation import Argument

from indxdatalaketools.DataStandardizer import FileMetadata, PatientTable
from indxdatalaketools.ClientTools.Files import Upload
from indxdatalaketools.ClientTools.PatientsTable import Insert
from indxdatalaketools.DocumentClassifierApi import DocumentClassifierApi
from indxdatalaketools.GoogleClientWrappers import CloudStorage
from indxdatalaketools import Helpers
import warnings


class Client:

    client_uuid = ''

    __argument_validator = None

    def __init__(self, client_uuid, credentials_file_path=None):
        '''
            Init function that sets up client credentials, uuid, 
            and File operations API
            Args:
                credentials_file_path   (string): The path to a Service Account key json file
                client_uuid             (string): The client's uuid
            Returns:
                None
        '''
        self.client_uuid = client_uuid

        GcpClients.instance(credential_file=credentials_file_path)
        self.__client_ops_logger = GcpClients.instance().get_logging_client(
        ).logger(client_uuid + '-file-logger')
        if self.client_uuid == 'indx-test-client-datalake':
            self.__throughput_logger = GcpClients.instance().get_logging_client(
            ).logger(client_uuid + '-throughput')
        self.__argument_validator = Argument.Validator()
        self.__document_classifier = DocumentClassifierApi.DocClassifierClient()

    def upload_file(self, mrn, metadata, file_path, modality=None):
        '''
            Top level function that uploads a file to a Datalake, This will aslo add the 
            Patient data to the PATIENTS table if applicable
            Args:
                modality    (string): The modality of the file
                mrn         (string): The mrn of who the file belongs to
                metadata    (dict|string|file_path): Any metadata belonging to the file
                file        (string): The file path of the file we wish to upload
            Returns:
                boolean: True if the operation was a success, False if otherwise
        '''
        # validate arguments
        arguments = {
            'client_id': self.client_uuid,
            'mrn': mrn,
            'file_metadata': metadata,
            'file_path': file_path
        }

        if modality is not None:
            arguments['modality'] = modality

        data_lake_command = 'file'

        Properties.Properties.instance()

        if not self.__argument_validator.validate_all_arguments(
                arguments, data_lake_command):
            return False

        return self.__standardize_and_run_file_upload(arguments)

    def batch_file_upload(self, file_path: str) -> bool:
        ''' Uploads multiple files found in a csv file

        Top level function that uploads multiple files to a datalake in one command,
        The file must contain the modality, mrn, metadata and file path for each file.

        Args:
            - file_path (str): The path to the batch file
        
        Returns:
            bool: True if all files were uploaded to the datalake, False if otherwise
        '''
        arguments = {'client_id': self.client_uuid, 'batch_file': file_path}
        data_lake_command = 'file'

        start = time.time()
        Properties.Properties.instance()

        if not self.__argument_validator.validate_all_arguments(
                arguments, data_lake_command):
            return False

        list_of_files = Helpers.read_batch_file(file_path)

        if self.client_uuid == 'indx-test-client-datalake':
            finish = time.time()
            upload_time = finish - start
            self.__throughput_logger.log_text(
                "It took " + str(upload_time) + " seconds to validate " +
                str(len(list_of_files) - 1) + " records",
                severity="INFO")

        failed_uploads = self.__upload_files_from_list(list_of_files, start)

        if len(failed_uploads) == 0:
            return True

        for i in failed_uploads:
            Helpers.print_error("Failure uploading patient " + i[1]['mrn'] +
                                " on line " + str(i[0]))

        return False

    def __upload_files_from_list(self, list_of_files, start):
        '''loops through passed list and inserts files to the datalake

        This function loops through the list passed and insertes each file into the clients datalake
        all errors and upload times are logged.
        
        Args:
            list_of_files (list): the list of file data we wish to upload
            start (time.time): the start time of the operation
        Returns:
            list: the list of files that did not get processed

        '''
        header = list_of_files[0]
        failed_uploads = []
        modality_index = header.index('MODALITY')
        mrn_index = header.index('MRN')
        metadata_index = header.index('METADATA')
        file_path_index = header.index('FILE_PATH')

        # skip header
        for row in range(1, len(list_of_files)):
            modality = list_of_files[row][modality_index]
            mrn = list_of_files[row][mrn_index]
            metadata = list_of_files[row][metadata_index]
            file_path = list_of_files[row][file_path_index]

            arguments = {
                'client_id': self.client_uuid,
                'modality': modality,
                'mrn': mrn,
                'file_metadata': metadata,
                'file_path': file_path
            }
            result = self.__standardize_and_run_file_upload(arguments)

            if not result:
                failed_uploads.append((row, arguments))

            if result and self.client_uuid == 'indx-test-client-datalake':
                finish = time.time()
                upload_time = finish - start
                self.__throughput_logger.log_text(
                    str(row) + " (" + str(DataLakeGlobals.SIZE_OF_FILES) +
                    " MB) files have been processed in " + str(upload_time) +
                    "seconds",
                    severity="INFO")

        return failed_uploads

    def upload_patient(self, patient_data):
        '''
            Top level function that uploads a patient to a PATIENT table, This will also update missing
            patient data but not overwrite it.
            Args:
                patient_data (dict): Dictionary containing the data to insert a patient to the patient table
            Returns:
                boolean: True if the operation was a success, False if otherwise
        '''
        # verify inputs
        arguments = {
            'client_id': self.client_uuid,
            'patient_data': patient_data
        }
        data_lake_command = 'patients-table'

        Properties.Properties.instance()

        if not self.__argument_validator.validate_all_arguments(
                arguments, data_lake_command):
            return False

        # clean data
        data_standardizer = PatientTable.Client()
        patient_data = data_standardizer.standardize(patient_data)

        # run the command
        return Insert.Client(
            self.client_uuid).insert_data_to_patients_table(patient_data)

    def __document_classifier_operations(self, mrn, file_path):
        '''
            function that handles operations required to run the document classifier. This includes uploading file from local to 
            a staging folder on the clients data lake, running the document classifier with this uploaded blob and then deleting the blob
            args:
                mrn: str - input mrn
                file_path: str - local file path of input file
            return:
                classified_modality: str - modaity prediction of the document classifier
        '''
        blob = CloudStorage.Wrapper().upload_file_to_gcs_bucket(
            mrn, file_path, "staging_folder", self.client_uuid)
        if not blob:
            return blob

        gcs_file_path = "gs://" + blob.bucket.name + "/" + blob.name
        classified_modality, classified_file_type = self.__send_request_to_document_classifier(
            gcs_file_path)

        return classified_modality

    def __standardize_and_run_file_upload(self, arguments: dict) -> bool:
        ''' Standardizes the arguments and data then uploads the file to the datalake.

        standradizes the agruments passed then calls the file upload command.

        Args:
            arguments (dict): the arguments to be passed to the file upload command

        Returns:
            bool: True if the file was successfully uploaded. False if otherwise
        '''
        # standardize the metadata
        file_metadata_standardizer = FileMetadata.Standardizer(arguments)
        file_metadata = file_metadata_standardizer.standardize(
            arguments['file_metadata'])

        # run the document classifier, check if modality matches predicted modality
        classified_modality = self.__document_classifier_operations(
            arguments['mrn'], arguments['file_path'])

        if 'modality' not in arguments:
            arguments['modality'] = classified_modality

        if not classified_modality or classified_modality is None:
            classified_modality = 'Failed To Classify'
            arguments['modality'] = 'UNKNOWN'
            warnings.warn("Request to document classifier failed.")
            self.__client_ops_logger.log_text(
                'failed to run document classifier on file ' +
                arguments['file_path'],
                severity='WARNING')
        elif classified_modality != arguments['modality']:
            Helpers.print_error(
                "Modality may be incorrect. Modality might be " +
                classified_modality)

        file_metadata['CLASSIFIED_MODALITY'] = classified_modality

        if 'MODALITY' not in file_metadata:
            file_metadata['MODALITY'] = arguments['modality']

        if 'FILE_PATH' not in file_metadata:
            file_metadata['FILE_PATH'] = str(file_metadata['MODALITY']) + \
            '/' + str(file_metadata['PATIENT_ID'])

        # run command
        return Upload.Client(self.client_uuid).upload_file_to_datalake(
            arguments['modality'], arguments['mrn'], file_metadata,
            arguments['file_path'])

    def __send_request_to_document_classifier(self, gcs_file_path):
        '''
            runs the document classifier
            args:
                gcs_file_path: str gcs path of file in staging folder
            return:
                classified_modality: str - modality prediction of the document classifier
                classified_file_type: str - file type prediction of the document classifier
        '''
        try:
            return self.__document_classifier.get_modality_and_file_type(
                gcs_file_path)
        except Exception as e:
            print("Error when trying to run document classifier. " + str(e))
            return False, False