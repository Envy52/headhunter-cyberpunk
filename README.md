# 🕶️ HeadHunter: Cyberpunk Edition

**HeadHunter** — это веб-платформа для поиска работы и подбора персонала, вдохновлённая стилистикой **Cyberpunk 2077**.

## 🚀 Возможности

- Регистрация и аутентификация пользователей
- Разделение ролей: **Наёмник** (соискатель) и **Фиксер** (работодатель)
- Создание, редактирование и удаление:
  - Резюме (для наёмников)
  - Вакансий (для фиксеров)
- Отклики на резюме и отзывы на вакансии
- Поиск, фильтрация и избранное
- Загрузка аватара, смена пароля
- Адаптивный дизайн + киберпанк-стилизация
- Уведомления на email и встроенные JS-функции

## 🛠️ Технологии

- `Python 3.12`, `Django`
- HTML, CSS, JavaScript
- SQLite (по умолчанию)
- Git, GitHub


## 🧪 Запуск проекта

```bash
git clone https://github.com/your-username/hh-cyberpunk.git
cd hh-cyberpunk
python -m venv venv
venv\Scripts\activate # или source venv/bin/activate на Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
