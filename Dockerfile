# Use the Python3.7.2 image
FROM python:3.7.2-stretch
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

COPY /app .

# Define environment variable
CMD ["python", "app.py"]
