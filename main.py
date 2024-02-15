from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

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

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX,
        'q': query,
        'start': start_index
    }

    response = requests.get(search_url, params=params)
    search_results = []
    total_pages = 0
    if response.status_code == 200:
        search_data = response.json()
        items = search_data.get('items', [])

        for item in items:
            thumbnail = item.get('pagemap', {}).get('cse_thumbnail', [{}])[0].get('src', '/path-to-default-thumbnail.jpg')
            search_results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet'),
                'thumbnail': thumbnail
            })

        total_results = int(search_data.get('searchInformation', {}).get('totalResults', 0))
        total_pages = max((total_results + 9) // 10, 1)  # Make sure at least one page is shown
    else:
        print(f"Error: {response.status_code}")

    return render_template('results.html', query=query, search_results=search_results, page=page, total_pages=total_pages)

@app.route('/search/images', methods=['GET'])
def search_images():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    if not query:
        return render_template('index.html')

    start_index = (page - 1) * 10 + 1
    search_type = "image"

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX,
        'q': query,
        'searchType': search_type,
        'start': start_index
    }

    response = requests.get(search_url, params=params)
    image_results = []
    total_pages = 0
    if response.status_code == 200:
        search_data = response.json()
        items = search_data.get('items', [])
        for item in items:
            image = item.get('link', '/path-to-default-image.jpg')
            image_results.append({
                'title': item.get('title'),
                'link': image,
                'thumbnail': item.get('image', {}).get('thumbnailLink', '/path-to-default-thumbnail.jpg')
            })

        total_results = int(search_data.get('searchInformation', {}).get('totalResults', 0))
        total_pages = max((total_results + 9) // 10, 1)  # Make sure at least one page is shown

    else:
        print(f"Error: {response.status_code}")

    return render_template('image_results.html', query=query, image_results=image_results, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
