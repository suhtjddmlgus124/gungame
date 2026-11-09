import asyncio
import time
from channels.layers import get_channel_layer
from .engine import Engine
from .engine.settings import *

class GameInstance:
    TPS = 60

    def __init__(self, instance_id):
        self.engine: Engine | None = None
        self.task: asyncio.Task | None = None
        self.instance_id = instance_id
        self.channel_layer = get_channel_layer()
        self.lock = asyncio.Lock()

    async def start(self):
        if self.task is not None and not self.task.done():
            return
        self.engine = Engine()
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        if self.task is None:
            return
        task = self.task
        if not task.done():
            task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        if self.task is task:
            self.task = None

    async def run(self):
        interval = 1 / self.TPS
        last_time = time.monotonic()

        try:
            while True:
                now = time.monotonic()
                dt = now - last_time
                last_time = now

                self.engine.update(dt)
                await self.broadcate_state()
                
                elapsed = time.monotonic() - now
                await asyncio.sleep(max(0, interval - elapsed))
        
        except asyncio.CancelledError:
            raise

        finally:
            self.engine = None

    async def join_player(self, profile_id):
        async with self.lock:
            if self.engine is None:
                await self.start()
            self.engine.add_player(profile_id, initial_position=(WORLD_WIDTH/2, WORLD_HEIGHT/2))

    async def leave_player(self, profile_id):
        async with self.lock:
            if self.engine is None:
                return
            self.engine.remove_player(profile_id)
            if not self.engine.players:
                await self.stop()

    def handle_input(self, profile_id, data):
        if self.engine is None:
            return
        player = self.engine.players.get(profile_id)
        if player is None:
            return

        self.engine.move_player(profile_id, data['dx'], data['dy'])
        if data['shoot']:
            self.engine.shoot_player(profile_id, data['x'], data['y'])

    async def broadcate_state(self):
        await self.channel_layer.group_send(
            f'game.instance.{self.instance_id}',
            {
                'type': 'game.state',
                'state': self.engine.get_state(),
            }
        )