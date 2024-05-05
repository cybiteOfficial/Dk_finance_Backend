from django.urls import path
from user_auth import views

urlpatterns = [
    # User Authentication endpoints
    path("signup", views.SignUpView.as_view()),
    path("signin", views.SignInView.as_view()),

    # User endpoints for CRUD
    path("user", views.UserView.as_view()),
]
