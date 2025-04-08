from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('mercenary', 'Наёмник'),
        ('fixer', 'Фиксер'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mercenary')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    experience = models.TextField()
    skills = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class Vacancy(models.Model):
    fixer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Response(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='responses')
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resume', 'vacancy')

    def __str__(self):
        return f"{self.resume.full_name} отклик на {self.vacancy.title}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'vacancy')

    def __str__(self):
        return f"{self.user.username} — {self.vacancy.title}"


class VacancyReview(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.vacancy.title}"

