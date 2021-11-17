from django.shortcuts import render

# Create your views here.


def create_review(request, movie_pk):
    # 리뷰 생성
    pass


def review(request, movie_pk, review_pk):
    # 리뷰 수정 삭제
    pass


def create_comment(request, review_pk):
    # 댓글 생성
    pass


def comment(request, review_pk):
    # 댓글 수정 삭제
    pass
