FROM python:3.10.9

# Указываем какую консоль будем использовать
SHELL ["/bin/bash", "-c"]


# Настройка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем и скачиваем нужные зависимости в pip
RUN pip install --upgrade pip
RUN pip install gunicorn

EXPOSE 8080

RUN useradd -rms /bin/bash food && chmod 777 /opt /run


# Указываем рабочую директорию
WORKDIR /food

# Создаёт папки и дает им права
RUN mkdir /food/static && mkdir /food/media && chown -R food:food /food && chmod -R 755 /food


# Копирование файлов проекта с ПК на Образ
COPY --chown=food:food . .

RUN pip install -r requirements.txt

# Переключение на созданного пользователя
USER food

# Запуск проекта
CMD ["gunicorn","-b","0.0.0.0:8001","conf.wsgi:application"]
# CMD отвечает за команды докера

