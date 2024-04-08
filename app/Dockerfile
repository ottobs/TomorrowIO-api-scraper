FROM python:3.10-slim
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY python_app.py .
COPY requirements.txt .
COPY app.config .

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run your Python script when the container launches
CMD ["python", "python_app.py"]