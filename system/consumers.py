from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from system.models import Chef, Customer, Order
from channels.db import database_sync_to_async

class MyConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        print ('connect')
        await self.accept ()
        await self.channel_layer.group_add ("users", self.channel_name)
        print (f"Add {self.channel_name} channel to users's group")


    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        print("_______________ ", command)
        if command == 'to_chef': # when customer completes order
            order_id = int(content.get("id"))
            await self.update_order_status(order_id=order_id, status=1)
            await self.channel_layer.group_send(
                'users',
                {
                    'type': 'chat.message',
                    'command': 'send to chef',
                }
            )
        elif command == 'shipping':   # when chef notify user of getting food
            order_id = int(content.get("id"))
            await self.update_order_status(order_id=order_id, status=2)
            await self.channel_layer.group_send(
                'users',
                {
                    'type': 'chat.message',
                    'command': 'shipping',
                }
            )
        elif command == 'complete':   # when chef notify user of getting food
            order_id = int(content.get("id"))
            await self.update_order_status(order_id=order_id, status=3)
            await self.channel_layer.group_send(
                'users',
                {
                    'type': 'chat.message',
                    'command': 'complete',
                }
            )

    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        print("chat_message is running")
        await self.send_json(
            {
                # "msg_type": settings.MSG_TYPE_ENTER,
                'command': event['command']
            },
        )
        

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        await self.channel_layer.group_discard ("users", self.channel_name)
        print (f"Remove {self.channel_name} channel from users's group")

    @database_sync_to_async
    def update_order_status(self, order_id, status):
        return Order.objects.filter(pk=order_id).update(status=status)