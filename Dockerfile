FROM python:3.10
WORKDIR /blacklist

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 5000
# Define environment variable
#ENV FLASK_APP=/app/src/main.py
CMD /bin/bash -c "python /app/application.py"