import json

from flask import abort
from flask import Flask
from flask import request

from movies import MovieListing, MovieListingIndex

app = Flask(__name__)

_search_index = MovieListingIndex()
 
@app.route('/search/', methods = ['POST'])
def search_handler():
    if request.headers['Content-Type'] != 'application/json':
        abort(415)

    body = request.json
    if 'search' not in body:
        abort(400, "must include search in post body")

    results = _search_index.search_movie_listings(body['search'])
    titles = [r.title for r in results] 
    return json.dumps(titles)
    
if __name__ == "__main__":
    movie_listings = []
    with open('top_imdb_movie_listings.json', 'r') as f:
        movie_listing_dicts = json.load(f)
        movie_listings = [MovieListing(**d) for d in movie_listing_dicts]

    _search_index.ingest_movie_listings(movie_listings)
    app.run(port=8080)
