from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/ajwc/<str:group_name>/<int:user_id>/", consumers.MyAsyncJsonWebsocketConsumer.as_asgi()) 

]