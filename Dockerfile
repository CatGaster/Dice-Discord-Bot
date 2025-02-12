# Use the official Python image (e.g., 3.10-slim)
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project code
COPY . .

# Command to run the bot (entry point — bot.py)
CMD ["python", "bot.py"]