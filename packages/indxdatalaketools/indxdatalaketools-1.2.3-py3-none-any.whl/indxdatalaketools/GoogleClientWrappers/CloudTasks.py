#
#   Created By Ryan McDermott
#   Created on 6/14/2022
#

from indxdatalaketools.GoogleClients.GoogleClients import GcpClients
from google.api_core.exceptions import ServiceUnavailable
from indxdatalaketools.Helpers import print_error
from indxdatalaketools.Helpers import retry_decorator


class Wrapper:
    '''
        Wrapper for Google Cloud Storage python SDK
    '''
    __google_cloud_tasks_client = None

    def __init__(self):
        self.__google_cloud_tasks_client = GcpClients.instance(
        ).get_tasks_v2_client()

    @retry_decorator()
    def create_http_task(self, parent, task):
        '''
            Function that creates an http task
            Args:
                - parent (string): The name of the task queue 
                    (projects/{project}/locations/{location}/queues/{queue name})
                - task (dict): Dictionary containing the task information
            Returns:
                - boolean: True if the task was created, False if otherwise
        '''
        try:
            response = self.__google_cloud_tasks_client.\
                create_task(request={"parent": parent, "task": task})
            print("Created task {}".format(response.name))
            return True
        except ServiceUnavailable as e:
            raise ServiceUnavailable('503 retry')
        except Exception as e:
            print_error(e)
            return False