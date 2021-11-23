from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField

from community.models import Comment, Review
from movies.models import Movie


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)


class UserPKSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username')


class UserDetailSerializer(serializers.ModelSerializer):

    class ReviewSerializer(serializers.ModelSerializer):

        class MovieSerializer(serializers.ModelSerializer):

            class Meta:
                model = Movie
                fields = ('pk', 'title',)

        movie = MovieSerializer(read_only=True)

        class Meta:
            model = Review
            fields = ('pk', 'title', 'rank', 'movie',
                      'content', 'updated_at',)

    class CommentSerializer(serializers.ModelSerializer):
        class ReviewSerializer(serializers.ModelSerializer):

            class MovieSerializer(serializers.ModelSerializer):

                class Meta:
                    model = Movie
                    fields = ('pk', 'title')

            movie = MovieSerializer(read_only=True)

            class Meta:
                model = Review
                fields = ('pk', 'title', 'rank', 'movie',)

        review = ReviewSerializer(read_only=True)

        class Meta:
            model = Comment
            fields = ('pk', 'content', 'review', 'updated_at')

    class MovieSerializer(serializers.ModelSerializer):

        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path')

        SerializerMethodField

    reviews = ReviewSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like_movies = MovieSerializer(many=True, read_only=True)
    pick_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'reviews', 'comments',
                  'like_movies', 'pick_movies')
