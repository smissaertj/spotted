# Base python package
FROM python:3.10.7-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the files
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]