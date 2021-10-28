# https://kitsu.io/api/edge//anime?filter[text]=<search_var>
# data = [
#         {
        # "attributes": {
        #         "createdAt": "2020-11-21T23:48:51.994Z",
        #         "description": "Just where do \"Curses,\" the fiendish spirits invisible to normal humans, come from? What is Sukuna Ryoumen, whose very existence grips the \"Jujutsu\" world in fear? And who exactly is Yuuji Itadori, the boy who recently became the center of attention in Jujutsu society? No need to fear, for Satoru Gojou, the strongest Jujutsu sorcerer, has the answers! From the new sorcerers in training to the enemies they face, Gojou provides all you need to know about Jujutsu and the inner workings of the institution who protect us from Curses: the Tokyo Jujutsu High School. [Written by MAL Rewrite]",
        #         "titles": {
        #             "en_jp": "Jujutsu Kaisen",
        #             "ja_jp": "呪術廻戦"
        #         },
        #         "canonicalTitle": "Jujutsu Kaisen",
        #         "abbreviatedTitles": [
        #             "Sorcery Fight"
        #         ],
        #         "averageRating": "70.23",
        #       
        #         "userCount": 119,
        #         "favoritesCount": 3,
        #         "startDate": "2018-12-03",
        #         "endDate": "2018-12-08",
        #         "nextRelease": null,
        #         "popularityRank": 10408,
        #         "ratingRank": 4141,
        #         "ageRating": "PG",
        #         "ageRatingGuide": null,
        #         "subtype": "ONA",
        #         "status": "finished",
        #         "tba": null,
        #         "posterImage": {
        #             "tiny": "https://media.kitsu.io/anime/poster_images/43748/tiny.jpg",
        #             "large": "https://media.kitsu.io/anime/poster_images/43748/large.jpg",
        #             "small": "https://media.kitsu.io/anime/poster_images/43748/small.jpg",
        #             "medium": "https://media.kitsu.io/anime/poster_images/43748/medium.jpg",
        #             "original": "https://media.kitsu.io/anime/poster_images/43748/original.jpg",
        #             "meta": {
        #                 "dimensions": {
        #                     "tiny": {
        #                         "width": 110,
        #                         "height": 156
        #                     },
        #                     "large": {
        #                         "width": 550,
        #                         "height": 780
        #                     },
        #                     "small": {
        #                         "width": 284,
        #                         "height": 402
        #                     },
        #                     "medium": {
        #                         "width": 390,
        #                         "height": 554
        #                     }
        #                 }
        #             }
        #         },
        #     },
        #     
#         },
#       ]
from django.http.response import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Q
import requests
from Animaze.models import Movie,Ratings
import json

api_key = "c2727ac4"

def make_json(movie_obj,rating_objs):
        data = {}
        data["Title"]=movie_obj.name
        data["Rated"]=movie_obj.rated
        data["Year"]= movie_obj.year
        data["Director"]=movie_obj.director
        data["Ratings"]=[]
        for x in rating_objs:
                data["Ratings"].append({"Source":x.source,"Value":x.value})
        return data

@api_view(['GET'])
@permission_classes([AllowAny])
def search_anime(request,q=None, *args, **kwargs):
        data = {}
        if q!=None and q != "" :
                movie_obj = Movie.objects.filter(name=q)
                rating_objs=[]
                if movie_obj.count() == 0:
                        data = requests.get(f"https://www.omdbapi.com/?apikey={api_key}&t=={q}")
                        data = data.json()
                        movie_obj = Movie.objects.create(name = data["Title"],rated=data["Rated"],year=data["Year"],director=data["Director"])
                        rating = data["Ratings"]
                        for x in rating:
                                rating_objs.append(Ratings.objects.create(movie=movie_obj,source=x["Source"],value=x["Value"]))   
                else:
                        movie_obj = movie_obj.first()
                        rating_objs = Ratings.objects.filter(movie=movie_obj)
                data = make_json(movie_obj=movie_obj,rating_objs=rating_objs)
        return JsonResponse(data,safe=False)