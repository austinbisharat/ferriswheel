import json

from movies import MovieListing, MovieListingIndex

def main():
    movie_listings = []
    with open('top_imdb_movie_listings.json', 'r') as f:
        movie_listing_dicts = json.load(f)
        movie_listings = [MovieListing(**d) for d in movie_listing_dicts]

    index = MovieListingIndex()
    index.ingest_movie_listings(movie_listings)

    while True:
        search = input('enter search (or "q" to exit): ')
        if search == "q":
            break
        
        results = index.search_movie_listings(search)
        for r in results:
            print(f'\t{r.title}')
    
    
if __name__ == '__main__':
    main()                                  
