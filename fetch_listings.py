import requests
import re
import json

from bs4 import BeautifulSoup

from movies import MovieListing

def get_top_1000_movie_links():
    """
    Fetch a list of 'fullcredits' links for the top 1000 imdb movies.

    This makes several HTTP calls to imdb
    """
    movie_links = []
    for start in range (1, 1000, 50):
        imdb_movie_list_page = requests.get(f'https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&start={start}')
        soup = BeautifulSoup(imdb_movie_list_page.text, 'html.parser')

        movie_list_div = soup.find('div', attrs={'class': 'lister list detail sub-list'})
        movie_item_spans = movie_list_div.find_all('span', attrs={'class':'lister-item-header'})
        links = [item.find('a').attrs['href'] for item in movie_item_spans]

        movie_links += links

    return [f'https://www.imdb.com{l}fullcredits/' for l in movie_links]


def get_movie_listing_for_movie_link(link):
    """
    For a link to an imdb 'fullcredits'link for a movie, create and return a MovieListing.

    This makes an HTTP request to imdb
    """
    detailPage = requests.get(link)
    soup = BeautifulSoup(detailPage.text, 'html.parser')

    titleDiv = soup.find('div', attrs={'class': 'subpage_title_block__right-column'})
    titleText = titleDiv.find('a').text
    
    contentBodyDiv = soup.find('div', attrs={'id': 'fullcredits_content'})
    crew = [nameTd.text.strip() for nameTd in contentBodyDiv.find_all('td', attrs={'class': 'name'})]

    castListTable = soup.find('table', attrs={'class': 'cast_list'})
    castListRows = castListTable.find_all('tr', attrs={'class': re.compile('even|odd')})
    castList = [row.find_all('td')[1].text.strip() for row in castListRows]

    return MovieListing(titleText, castList, crew)

def main():
    print("Fetching top 1000 imdb movie links...")
    movie_links = get_top_1000_movie_links()
    movie_listings = []
    print("Done fetching top 1000 imdb movie links\n")
    
    print("Fetching detailed listings...")
    for i, link in enumerate(movie_links):
        if i % 10 == 0:
            print(f'... done fetching detailed listings for {i} links')
        movie_listings.append(get_movie_listing_for_movie_link(link))

    print("Done fetching detailed listings\n")

    jsonable_movie_listings = [ml._asdict() for ml in movie_listings]
    with open('top_imdb_movie_listings.json', 'w') as f:
        json.dump(jsonable_movie_listings, f)
   
if __name__ == '__main__':
    main()                                  
