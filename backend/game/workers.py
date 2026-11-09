from channels.consumer import AsyncConsumer
from .instance import GameInstance

class GameWorker(AsyncConsumer):
    instances: dict[int, GameInstance] = {}

    async def game_join(self, event):
        instance_id = int(event['instance_id'])
        
        if instance_id not in self.instances:
            self.instances[instance_id] = GameInstance(instance_id)
        
        instance = self.instances[instance_id]
        await instance.join_player(event['profile_id'])

    async def game_leave(self, event):
        instance_id = int(event['instance_id'])

        instance = self.instances.get(instance_id)
        if instance is None:
            return
        await instance.leave_player(event['profile_id'])

        if instance.engine is None:
            self.instances.pop(instance_id, None)

    async def game_input(self, event):
        instance = self.instances.get(int(event['instance_id']))
        if instance is None:
            return
        instance.handle_input(event['profile_id'], event['data'])