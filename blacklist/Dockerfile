FROM python:3.9
WORKDIR /blacklist

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/Pipfile

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=/app/src/main.py

CMD /bin/bash -c "sleep 2 && flask run --host=0.0.0.0 -p 5000"

ENTRYPOINT ["newrelic-admin", "run-program"]
