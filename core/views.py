from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Resume, Vacancy, Favorite, Response
from .forms import ResumeForm, VacancyForm, CustomUserCreationForm, ProfileUpdateForm, VacancyReviewForm
from django.contrib.auth import login
from .decorators import mercenary_required, fixer_required
from django.core.paginator import Paginator
from django.utils.http import urlencode
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib import messages


@login_required
def home(request):
    if request.user.role == 'mercenary':
        resumes = Resume.objects.filter(user=request.user)
    elif request.user.role == 'fixer':
        resumes = Resume.objects.all()
    else:
        resumes = []

    return render(request, 'home.html', {'resumes': resumes})



def start_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'start_page.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}! Вы успешно зарегистрировались.")
            return redirect('home')
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def resume_create(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            messages.success(request, "Резюме успешно создано.")
            return redirect('resume_list')
        else:
            messages.error(request, "Ошибка при создании резюме.")
    else:
        form = ResumeForm()
    return render(request, 'resume_form.html', {'form': form})


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    form = ResumeForm(request.POST or None, instance=resume)
    if form.is_valid():
        form.save()
        return redirect('resume_list')
    return render(request, 'resume_form.html', {'form': form})


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        messages.success(request, "Резюме удалено.")
        return redirect('resume_list')
    return render(request, 'resume_confirm_delete.html', {'resume': resume})


@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume_list.html', {'resumes': resumes})


@login_required
def vacancy_list(request):
    vacancies = Vacancy.objects.filter(fixer=request.user)
    return render(request, 'vacancy_list.html', {'vacancies': vacancies})


@login_required
def vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, fixer=request.user)
    reviews = vacancy.reviews.all()
    return render(request, 'vacancy_detail.html', {
        'vacancy': vacancy,
        'reviews': reviews
    })



@login_required
def vacancy_create(request):
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.fixer = request.user
            vacancy.save()
            messages.success(request, "Вакансия успешно создана.")
            return redirect('vacancy_list')
        else:
            messages.error(request, "Ошибка при создании вакансии. Проверьте форму.")
    else:
        form = VacancyForm()
    return render(request, 'vacancy_form.html', {'form': form})


@login_required
def vacancy_update(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, fixer=request.user)
    form = VacancyForm(request.POST or None, instance=vacancy)
    if form.is_valid():
        form.save()
        return redirect('vacancy_list')
    return render(request, 'vacancy_form.html', {'form': form})


@login_required
def vacancy_delete(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk, employer=request.user)
    if request.method == 'POST':
        vacancy.delete()
        messages.success(request, "Вакансия удалена.")
        return redirect('vacancy_list')
    return render(request, 'vacancy_confirm_delete.html', {'vacancy': vacancy})


@login_required
def all_resumes(request):
    resumes = Resume.objects.all()

    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', '-created_at')

    if search_query:
        resumes = resumes.filter(full_name__icontains=search_query)

    resumes = resumes.order_by(sort_by)

    paginator = Paginator(resumes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    base_url = '?' + urlencode(query_params)

    return render(request, 'all_resumes.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
        'base_url': base_url,
    })


@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)
    vacancies = Vacancy.objects.filter(fixer=request.user) if request.user.role == 'fixer' else None
    return render(request, 'resume_detail.html', {'resume': resume, 'vacancies': vacancies})


@login_required
@mercenary_required
def public_vacancy_list(request):
    vacancies = Vacancy.objects.all()
    search = request.GET.get('search')
    date = request.GET.get('date')
    user_favorites = request.user.favorites.all().values_list('vacancy_id', flat=True)

    if search:
        vacancies = vacancies.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(requirements__icontains=search)
        )

    if date:
        vacancies = vacancies.filter(created_at__date=date)

    return render(request, 'public_vacancy_list.html', {
        'vacancies': vacancies,
        'user_favorites': user_favorites,
        'search': search or '',
        'date': date or '',
    })


@login_required
@mercenary_required
def public_vacancy_detail(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    reviews = vacancy.reviews.select_related('user').order_by('-created_at')

    if request.method == 'POST':
        form = VacancyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.vacancy = vacancy
            review.user = request.user
            review.save()
            return redirect('public_vacancy_detail', pk=pk)
    else:
        form = VacancyReviewForm()

    return render(request, 'public_vacancy_detail.html', {
        'vacancy': vacancy,
        'form': form,
        'reviews': reviews
    })


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def leave_review(request, pk):
    vacancy = get_object_or_404(Vacancy, pk=pk)
    form = VacancyReviewForm(request.POST or None)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.vacancy = vacancy
        review.save()
        return redirect('public_vacancy_detail', pk=pk)
    return render(request, 'leave_review.html', {'form': form, 'vacancy': vacancy})


@login_required
def respond_to_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    if request.method == 'POST':
        vacancy_id = request.POST.get('vacancy')
        if not vacancy_id:
            messages.error(request, "Выберите вакансию для отклика.")
            return redirect('resume_detail', pk=pk)

        vacancy = get_object_or_404(Vacancy, id=vacancy_id, fixer=request.user)
        Response.objects.create(resume=resume, vacancy=vacancy)
        messages.success(request, "Отклик отправлен.")
        return redirect('resume_detail', pk=pk)

    return redirect('resume_detail', pk=pk)


def error_page(request):
    return render(request, 'error_page.html', {'message': 'Вакансия не найдена!'})


@login_required
@mercenary_required
def add_to_favorites(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, id=vacancy_id)
    Favorite.objects.get_or_create(user=request.user, vacancy=vacancy)
    return redirect('public_vacancy_list')


@login_required
@mercenary_required
def remove_from_favorites(request, vacancy_id):
    Favorite.objects.filter(user=request.user, vacancy_id=vacancy_id).delete()
    return redirect('favorites')


@login_required
@mercenary_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('vacancy')
    return render(request, 'favorites.html', {'favorites': favorites})

