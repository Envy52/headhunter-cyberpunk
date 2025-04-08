from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.start_page, name='start'),
    path('home/', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('resumes/', views.resume_list, name='resume_list'),
    path('resumes/create/', views.resume_create, name='resume_create'),
    path('resumes/<int:pk>/update/', views.resume_update, name='resume_update'),
    path('resumes/<int:pk>/delete/', views.resume_delete, name='resume_delete'),

    path('vacancies/', views.vacancy_list, name='vacancy_list'),
    path('vacancies/create/', views.vacancy_create, name='vacancy_create'),
    path('vacancies/<int:pk>/', views.vacancy_detail, name='vacancy_detail'),
    path('vacancies/<int:pk>/update/', views.vacancy_update, name='vacancy_update'),
    path('vacancies/<int:pk>/delete/', views.vacancy_delete, name='vacancy_delete'),

    path('resumes/all/', views.all_resumes, name='all_resumes'),
    path('resumes/<int:pk>/', views.resume_detail, name='resume_detail'),

    path('vacancies/public/', views.public_vacancy_list, name='public_vacancy_list'),
    path('vacancies/public/<int:pk>/', views.public_vacancy_detail, name='public_vacancy_detail'),

    path('vacancies/<int:pk>/review/', views.leave_review, name='leave_review'),
    path('resumes/<int:pk>/respond/', views.respond_to_resume, name='respond_to_resume'),

    path('favorites/', views.favorite_list, name='favorite_list'),

    path('test-email/', views.test_email_view, name='test_email'),

    path('favorites/add/<int:vacancy_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:vacancy_id>/', views.remove_from_favorites, name='remove_from_favorites'),

    path('error/', TemplateView.as_view(template_name='error.html'), name='respond_error'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='password_change.html',
        success_url='/password_change/done/'
    ), name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_change_done.html'
    ), name='password_change_done'),

]
