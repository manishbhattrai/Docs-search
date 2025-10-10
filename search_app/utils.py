from django.utils import timezone
from datetime import timedelta
import requests
from django.conf import settings
from .models import GoogleAPIKeys
import logging



logger = logging.getLogger(__name__)


def get_next_google_api_keys():

    keys = GoogleAPIKeys.objects.filter(status='inactive')

    for key in keys:
        deactivated_time = timezone.now() - key.deactivated_at
        if deactivated_time >= timedelta(hours=24):
            key.status = 'active'
            key.deactivated_at = None
            key.save()

    active_keys = GoogleAPIKeys.objects.filter(status='active').order_by('last_used')


    if not active_keys:
        logger.info('No active Google API keys found')
        raise Exception('No active Google API keys found')


    selected_key = active_keys[0]

    selected_key.usage_count += 1
    selected_key.last_used = timezone.now()
    selected_key.save()

    return selected_key



def search_query(query, document_types=None):

    if document_types is None:
        document_types = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt']

    '''
      Building file type filter string using the list comprehension

      which makes list like for example = ['filetype:pdf', 'filetype:doc'] 

     and joining to create a single string for example : 'filetype:pdf OR filetype:doc OR filetype:docx'

        '''

    filetype_filter = ' OR '.join([f'filetype:{doc_type}' for doc_type in document_types])

    '''
    Combining the original query with the filetype_filter.

    Suppose the query is 'AI research paper' and the filetype_filter is 'filetype:pdf OR filetype:doc OR filetype:docx'. 

    The resulting filtered_query would be: 

    'AI research paper (filetype:pdf OR filetype:doc OR filetype:docx)'

    '''
    filtered_query = f"{query} ({filetype_filter})"

    retry_count = 0
    max_tries = 8
    current_key = None

    while retry_count < max_tries:

        try:
            current_key = get_next_google_api_keys()

        except Exception as e:
            logger.error(f'Error getting next google api key: {e}')
            ##print(f'Error getting Google API keys: {e}')
            return []

        '''if current_key.status == 'inactive' and current_key.deactivated_at:
            deactivated_time = timezone.now() - current_key.deactivated_at
            if deactivated_time >= timedelta(hours=24):

                current_key.status = 'active'
                current_key.deactivated_at = None
                current_key.save()

            else:
                retry_count += 1
                continue'''

        api_url = f"https://www.googleapis.com/customsearch/v1?q={filtered_query}&key={current_key.key}&cx={current_key.cse_id}"

        response = requests.get(api_url)

        if response.status_code == 200:

            logger.info(f'Got response: {response}')
            search_results = response.json()
            return search_results.get('items',[])

        elif response.status_code in [403, 429]:
            current_key.status = 'inactive'
            current_key.deactivated_at = timezone.now()
            current_key.save()
            retry_count += 1

        else:
            logger.error(f'Error getting next google api key: {response.status_code}')
            ##print(f'Error getting Google API keys: {response.status_code}')


    return []

