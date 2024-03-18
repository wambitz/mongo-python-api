# Use an official Python runtime as a parent image
FROM python:3-alpine

# Install bash
RUN apk add --no-cache bash

# Copy the current directory contents into the container at /usr/src/app
COPY ./ ./

# Install any needed packages specified in requirements.txt
RUN pip install Flask pymongo

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["flask", "run"]
