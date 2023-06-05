import sys
sys.path.append("..")  # Adds higher directory to python modules path.
from celery import Celery
from chat_app.db import schemas
from chat_app.db import crud

celery = Celery('chat_app', broker='amqp://guest@broker//', include=["chat_app.tasks"])

@celery.task
def send_message(message: schemas.MessageCreate) -> None:
    """
    Celery task for sending a message.

    Parameters:
        - message: The message to be sent, represented as a schemas.MessageCreate object.

    Returns:
        None
    """
    crud.create_message(message=message)
