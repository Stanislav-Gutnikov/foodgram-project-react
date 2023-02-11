from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(
        max_length=254,
        unique=True)
    password = models.CharField(
        max_length=128,
        blank=False
    )
    role = models.CharField(
        max_length=50,
        choices=ROLES,
        default='user'
    )
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'password'
    ]
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow'
        ),)
