from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    # 단일 리뷰 상세 정보 조회 / 수정 / 삭제
    path("<int:review_pk>/", views.review),

    #  리뷰 생성 및 리뷰 리스트 조회
    path("<int:movie_pk>/reviews/", views.create_list_review),

    # 댓글 생성
    path("<int:review_pk>/comments/", views.create_comment),

    # 댓글 수정 삭제
    path("<int:review_pk>/comments/<int:comment_pk>/", views.comment),
]
