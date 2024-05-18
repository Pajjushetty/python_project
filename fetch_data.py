import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def fetch_data(api_url):
    results = []
    page = 1

    # Set up retry logic
    session = requests.Session()
    retry = Retry(
        total=5, 
        backoff_factor=1, 
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    while True:
        try:
            logger.debug(f"Fetching data from page {page}")
            response = session.get(api_url, params={'page': page})
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response text: {response.text}")

            if response.status_code != 200:
                logger.error(f"Failed to fetch data: {response.status_code} - {response.text}")
                break

            data = response.json()
            logger.debug(f"Data received: {data}")

            if 'error' in data:
                logger.error(f"API error: {data['error']}")
                break

            if not data:
                logger.debug(f"No more data available at page {page}")
                break

            results.extend(data)
            page += 1

        except requests.exceptions.RequestException as e:
            logger.exception(f"An error occurred while fetching data: {e}")
            break

    return results

def identify_citations(response, sources):
    citations = []
    for source in sources:
        # Checking if source context is in response
        if source['context'].strip().lower() in response.strip().lower():
            citation = {'id': source['id']}
            if 'link' in source and source['link']:
                citation['link'] = source['link']
            citations.append(citation)
    return citations

def process_data(data):
    results = []
    for item in data:
        logger.debug(f"Processing item: {item}")  # Log each item to inspect structure
        if isinstance(item, dict):
            response = item.get('response', "")
            sources = item.get('sources', [])
            citations = identify_citations(response, sources)
            results.append(citations)
        else:
            logger.warning(f"Unexpected data format: {item}")
    return results

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"
    data = fetch_data(API_URL)
    if data:
        results = process_data(data)
        print(results)
    else:
        logger.error("No data fetched from API.")
