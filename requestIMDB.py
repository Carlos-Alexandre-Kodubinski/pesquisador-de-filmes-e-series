import re
import requests

#apiKey = 'k_1xopr4ks'
apiKey = 'k_1hd8grsy'
baseURL = 'https://imdb-api.com'

class IMDB:
    def base_search(self, url):
        information = requests.get(url)
        return information.json()

    
    def get_results_id(self, search):
        ids = []
        for num, id in enumerate(search['results']):
            ids.append({'id': id['id'], 'title': id['title'], 'image': id['image']})
        return ids


    def search_movies(self, movieName, lang='en'):
        url = f'{baseURL}/{lang}/API/SearchMovie/{apiKey}/{movieName}'
        return self.get_results_id(self.base_search(url))

    
    def search_series(self, serieName, lang='en'):
        url = f'{baseURL}/{lang}/API/SearchSeries/{apiKey}/{serieName}'
        return self.get_results_id(self.base_search(url))


    def search_title(self, titleID, lang='en', allResult=True):
        url = f'{baseURL}/{lang}/API/Title/{apiKey}/{titleID}'
        title = self.base_search(url)
        filtedResult = {
            'title': title['title'],
            'year': title['year'],
            'plot': title['plot'],
            'stars': title['stars'],
            'imDbRating': title['imDbRating'],
            'metacriticRating': title['metacriticRating']
        }
        if allResult:
            return title
        else:
            return filtedResult


    def get_genres_title(self, titleID, lang='en'):
        title = self.search_title(titleID)
        genres = title['genres']
        genres += ', Categories'
        return genres
