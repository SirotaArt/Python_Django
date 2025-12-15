import os
import django
from django.core.management import execute_from_command_line

#Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
django.setup()

print("🔧 Сброс и настройка базы данных...")

#Удаляем файл базы если существует
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("🗑️  Удалена старая база данных")

#Создаем миграции
print("📦 Создаем миграции...")
execute_from_command_line(['manage.py', 'makemigrations', 'tasks'])

#Применяем миграции
print("🚀 Применяем миграции...")
execute_from_command_line(['manage.py', 'migrate'])

#Создаем суперпользователя
print("👤 Создаем администратора...")
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Создан пользователь: admin / admin123")
else:
    print("⚠️  Пользователь admin уже существует")

print("\n🎉 Готово! Запустите сервер командой:")
print("python manage.py runserver")