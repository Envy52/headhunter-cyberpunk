from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Vacancy, VacancyReview

User = get_user_model()


class SimpleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='mercenary')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_home_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/home/')


class VacancyReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='merc1', password='pass123', role='mercenary')
        self.fixer = User.objects.create_user(username='fixer1', password='pass123', role='fixer')
        self.vacancy = Vacancy.objects.create(title='Test Vacancy', description='...', requirements='...',
                                              fixer=self.fixer)

    def test_create_review(self):
        self.client.login(username='merc1', password='pass123')
        url = reverse('public_vacancy_detail', args=[self.vacancy.id])
        response = self.client.post(url, {'text': 'Отклик на вакансию'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(VacancyReview.objects.count(), 1)
        review = VacancyReview.objects.first()
        self.assertEqual(review.text, 'Отклик на вакансию')
        self.assertEqual(review.user, self.user)
