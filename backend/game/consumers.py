from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import math
from .models import Instance

class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        if not user or user.is_anonymous:
            await self.close(code=4403)
            return

        self.instance_id = self.scope['url_route']['kwargs']['instance_id']
        if not await self.instance_exists(self.instance_id):
            await self.close(code=4404)
            return

        self.group_name = f'game.instance.{self.instance_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.channel_layer.send(
            'game.worker',
            {
                'type': 'game.join',
                'instance_id': self.instance_id,
                'profile_id': self.scope['user'].pk,
            }
        )

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.send(
                'game.worker',
                {
                    'type': 'game.leave',
                    'instance_id': self.instance_id,
                    'profile_id': self.scope['user'].pk,
                }
            )
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        t = content.get('type')
        
        if t == 'game.pingpong':
            await self.send_json({
                'type': 'game.pingpong',
                'data': 'pong',
            })
        
        elif t == 'game.input':
            data = content.get('data')
            if not self.input_is_valid(data):
                return
            
            await self.channel_layer.send(
                'game.worker',
                {
                    'type': 'game.input',
                    'instance_id': self.instance_id,
                    'profile_id': self.scope['user'].pk,
                    'data': data,
                }
            )
    
    async def game_state(self, event):
        await self.send_json({
            'type': 'game.state',
            'state': event['state'],
        })

    @database_sync_to_async
    def instance_exists(self, pk):
        return Instance.objects.filter(pk=pk).exists()

    def input_is_valid(self, data):
        if data is None or type(data) != dict:
            return False
        dx = data.get('dx')
        if type(dx) not in (int, float) or not math.isfinite(dx):
            return False
        dy = data.get('dy')
        if type(dy) not in (int, float) or not math.isfinite(dy):
            return False
        shoot = data.get('shoot')
        if type(shoot) not in (bool,):
            return False
        x = data.get('x')
        if type(x) not in (int, float) or not math.isfinite(x):
            return False
        y = data.get('y')
        if type(y) not in (int, float) or not math.isfinite(y):
            return False
        return True