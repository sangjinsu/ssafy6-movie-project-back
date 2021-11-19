from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.serializers import MovieDetailSerializer, MovieSerializer

from .models import Genre, Movie

import requests

# Create your views here.


@api_view(['GET'])
def movies_top(request):
    movies = Movie.objects.order_by('-popularity', '-release_date')[:3]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movies_lastest(request):
    movies = Movie.objects.order_by('-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def movies_like(request):

    if request.method == 'GET':
        user = request.user
        movies = user.like_movies.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        movie_pk = request.data.get('movieId')
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
def movies_pick(request):

    if request.method == 'GET':
        user = request.user
        movies = user.pick_movies.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        movie_pk = request.data.get('movieId')
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.pick_users.filter(pk=request.user.pk).exists():
            movie.pick_users.remove(request.user)
        else:
            movie.pick_users.add(request.user)
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def movies_genre(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.order_by('-popularity', '-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def youtube(request):
    movie_title = request.data.get('title')
    API_URL = 'https://www.googleapis.com/youtube/v3/search'
    YOUTUBE_API_KEY = 'AIzaSyC5RMAkEJWF1MHT9s39WiPH6mEUfBF-U1A'
    payload = {
        'key': YOUTUBE_API_KEY,
        'part': 'snippet',
        'q': movie_title + ' 예고편',
        'type': 'video',
    }
    result = requests.get(url=API_URL, params=payload).json()
    return Response(result, status=status.HTTP_200_OK)


def recommend(request):
    pass
