#
#   Created by Ryan McDermott
#   Created on 7/7/2022
#

import google_crc32c
from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from google.api_core.exceptions import ServiceUnavailable
from indxdatalaketools.Helpers import print_error
from indxdatalaketools.Helpers import retry_decorator


class Wrapper:
    ''' Wrapper for all secret manager client API Calls'''

    def __init__(self):
        ''' Nothin to initialize'''
        pass

    @retry_decorator()
    def get_secret(self, project_id, secret_id, version_id='latest'):
        '''
            Function that returns a secret found in secret manager
            Args:
                project_id (string): The project id where the secret is
                secret_id (string): The id of the secret
                version_id (string): The version of the sercet, defauls to latest
            Returns:
                string: The secret
        '''
        try:
            name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
            response = GcpClients.instance().get_secretmanager_client().\
                access_secret_version(request={"name": name})

            # Verify payload checksum.
            crc32c = google_crc32c.Checksum()
            crc32c.update(response.payload.data)
            if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
                print_error("Data corruption detected for secret id" +
                            secret_id)
                return ''
            payload = response.payload.data.decode("UTF-8")
            return payload
        except ServiceUnavailable:
            raise ServiceUnavailable('503 retry')
        except Exception as err:
            print_error('problem accessing secret ' + name + ' ' + str(err))
            return ''
