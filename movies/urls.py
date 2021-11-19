from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # 최신 영화 리스트
    path("", views.movies_lastest),

    path("top/", views.movies_top),

    # 좋아요 영화 리스트 및 좋아요 기능
    path("like/", views.movies_like),

    # 찜한 영화 리스트 및 찜 기능
    path("pick/", views.movies_pick),

    # 장르별 영화 리스트
    path("<int:genre_pk>/genres/", views.movies_genre),

    # 단일 영화 상세 정보 조회
    path("<int:movie_pk>/", views.detail),

    path("youtube/", views.youtube),

    # 사용자 영화 추천
    path("recommend/", views.recommend)
]
