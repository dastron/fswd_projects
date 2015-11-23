# Welcome to Bad Tomatoes!

Complie a list of movies and track your progress as you watch them.

* A couple of key points, when running MovieLibrary.py, please make sure that you have a valid internet connect, Bad Tomatoes will pull the latest data from teh interwebs and search for a trailer for your movie library. Also give it a second, there are a lot of queries happening. 

If you want to increase the speed please remove items from myMovies.

# Setup!
It's not working!?!?!?!! Wait! You need a Google Api with youtube enabled!

 Read here to get setup. Then replace "api_key = XXXX" with your key!

 https://developers.google.com/youtube/v3/getting-started

## Added Features:

	1. OMDB (http://www.omdbapi.com/) intergration, simply list a title or IMDB Id and Bad Tomatoes will load the title, year, poster and plot information.

	2. Youtube trailer finder: Using hot key words like trailer combined with release year Bad Tomatoes will do it's best to find the a trailer (or a trailer) on youtube.

	3. Marked as Watched / Remover: Mark items as watch or remove them entirely.


##  Setup Instructions
	
	Extract to a folder. Run the MovieLibrary.py either from the:

		command line: python MovieLibrary.py
		or 
		From within an IDE. Run -> MovieLibrary.py
	
	*Make sure that Library.py & Fresh_Tomatoes.py are located in the same folder and have write permission