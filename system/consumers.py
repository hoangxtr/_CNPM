from django.conf import settings

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from system.models import Chef, Customer, Order

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
        print('connect roi nha')
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            self.channel_layer.group_add("users", self.channel_name)
            user = self.scope['user']
            await self.accept()
            # await self.send_json({'data': str(user)})
        print(" +++++++++++++++++++++++++++++end connect function ")


    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        print("_______________ ", command)
        user = self.scope['user']
        # if Customer.objects.filter(user=user).exists(): # when customer sends json
        if command == 'to_chef': # when customer completes order
            my_id = content.get("id")
            print("send from customer", my_id)
            # order = Order.objects.get(pk=int(my_id))
            # order.to_chef = True
            # order.save()
            # await self.send_json({'command': 'refresh'})

            await self.channel_layer.group_send(
                'users',
                {
                    'type': 'chat.message',
                    'text': 'group send message for you'
                }
            # print("da sent")
            )
            print('sent')
        elif command == 'shipping':   # when chef notify user of getting food
            print("send from chef")
            await self.send_json({'title': 'hoang dep trai ghe'})

    async def chat_message(self, event):
        # Handles the "chat.message" event when it's sent to us.
        print("chat_message is running")
        await self.send_json(
            {
                # "msg_type": settings.MSG_TYPE_ENTER,
                'content': event['text']
            },
        )
        

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        print('disconnect r nha')
        # for room_id in list(self.rooms):
        #     try:
        #         await self.leave_room(room_id)
        #     except ClientError:
        #         pass

    