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
        if isinstance(item, dict):  # Ensure item is a dictionary
            response = item.get('response', "")
            sources = item.get('sources', [])
            citations = identify_citations(response, sources)
            results.append(citations)
        else:
            print(f"Unexpected data format: {item}")  # Log unexpected data format
    return results

# Example usage
if __name__ == "__main__":
    data = [
        {"response": "This is a sample response with a citation.", "sources": [{"id": 1, "context": "sample response", "link": "http://example.com"}]},
        "This is an invalid item",  # This string will trigger the type check
        {"response": "Another response.", "sources": [{"id": 2, "context": "another response"}]}
    ]
    results = process_data(data)
    print(results)
