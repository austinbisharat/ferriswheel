# ferriswheel
Simple imdb search for ferriswheel.ai

## How to Run
This project requires python 3.6, Flask, and BeautifulSoup 4. There are three included python executables: one for scraping IMDB, one for a simple CLI for searching, and one for a simple web server exposing a search endpoint.

To run the webscraper: `python fetch_listings.py`. This will update `top_imdb_movie_listings.json` to have the most up-to-date information, but is not required to get up and running.

To run the CLI: `python cli_search.py`. This will read in `top_imdb_movie_listings.json`, create and index, then offer a very simple search functionality in a loop. I found this easier to use for testing than the server

To run the web server: `python server.py` This will read in `top_imdb_movie_listings.json`, create and index, then offer a very simple search functionality. To hit the endpoint, you can test with `curl -H 'Content-type: application/json' -X POST localhost:8080/search/ -d '{"search": "hanks"}'`

Note: my implementation indexes _all_ cast and crew for a movie that is listed on the full detail page for a movie. It's debatable if this is a bug or a feature, as searching for "hanks" now cannot distinguish between "Tom Hanks" and the lesser known "David Hanks" who was an equipment engineer for The Goonies. 

## Overview of design
The project is broken roughly into three different layers:
- The web scraper. This layer is responsible for scraping IMDB and formatting movie listings in a format that the index can use
- The search index module. This layer offers an interface for indexing movie listings and searching for them. The index is a simple map of keyword to the set of movie listings that have that keyword associated with it. Lookup requires performing N-1 set intersections where N is the number of search terms.
- The API layer. Both the CLI and the web server offer ways to use the search index to expose functionality to the user, either in the form of a web server or a local CLI.

I felt that it was important to seperate the scraper from the search index so that the search index could offer a clean api that wouldn't have to change at the whims of IMDB's frontend team. I also felt it important to seperate the API layer so that the indexing code could be agnostic both to how the search occurs (via some web api, etc) _and_ how the listings that get indexed are loaded. In particular, we might imagine a world in which the search index becomes smart enough to update and delete listings. Then, we may want to offer an ingestion endpoint for new or updated movies in our server implementation.

## Future work
I spent about 2.5 hours on this project, most of which was spent on the scraping code. There is a lot I would have loved to build out provided more time:

- Tests:
  - Unit tests of the search index code
  - Integration tests of the scraping code (perhaps with a stubbed out requests implementation to avoid hitting imdb)
  - Integration tests of the server
  - Integration tests of the scraping code along with the API server which loads the serialized listings file
- Search Index improvements:
  - If I were doing this in production, I would prefer to use ElasticSearch or something of the like
  - Adding better stopwords and using TFIDF (or something of the like) to unlock ranking
  - Adding a way to update or delete listings in the index. This would probably require having an inverse index of document to keywords, or maybe even something more complicated to figure out how exactly to update the index
  - The current search index only offers doing boolean and over search terms. It might be nice to offer a way for searches to specify arbitrary boolean combinations, or at least something more useful than just and.
  - In that vain, seperating the search into search terms splits on whitespace only. This means that searching for "tom hanks" is nearly the same as searching for "hanks" because tom is such a common name. We might want to index n-grams for some n > 2. This also might allow us to offer searches that use quotes to denote a multiword term, so long as the number of words is <=n.
- API improvements
  - The current api is very barebones and doesn't offer very clear error handling. This could be improved
  - I did nothing to test performance and I am not sure what Flask does under the hood. This could likely be improved, especially if flask does not use asyncio
  - As mentioned above, it would be nice to offer an ingestion endpoint for movie listings
- Overall project improvements
  - It would be nice to work out a deployement/testing/release workflow. Currently, system dependancies are not reproducible at all. I have not done a lot of dev ops work, but containerizing in some form or another (hopefully in a way that is consistent with how the rest of the org does things) would offer some safety gains there
  - If this were a real project, I would want to see some form of automatic testing upon PR creation with Circle or Travis or something of the like
  
  
  
- 
