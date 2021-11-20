from rest_framework import serializers
from django.contrib.auth import get_user_model

from community.models import Comment, Review
from movies.models import Movie


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)


class UserDetailSerializer(serializers.ModelSerializer):

    class reviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ('pk', 'title',)

    class commentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('pk', 'content',)

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('pk', 'title')

    reviews = reviewSerializer(many=True, read_only=True)
    comments = commentSerializer(many=True, read_only=True)
    like_movies = MovieSerializer(many=True, read_only=True)
    pick_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'reviews', 'comments',
                  'like_movies', 'pick_movies')
