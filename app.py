from flask import Flask, jsonify, render_template_string
import logging
from fetch_data import fetch_data
from process_data import process_data

app = Flask(__name__)

API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template_string("""
        <!doctype html>
        <title>Citation Finder</title>
        <h1>Welcome to Citation Finder</h1>
        <p>Go to <a href="/citations">/citations</a> to see the citations.</p>
    """)

@app.route('/citations', methods=['GET'])
def get_citations():
    logger.debug("Fetching data from API...")
    data = fetch_data(API_URL)
    if data:
        logger.debug("Processing data...")
        results = process_data(data)
        print(results)
        logger.debug("Data processed successfully")
        return render_template_string("""
            <!doctype html>
            <title>Citations</title>
            <h1>Citations</h1>
            {% if results %}
                <ul>
                {% for result in results %}
                    <li>{{ result.field1 }} - {{ result.field2 }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No citations found.</p>
            {% endif %}
        """, results=results)
    else:
        logger.error("Failed to fetch data from API")
        return jsonify({"error": "Failed to fetch data from API"}), 500

if __name__ == "__main__":
    app.run(debug=True)
