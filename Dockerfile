# pull official base image
FROM python:3.9-slim

# set work directory
WORKDIR /

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY chat_app/ /chat_app

# Expose the port that the FastAPI app will be listening on
EXPOSE 8000

# Start the FastAPI app when the container starts
CMD ["uvicorn", "chat_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
