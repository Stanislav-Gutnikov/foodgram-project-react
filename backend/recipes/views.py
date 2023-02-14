from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)
from .models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredients,
    Favorite,
    ShoppingCart
)
from .filters import IngredientFilter, RecipeFilter


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        detail=True,
        methods=('post', ),
        permission_classes=(IsAuthenticated,),
        url_path='favorite')
    def create_favorite(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk
            }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,),
        url_path='shopping_cart'
    )
    def add_to_shopping_cart(self, request, pk=None):
        data = {
            'user': request.user.id,
            'recipe': pk
            }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

    @create_favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @add_to_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
            )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredients.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        if not ingredients:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        shopping_list = 'Список покупок \n\n'
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient["ingredient__name"]}'
                f'{ingredient["ingredient__measurement_unit"]}'
                f'{ingredient["amount__sum"]}\n'
            )
        return HttpResponse(
            shopping_list,
            content_type='text/plain'
        )


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('name',)
