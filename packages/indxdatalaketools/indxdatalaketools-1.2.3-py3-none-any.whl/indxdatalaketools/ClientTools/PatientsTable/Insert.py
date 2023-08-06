#
#   Created by Ryan McDermott
#   Created on 2/21/2022
#

import datetime
import time

from indxdatalaketools.ClientTools.PatientsTable import Update
from indxdatalaketools import Helpers
from indxdatalaketools.GoogleClientWrappers import BigQuery
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients


class Client:
    '''
        Class that contains all the functionality to insert a patient into
        The patient table
    '''

    client_uuid = ''
    dataset_id = ''
    patient_table_name = ''
    table_fields = [
        "CLIENT_ID", "MRN", "PATIENT_ID", "FIRSTNAME", "MIDDLENAME", "LASTNAME",
        "DOB", "SEX", "RACE", 'CHECKSUM', 'UPDATED_AT'
    ]
    __patient_insert_logger = None

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
        self.dataset_id = self.client_uuid.replace("-", "_")
        self.patient_table_name                 = 'indx-data-services.' + \
            self.dataset_id + ".PATIENTS"
        self._bq_wrapper = BigQuery.Wrapper()
        logging_client = GcpClients.instance().get_logging_client()
        self.__patient_insert_logger = logging_client.logger(client_uuid +
                                                             '-patient-logger')

    def insert_data_to_patients_table(self, patient_json, overwrite=False):
        '''
            This function determines whether the patient_json is a list
            or a single patient. Then it uploads all patient data to the PATIENT 
            table for the client_id
            Args:
                patient_json    (json): Either a json object or a JSON Array containing
                    multiple patients data
                overwrite       (boolean): Flag to indicat whether or not we can overwrite the patients 
                    data
            Returns: 
                boolean: True if the patient/s were succesfully inserted in the PATIENTS table
        '''
        # parse json to determine single or multiple patients

        # multiple patients
        if isinstance(patient_json, list):
            return self.__insert_multiple_patients_to_table(patient_json,
                                                            overwrite=overwrite)

        return self.__insert_patient_to_patients_table(patient_json,
                                                       overwrite=overwrite)

    def __insert_multiple_patients_to_table(self,
                                            json_structure,
                                            overwrite=False):
        '''
            loops through json structure and inserts all patients into the PATIENTS
            table, if a patient is not successfully uploaded then it is logged and
            the process continues.
            Args:
                json_structure (dict[]): list of dictionarys containing the patients data
                overwrite (boolean): Flag to indicate whether or not the row needs to get
                    overwritten
            Returns:
                boolean: True if the operation was a success False if otherwise
        '''
        status = True
        for i in json_structure:
            if self.__insert_patient_to_patients_table(i, overwrite=overwrite):
                continue
            else:
                status = False

        if status == False:
            self.__patient_insert_logger.log_text(
                'One or more patients have not been uploaded Successfully',
                severity='ERROR')

        self.__patient_insert_logger.log_text(
            'All patients have been uploaded Successfully', severity='INFO')
        return status

    def __insert_patient_to_patients_table(self, patient_data, overwrite=False):
        '''
            Function that adds a single patient to the patient table, if that patient already exists
            in the table their data is updated with the provided information
            Args:
                patient_data    (dict): The data we wish to add to the patient table
                overwrite       (boolean): Flag to indicate whether or not we can over 
                    write the patients data
            Returns:
                boolean: True if the operation was a success, false if otherwise
        '''
        now = datetime.datetime.utcnow()
        patient_data['UPDATED_AT'] = str(now).replace(' ', 'T')
        patient_mrn = patient_data['MRN']
        patient_partition = patient_data['PATIENT_PARTITION']
        patient_id = Helpers.patient_hash(self.client_uuid, [patient_mrn])[0]
        patient_row = self.__get_patient_in_patients_table(
            patient_mrn, patient_id, patient_partition)

        result = self.__insert_data_to_patients_table(patient_data,
                                                      patient_row,
                                                      overwrite=overwrite)
        return result

    def __get_patient_in_patients_table(self, patient_mrn, patient_id,
                                        patient_partition):
        '''
            performs a query look up on the PATIENTS table to find if the given patient
            exists in the PATIENTS table
            Args:
                patient_mrn (string): The patients mrn
                patient_id  (string): The patients UUID
            Returns:
                The row of the Patient, if they are not in the table None is returned
        '''
        query = 'SELECT * \
                    FROM `' + self.patient_table_name + '`\
                    WHERE MRN =\'' + patient_mrn + '\'\
                    AND PATIENT_ID =\'' + patient_id + '\'\
                    AND (PATIENT_PARTITION =' + str(patient_partition) + '\
                    OR PATIENT_PARTITION = 4000)'

        rows = BigQuery.Wrapper().perform_query(query)

        if rows is None:
            return None

        if rows.total_rows == 0:
            return None
        if rows.total_rows > 1:
            Helpers.print_error(
                "CRITICAL: Error in PATIENTS table, multiple instances of MRN: "
                + patient_mrn + " and PATIENT_ID " + patient_id)

        # must only contain one row if not 0 and > 1
        return next(rows)

    def __insert_data_to_patients_table(self,
                                        patient_data,
                                        patient_row,
                                        overwrite=False):
        '''
            Inserts data to the patients table, if the data needs to be updated it will overwrite
            if the flag is set
            Args:
                patient_data (dict): The dictionary of the patients data
                patient_row  (row): The row already existing in the patients table
                overwrite    (boolean): True if we wish to overwrite the existing data in the 
                    PATIENTS table
            Returns:
                boolean: True if the operations was successful, False if otherwise
        '''
        if patient_row is not None:
            # patient exists, updated patient in table
            # check if patient partition is 4000
            if patient_row.get('PATIENT_PARTITION') == 4000:
                patient_data['PATIENT_PARTITION'] = 4000

            return Update.Client(
                self.client_uuid).update_patient_in_patient_table(
                    patient_data, patient_row, overwrite=overwrite)
        elif overwrite == False:
            # patient ID has never been inserted, add to todays partition
            patient_data['PATIENT_PARTITION'] = 4000
            return self.__add_data_to_patient_table(patient_data)
        else:
            Helpers.print_error("patient does not exist cannot update")
            return False

    def __add_data_to_patient_table(self, patient_data):
        '''
            Adds the patients data to the PATIENT table using the Big Query 
            Storage API COMMITTED row type to bypass the streaming buffer
            Args:
                patient_data    (dict): The Patients Data
            Returns
                Boolean: True if the request worked, false if other wise
        '''
        result = self._bq_wrapper.insert_to_bq_table(
            [patient_data],
            'indx-data-services.' + self.dataset_id + '.PATIENTS')

        if result == True:
            self.__patient_insert_logger.log_text(
                str(patient_data) + ' has been succesfully uploaded',
                severity='INFO')
        else:
            self.__patient_insert_logger.log_text(str(patient_data) +
                                                  ' could not be uploaded',
                                                  severity='ERROR')
        return result
