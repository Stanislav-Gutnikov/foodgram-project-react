from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    UserSerializer,
    SubscrptionsSerializer,
    UserMeSerializer,
    ChangePasswordSerializer
)
from .models import User, Subscriptions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = (AllowAny,)
    search_fields = ('username', )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
        )
    def me(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )

    @action(
        detail=False,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        serializer_class=ChangePasswordSerializer,
        url_path='set_password'
        )
    def set_password(self, request, pk=None):
        serialiser = self.get_serializer(
            instance=request.user,
            data=request.data
        )
        serialiser.is_valid(raise_exception=True)
        serialiser.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscriptions.objects.filter(user=user)
        paginator = self.paginate_queryset(queryset)
        serializer = SubscrptionsSerializer(
            paginator,
            context={
                'request': request
            },
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscriptions.objects.filter(
            user=user,
            author=author
        ).exists():
            return Response(
                {'errors': ('Подписка существует')},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscribe = Subscriptions.objects.create(
            user=user,
            author=author
        )
        serializer = SubscrptionsSerializer(
            subscribe,
            context={
                'request': request
            }
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscribe = Subscriptions.objects.filter(
            user=user,
            author=author
        )
        if subscribe.exists():
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
