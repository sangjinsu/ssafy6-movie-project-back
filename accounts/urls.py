from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

app_name = 'accounts'
urlpatterns = [
    # 회원가입
    path('signup/', views.signup),

    # 회원 탈퇴
    path("delete/", views.delete),

    path('api-token-auth/', obtain_jwt_token),
    path("<username>/", views.profile),
]
