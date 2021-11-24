from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from movies.serializers import MovieDetailSerializer, MovieSerializer

from .models import Genre, Movie

# Create your views here.


@api_view(['GET'])
def movies_top(request):
    movies = Movie.objects.order_by('-popularity', '-release_date')[:100]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def movies_lastest(request):
    movies = Movie.objects.order_by('-release_date')[:100]
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
    movies = genre.movies.order_by('-popularity', '-release_date')[:100]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def recommend_by_reviews(request):
    user = request.user
    reviews = user.reviews.all()
    likes = user.like_movies.all()

    if not reviews and not likes:
        return Response([], status=status.HTTP_200_OK)

    genres = {
        '액션': {'score': 0, 'count': 0},
        "모험": {'score': 0, 'count': 0},
        "애니메이션": {'score': 0, 'count': 0},
        "코미디": {'score': 0, 'count': 0},
        "범죄": {'score': 0, 'count': 0},
        "다큐멘터리": {'score': 0, 'count': 0},
        "드라마": {'score': 0, 'count': 0},
        "가족": {'score': 0, 'count': 0},
        "판타지": {'score': 0, 'count': 0},
        "역사": {'score': 0, 'count': 0},
        "공포": {'score': 0, 'count': 0},
        "음악": {'score': 0, 'count': 0},
        "미스터리": {'score': 0, 'count': 0},
        "로맨스": {'score': 0, 'count': 0},
        "SF": {'score': 0, 'count': 0},
        "TV 영화": {'score': 0, 'count': 0},
        "스릴러": {'score': 0, 'count': 0},
        "전쟁": {'score': 0, 'count': 0},
        "서부": {'score': 0, 'count': 0},
    }
    review_movies = []
    for review in reviews:
        review_movies.append(review.movie.title)
        for genre in review.movie.genres.all():
            genres[genre.name]['score'] += review.rank
            genres[genre.name]['count'] += 1

    for like in likes:
        if like.title not in review_movies:
            for genre in like.genres.all():
                genres[genre.name]['score'] += 7
                genres[genre.name]['count'] += 1

    for genre, data in genres.items():
        if data['count'] > 0:
            data['avg'] = round(data['score'] / data['count'])
        else:
            data['avg'] = 0

    def sorting_algorithm(movie):
        movie_score = 0
        movie_genres = movie.genres.all()
        for movie_genre in movie_genres:
            movie_score += genres[movie_genre.name]['avg']
        movie_score = round(movie_score / len(movie_genres))
        return (-movie_score, -movie.vote_average, -movie.vote_count)

    movies = Movie.objects.order_by('-popularity', '-release_date')[:500]
    movies = sorted(movies,
                    key=sorting_algorithm)

    def make_recommend_movies():
        recommend_movies = []
        for movie in movies:
            if movie not in likes and movie not in reviews:
                recommend_movies.append(movie)
                if len(recommend_movies) >= 30:
                    return recommend_movies
        return recommend_movies

    recommend_movies = make_recommend_movies()
    serializer = MovieSerializer(recommend_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def recommend_by_users(request):
    me = request.user
    me_like_movies = me.like_movies.all()
    users = get_user_model().objects.all()

    similar_users = sorted(users, key=lambda user: len(
        set(user.like_movies.all()).intersection(me_like_movies)))

    def make_recommend_movies():
        recommend_movies = set()
        for similar_user in similar_users:
            for like_movie in similar_user.like_movies.all():
                if like_movie not in me_like_movies:
                    recommend_movies.add(like_movie)
                    if len(recommend_movies) >= 30:
                        return recommend_movies
        return list(recommend_movies)

    recommend_movies = make_recommend_movies()

    serializer = MovieSerializer(recommend_movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def recommend_by_md(request):
    yun_picks = [
        "블랙 위도우", "프리 가이", "코코",
        "스파이더맨: 뉴 유니버스", "데드풀",
        "소울", "주토피아",  "라라랜드",
        "인사이드 아웃", "이터널 선샤인",
        "히든 피겨스", "나이브스 아웃", "굿모닝 에브리원",
        "인턴", "악마는 프라다를 입는다"
    ]
    sang_picks = [
        '포레스트 검프', "해리 포터와 죽음의 성물 2", "어바웃 타임",
        "나의 소녀시대", "러브 액츄얼리", "미드나이트 스카이",
        "1917", "라스트 홀리데이", "이프 온리", "에놀라 홈즈",
        "캐롤", "찰리와 초콜릿 공장", "크리스마스 스위치 - 한 번 더 바꿔?",
        "스파이더맨: 파 프롬 홈", "두 교황", "인셉션"
    ]

    yun_pick_movies = Movie.objects.filter(
        Q(title=yun_picks[0]) | Q(title=yun_picks[1]) | Q(title=yun_picks[2]) | Q(title=yun_picks[3]) |
        Q(title=yun_picks[4]) | Q(title=yun_picks[5]) | Q(title=yun_picks[6]) | Q(title=yun_picks[7]) |
        Q(title=yun_picks[8]) | Q(title=yun_picks[9]) | Q(title=yun_picks[10]) | Q(title=yun_picks[11]) |
        Q(title=yun_picks[12]) | Q(title=yun_picks[13]) |
        Q(title=yun_picks[14])
    )

    sang_pick_movies = Movie.objects.filter(
        Q(title=sang_picks[0]) | Q(title=sang_picks[1]) | Q(title=sang_picks[2]) | Q(title=sang_picks[3]) |
        Q(title=sang_picks[4]) | Q(title=sang_picks[5]) | Q(title=sang_picks[6]) | Q(title=sang_picks[7]) |
        Q(title=sang_picks[8]) | Q(title=sang_picks[9]) | Q(title=sang_picks[10]) | Q(title=sang_picks[11]) |
        Q(title=sang_picks[12]) | Q(title=sang_picks[13]) |
        Q(title=sang_picks[14])
    )

    yun_serializer = MovieSerializer(yun_pick_movies, many=True)
    sang_serializer = MovieSerializer(sang_pick_movies, many=True)

    res = {
        'yun': yun_serializer.data,
        'sang': sang_serializer.data,
    }
    return Response(res, status=status.HTTP_200_OK)
