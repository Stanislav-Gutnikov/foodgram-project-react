from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UserSerializer, FollowSerializer, UserMeSerializer, ChangePasswordSerializer
from .models import User, Follow


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    #search_fields = ['username', ]
    
    @action(detail=False, methods=('get',), serializer_class=UserMeSerializer)
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=('post',), permission_classes=(IsAuthenticated,), serializer_class=ChangePasswordSerializer, url_path='set_password')
    def set_password(self, request, pk=None):
        serialiser = self.get_serializer(
            instance=request.user,
            data=request.data
        )
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        return Response(status=status.HTTP_204_NO_CONTENT)