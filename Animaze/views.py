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
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import requests
from Animaze.models import Anime
from Animaze.serializers import searchDisplay

@api_view(['GET'])
@permission_classes([AllowAny])
def search_anime(q=None, *args, **kwargs):
        data = {}
        if q!=None and q == "" :
                lookup=Q(name__icontains=q)
                data_db = Anime.objects.filter(lookup)
                if data_db.count() == 0:
                        x = requests.get(f"https://kitsu.io/api/edge//anime?filter[text]={q}")
                        data = x.json()["data"][0]['attributes']
                        data = Anime.objects.create(name = data['canonicalTitle'],rating=data['averageRating'],created=data['createdAt'],description=data['description'],poster=data['posterImage']['large'])
                        data = searchDisplay(instance = data)        
                else:
                        data = searchDisplay(instance = data_db.first())
        return Response(data = data.data, status=status.HTTP_200_OK)