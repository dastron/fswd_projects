__author__ = 'edanford'
import fresh_tomatoes

movies=[]

#List of IMDB Movies ID's to fetch data
myMovies=["tt0114709", "tt0133093", "tt0110912", "tt0268978", "tt0088763", "tt3659388", "tt0068646", "tt0468569", "tt0108052", "tt0796366", "tt2039393","tt0062622", "tt0361748", "tt0116282", "tt0401792", "tt0107290", "tt0107048", "tt0073195" ]


for b in range(0,len(myMovies)):
    movies.append(fresh_tomatoes.Movie(myMovies[b]))
fresh_tomatoes.open_movies_page(movies)

