# Указываем официальный образ Python (минимальный размер)
FROM python:3.9-slim

# Не создавать .pyc-файлы и выводить логи сразу в stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /code

# Сначала копируем только requirements.txt, чтобы использовать кеширование слоев Docker
COPY requirements.txt /code/

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . /code/

# По желанию: собираем статические файлы (если вы используете collectstatic)
#RUN python manage.py collectstatic --noinput

# Указываем команду, которая будет запускать Django-сервис
# Здесь используется gunicorn. Меняйте myproject на имя вашего Django-пакета
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]