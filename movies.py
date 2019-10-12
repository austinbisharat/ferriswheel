from collections import namedtuple

# Type used to represent a movie listing
MovieListing = namedtuple('MovieListing', ['title', 'cast', 'crew'])

class MovieListingIndex:
    """Simple class to represent a search index of movie listings"""
    def __init__(self):
        self.index = dict()

    def ingest_movie_listing(self, listing):
        pass

    def ingest_movie_listings(self, listings):
        for listing in listings:
            self.ingest_movie_listing(listing)

    def search_movie_listings(self, search_str):
        return []
