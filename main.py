from fetch_data import fetch_data
from process_data import process_data

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

if __name__ == "__main__":
    data = fetch_data(API_URL)
    results = process_data(data)
    print(results)
