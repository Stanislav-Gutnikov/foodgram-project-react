from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    ValidationError
)
from rest_framework.fields import SerializerMethodField, IntegerField
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag, ShoppingCart,
    Favorite
)
from users.serializers import UserSerializer


User = get_user_model()


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class AddIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeIngredientSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeSerializer(ModelSerializer):
    image = Base64ImageField()
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = UserSerializer(read_only=True)
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'text',
            'tags',
            'ingredients',
            'image',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if ingredient_id in ingredient_list:
                raise ValidationError({
                    'ingredients': ('Этот ингредиент уже существует')
                })
            ingredient_list.append(ingredient_id)
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance, context={
                'request': self.context.get('request')
            }
        ).data

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    @staticmethod
    def create_ingredients(ingredients, recipe):
        new_ingredients = []
        for ingredient in ingredients:
            new_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
            new_ingredients.append(new_ingredient)
        RecipeIngredient.objects.bulk_create(new_ingredients)


class RecipeListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(
        read_only=True,
        source='ingredient.id',
        many=True)
    is_in_favorite = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'author',
            'text',
            'tags',
            'ingredients',
            'image',
            'cooking_time',
            'is_in_favorite',
            'is_in_shopping_cart'
            )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(carts__user=user, id=obj.id).exists()

    def get_is_in_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()


class ShoppingCartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('id', 'user', 'recipe')


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'recipe')
