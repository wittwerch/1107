# Using official python runtime base image
FROM ubuntu

# Set the application directory
WORKDIR /app

RUN mkdir /logs
RUN apt-get update
RUN apt-get install -y python python-dev python-pip libmysqld-dev libjpeg-dev zlib1g-dev libpng12-dev
RUN /usr/sbin/locale-gen de_CH de_CH.UTF-8

# Copy our code from the current folder to /app inside the container
ADD ./src /app

# Install our requirements.txt
RUN pip install -r /app/requirements.txt

# Make port 8000 available for links and/or publish
EXPOSE 8000

# Define our command to be run when launching the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
