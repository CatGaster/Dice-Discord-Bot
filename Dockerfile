# Версия python
FROM python:3.10-slim

# Рабочая директория
WORKDIR /app

#устанавливаем зависимости из файла requirements.txt
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Команда для запуска бота.
CMD ["python", "bot.py"]