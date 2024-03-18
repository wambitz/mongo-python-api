# Use an official Python runtime as a parent image
FROM python:3-alpine

# Install bash
RUN apk add bash

# Install any needed packages
RUN pip install Flask pymongo

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
