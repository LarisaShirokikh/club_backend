FROM python:3.9

WORKDIR /app

# Скопировать requirements.txt в контейнер
COPY requirements.txt ./

# Обновить pip и установить зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Скопировать все файлы проекта в контейнер
COPY . .

EXPOSE 4000

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]