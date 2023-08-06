#
#   Created By Ryan McDermott
#   Created On 5/13/2022
#
#   Top level file that hold all the logic for calling the executables. This
#   includes argument validations and implementing the sub modules for each
#   command

import sys
import click
from indxdatalaketools import __version__
from indxdatalaketools.ClientTools import ClientOps


@click.group()
@click.version_option(__version__)
def main():
    """ ALL CLIENT OPERATIONS """


#####
#   File Commands
#####
@main.group()
def files():
    """Commands for file operations"""


@files.command('upload')
@click.option('--service_account',
              default=None,
              help='The path to the service account key json file')
@click.option('--modality', default=None, help='The modality of the file')
@click.argument('client_id')
@click.argument('mrn')
@click.argument('metadata')
@click.argument('file_path')
def upload_file(client_id, modality, mrn, metadata, file_path, service_account):
    """\b\nupload a file
    
    Arguments: 
        
        CLIENT_ID:      The specific UUID4 for a client.
        MRN:            The Patients medical record number
        METADATA:       The json string or json file of the file you wish to upload.
                        The structure is:
            CLIENT_ID (REQUIRED):   String, UUID of client / health care agency
            PATIENT_ID:             String, UUID of patient
            MODALITY:               String, The modality of the file
            FILE_PATH:              String, The path in the datalake where the file is stored
            DATE_OF_SERVICE:        String, The date of service in
            TIME_OF_SERVICE:        String, The time of service in
            LOCATION_OF_SERVICE:    String, Where the file was created
            SOURCE:                 String, The Source of the file
            ORIGINATOR:             String, The user that uploaded the file to the data lake
        FILE_PATH:      The path to the file you wish to upload
        
    """
    file_client = ClientOps.Client(client_id,
                                   credentials_file_path=service_account)
    result = file_client.upload_file(mrn,
                                     metadata,
                                     file_path,
                                     modality=modality)
    sys.exit(int(not result))


@files.command('batch-upload')
@click.option('--service_account',
              default=None,
              help='The path to the service account key json file')
@click.argument('client_id')
@click.argument('file_name')
def batch_upload_file(client_id, file_name, service_account):
    """\b\nupload multiple files with the data in a csv file
    
    Arguments: 
        
        CLIENT_ID:      The specific UUID4 for a client.
        FILE_PATH:      The path to the file thats contains the upload data. The
            file must be a csv file with a header that contains each fields below.
            The order does not matter.
            

            MODALITY:       The files MODALITY. acceptable parameters are:
                HVF
                OCT_RNFL
                OCT_RETINA
                AVS
            MRN:            The Patients medical record number
            METADATA:       The json string or json file of the file you wish to upload.
                            The structure is:
                CLIENT_ID (REQUIRED):   String, UUID of client / health care agency
                PATIENT_ID:             String, UUID of patient
                MODALITY:               String, The modality of the file
                FILE_PATH:              String, The path in the datalake where the file is stored
                DATE_OF_SERVICE:        String, The date of service in
                TIME_OF_SERVICE:        String, The time of service in
                LOCATION_OF_SERVICE:    String, Where the file was created
                SOURCE:                 String, The Source of the file
                ORIGINATOR:             String, The user that uploaded the file to the data lake
            FILE_PATH:      The path to the file you wish to upload
        
    """
    file_client = ClientOps.Client(client_id,
                                   credentials_file_path=service_account)
    result = file_client.batch_file_upload(file_name)
    sys.exit(int(not result))


#####
#   PATIENTS Table Commands
#####
@main.group()
def patients_table():
    """Commands for PATIENTS table operations"""


@patients_table.command('upload')
@click.option('--service_account',
              default=None,
              help='The path to the service account key json file')
@click.argument('client_id')
@click.argument('patient_data')
def upload_patient(client_id, patient_data, service_account):
    """\b\nuploads a single, or multiple patients to the PATIENTS table
    
    Arguments: 
        
        CLIENT_ID:      The specific UUID4 for a client.
        PATIENT_DATA:   The json string, or json file representing a single, or 
                        multiple patients. The json structure is
            PATIENT_ID:             String, UUID of patient 
            CLIENT_ID (REQUIRED):   String, UUID of client / health care agency 
            MRN (REQUIRED):         String, patient’s medical record number per the client’s EMR system 
            LASTNAME:               String, patient’s last name 
            FIRSTNAME:              String, patient’s first name 
            MIDDLENAME:             String, patient’s middle name 
            DOB:                    Date, patient’s date of birth 
            SEX:                    String, patient’s administrative gender as per the HL7 code 
            RACE:                   String, patient’s race as per the HL7 code 
    """
    patients_table_client = ClientOps.Client(client_id, service_account)
    result = patients_table_client.upload_patient(patient_data)
    sys.exit(int(not result))


if __name__ == '__main__':
    main()