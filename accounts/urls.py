from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),


    path("follow/<int:user_id>/", views.FollowUserView.as_view(), name="follow"),
    path("unfollow/<int:user_id>/", views.UnfollowUserView.as_view(), name="unfollow"),
    path("followers/<int:user_id>/", views.FollowersListView.as_view(), name="followers-list"),
    path("following/<int:user_id>/", views.FollowingListView.as_view(), name="following-list"),
]
