from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

from .models import User, Subscriptions
from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, },
            'last_name': {'required': True, },
            'first_name': {'required': True, },
            'username': {'required': True, },
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password')
        )
        return super(UserSerializer, self).create(validated_data)

    def is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscriptions.objects.filter(
            user=request.user,
            author=obj
        ).exists()

    def password_is_valided(self, value):
        password_validation.validate_password(value, self.instance)
        return value


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password',)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Проверьте текущий пароль')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def update_password(self, instance, valided_data):
        instance.set_password(valided_data['new_password'])
        instance.save()
        return instance


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class UserMeSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            User.REQUIRED_FIELDS,
            User.USERNAME_FIELD,
            'password',
            )


class SubscrptionsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)
    is_subscribe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriptions
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribe',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = Recipe.objects.filter(
                author=obj.author_id
            ).all()[:(int(recipes_limit))]
        else:
            recipes = Recipe.objects.filter(author=obj.author_id).all()
        context = {
            'request': request
            }
        return RecipeSerializer(
            recipes,
            many=True,
            context=context
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author_id).count()

    def get_is_subscribe(self, obj):
        user = self.context.get('request').user
        if not user:
            return False
        return Subscriptions.objects.filter(
            user=user,
            author=obj.author_id
            ).exists()
