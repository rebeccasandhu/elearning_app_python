from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:course_id>/', consumers.ChatConsumer.as_asgi()),
]

# Let's add a logging statement here to verify this file is being executed
import logging
logger = logging.getLogger(__name__)
logger.info("WebSocket routing has been set up.")