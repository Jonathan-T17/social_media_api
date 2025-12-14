from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from notifications.utils import create_notification

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    SimpleUserSerializer
)

# Use Django’s custom user model
User = get_user_model()   # <-- This ensures: CustomUser.objects.all() is used everywhere


# -----------------------------------
# REGISTER
# -----------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()     # <-- Includes CustomUser.objects.all()
    serializer_class = RegisterSerializer


# -----------------------------------
# LOGIN
# -----------------------------------
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


# -----------------------------------
# PROFILE
# -----------------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# -----------------------------------
# FOLLOW USER
# -----------------------------------
class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)

        if target == request.user:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        if target != request.user:
            create_notification(recipient=target, actor=request.user, verb="started following you", target=request.user)
            
        return Response({"detail": f"You are now following {target.username}."})


# -----------------------------------
# UNFOLLOW USER
# -----------------------------------
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)

        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        return Response({"detail": f"You have unfollowed {target.username}."})


# -----------------------------------
# LIST FOLLOWERS
# -----------------------------------
class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = SimpleUserSerializer(user.followers.all(), many=True)
        return Response(serializer.data)


# -----------------------------------
# LIST FOLLOWING
# -----------------------------------
class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = SimpleUserSerializer(user.following.all(), many=True)
        return Response(serializer.data)
