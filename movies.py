from collections import namedtuple

# Type used to represent a movie listing
MovieListing = namedtuple('MovieListing', ['title', 'cast', 'crew'])

class MovieListingIndex:
    """Simple class to represent a search index of movie listings"""
    def __init__(self):
        self.index = dict()

    def ingest_movie_listing(self, listing):
        for keyword in _get_keywords_for_movie_listing(listing):
            if keyword not in self.index:
                self.index[keyword] = set()

            self.index[keyword].add(listing)

    def ingest_movie_listings(self, listings):
        for listing in listings:
            self.ingest_movie_listing(listing)

    def search_movie_listings(self, search_str):
        search_terms = search_str.split():
        if len(search_terms) == 0:
            return []

        results = self.index.get(search_terms[i], set())
        for term in search_terms[1:]:
            results_for_term = self.index.get(search_terms[i], set())

            # this always does a logical "and" for search terms. This
            # is a pretty major simplification
            results = results.intersection(results_for_term)
            
        return list(results)


MOVIE_LISTING_STOP_WORDS = {
    'the',
    # TODO
    }

def _get_keywords_for_movie_listing(listing):
    lowercase = (k.lower() for k in _get_raw_keywords_for_movie_listing(listing))
    return (k for k in lowercase if k not in MOVIE_LISTING_STOP_WORDS)

def _get_raw_keywords_for_movie_listing(listing):
    for keyword in listing.title.split():
        yield keyword

    for name in listing.cast:
        for keyword in name.split():
            yield keyword

    for name in listing.crew:
        for keyword in name.split():
            yield keyword
    
