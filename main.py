from flask import Flask, render_template, request
import requests  # Import the requests library
import os

app = Flask(__name__)

# Replace 'your_api_key' with your actual Google Custom Search JSON API key
# Replace 'your_search_engine_id' with your actual search engine id obtained
# from your custom search engine configuration on Google
GOOGLE_API_KEY = os.environ['GOOGLEAPI']
GOOGLE_CX = os.environ['GOOGLEID']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    if not query:
        return render_template('index.html')

    start_index = (page - 1) * 10 + 1
    # Build the Google Custom Search API request URL
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX,
        'q': query,
        'start': start_index
    }

    # Issue a request to the Google API
    response = requests.get(search_url, params=params)
    search_results = []
    if response.status_code == 200:
        search_data = response.json()

        # Extract the search results
        items = search_data.get('items', [])
        for item in items:
            search_results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            })

        total_results = int(search_data.get('searchInformation', {}).get('totalResults', 0))
        total_pages = (total_results + 9) // 10

    else:
        # In a production environment, you should handle response errors appropriately.
        print(f"Error: {response.status_code}")

    return render_template('results.html', query=query,
                           search_results=search_results, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
