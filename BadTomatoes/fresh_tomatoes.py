import webbrowser
import requests
import os
import re
import urllib
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')


#It's not working!?!?!?!! Wait! You need a Google Api with youtube enabled!
#
# Read here to get setup. Then replace
# api_key = XXXX
# With your key
#
# https://developers.google.com/youtube/v3/getting-started
#

api_key = config.get('Keys', 'gapis')

import json
# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Bad Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 960px;
            height: 500px;

        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;

        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .flip-container {
            perspective: 1000;

        }
            /* flip the pane when hovered */
        .flip-container:hover .flipper, .flip-container.hover .flipper {
            transform: rotateY(180deg);
        }

        .flip-container, .front, .back {

        }

        /* flip speed goes here */
        .flipper {
            /*transition-delay: 0.4s;*/
            transition: 1.0s;
            transform-style: preserve-3d;

            position: relative;
        }

        /* hide back of pane during swap */
        .front, .back {
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;




        }

        .watched{
        opacity:0.5;
        }

        /* front pane, placed above back */
        .front {
            z-index: 2;
            /* for firefox 31 */
            transform: rotateY(0deg);

        }

        /* back, initially hidden pane */
        .back {
            position: absolute;
            top: 0;
            margin-left: auto;
            margin-right: auto;
            left: 0;
            right: 0;

            transform: rotateY(180deg);
        }

        .play-glyp{


            position: absolute;
            margin-top: -60px;
            top: 50%;
            margin-left: -60px;
            left: 50%;
            font-color:white;
            font-size: 120px;

        }

    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });

        // Remove Movie from Screen
        $(document).on('click', '.remover', function (event) {
            var tileId = $(this).attr('data-imdb');
            console.log(tileId);
            $("#"+tileId).remove();
        });

        //Add Class to Watched Film
        $(document).on('click', '.btn-watch', function (event) {
            var tileId = $(this).attr('data-imdb');
            console.log(tileId);
            $("#"+tileId).addClass("watched");
        });

        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.poster', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">

            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Internet Based Tomatoes & Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div id="{id}" class="col-md-6 col-lg-4 movie-tile text-center">
   <div class="flip-container">
   <div class="flipper">
    <div class="front">
        <img src="{poster_image_url}" class="poster" width="220" height="342" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
        <h3>{movie_title} ({year})</h3>
        <p style="">{plot}</p>
    </div>
    <div class="back">
        <div style="width:100%;">
        <div class="poster" style="position:relative;" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
         <img src="{poster_image_url}"  width="220" height="342">
         <span class="glyphicon glyphicon-play-circle play-glyp"> </span>
         </div>
         <h3>{movie_title} ({year})</h3>
         <span>  <button type="button" class="btn btn-default remover" data-imdb="{id}">Remove from List</button>
  <button type="button" class="btn btn-default btn-watch" data-imdb="{id}">Mark as Watched</button> </span>
         </div>
    </div>
    </div>
  </div>
</div>
'''
class Movie:



    def __init__(self, movieString):

        # Check to see if IMDB ID or Not
        checkMovieID = re.search(r'tt[0-9]{5,8}', movieString)


        if(checkMovieID):
            print("IMDB ID: "+movieString)
            movieData = self.searchOMDB(movieString)

        else:
            print("Searching For ID: "+movieString)
            movieData = self.searchOMDB(movieString)

        # Check for Errors
        if(movieData == False):
            print("Connection Error")
            self.valid = False
            return


        print ("Title: "+movieData['Title'])


        tSearch = movieData['Title']+" "+movieData['Year']+" Trailer";
        trailerData = self.searchYoutube(tSearch)

        if(movieData != False and trailerData != False):
            self.id = movieString
            self.trailer_youtube_url = "www.youtube.com/watch?v=" + trailerData['items'][0]['id']['videoId']
            self.title = movieData['Title']
            self.year = movieData['Year']
            self.poster_image_url = movieData['Poster']
            self.plot = movieData['Plot'][0:90] + "..."
            self.valid = True
        else:
            self.valid = False

        print(" ")
        print(" ")

    def searchOMDB(self, urlString):

        try:
            r = requests.get('http://www.omdbapi.com/?i='+urlString+'&r=json')
        except requests.exceptions.ConnectionError as e:
            print "Domain Issues! Please check your internet!"
            return False

        returnData = r.json()

        #Check Responses for Proper Structure
        errorChecks = ['Title', 'Year', 'Poster', 'Plot']

        for errorCheck in errorChecks:
            if errorCheck not in returnData:
                return False

        #Return Valid Data
        return returnData

    def searchYoutube(self, searchString):
        #Encode Search
        search = urllib.quote_plus(searchString)

        try:
            rT = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&order=relevance&q="+search+"&key="+api_key)
        except rT.exceptions.ConnectionError as e:
            print "Domain Issues! Please check your internet!"

        #Process JSON from Youtube
        returnData = json.loads(rT.text)

        #Print Youtube Title
        if  returnData['items'][0]['snippet']['title']:
            print returnData['items'][0]['snippet']['title']

        #Check for valid link
        if not returnData['items'][0]['id']['videoId']:
            print("No Trailer")
            return False

        return returnData

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:

        if(movie.valid == True):
            # Extract the youtube ID from the url
            youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
            youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
            trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

            # Append the tile for the movie with its content filled in
            content += movie_tile_content.format(
                year=movie.year,
                id=movie.id,
                plot=movie.plot,
                movie_title=movie.title,
                poster_image_url=movie.poster_image_url,
                trailer_youtube_id=trailer_youtube_id
            )
    return content

def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

#open_movies_page()