from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from movies.serializers import MovieSerializer

from .models import Genre, Movie

# Create your views here.


@api_view(['GET'])
def movies_top(request):
    movie = Movie.objects.order_by(
        '-popularity',  '-vote_count', '-vote_average',  '-release_date').first()
    movie_genres = movie.genres.all()
    new_genres = []
    for mg in movie_genres:
        new_genres.append(mg.name)
    serializer = MovieSerializer(movie)
    return Response({'data': serializer.data, 'genres': new_genres}, status=status.HTTP_200_OK)


@api_view(['GET'])
def movies_lastest(request):
    movies = Movie.objects.order_by('-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def movies_like(request):
    user = request.user
    movies = user.like_movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def movies_pick(request):
    user = request.user
    movies = user.pick_movies.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movies_genre(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.order_by(
        '-popularity',  '-vote_count', '-vote_average',  '-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_genres = movie.genres.all()
    new_genres = []
    for mg in movie_genres:
        new_genres.append(mg.name)
    serializer = MovieSerializer(movie)
    return Response({'data': serializer.data, 'genres': new_genres}, status=status.HTTP_200_OK)


def like(request, movie_pk):
    pass


def pick(request, movie_pk):
    pass


def recommend(request):
    pass
