import os
import dotenv
import asyncio
import requests
import websockets
import json
import pygame
from engine import Engine
from renderer import Renderer
from renderer.settings import *
dotenv.load_dotenv()

URL = os.environ.get('URL')
TLS = os.environ.get('TLS') == 'true'
ID = os.environ.get('ID')
PASSWORD = os.environ.get('PASSWORD')
INSTANCEID = os.environ.get('INSTANCEID')
FPS = 60

def get_sessionid():
    response = requests.post(f"{'https://' if TLS else 'http://'}{URL}/api/account/login/", data={
        'username': ID,
        'password': PASSWORD,
    })
    response.raise_for_status()
    sessionid = response.cookies.get('sessionid')
    if sessionid is None:
        raise RuntimeError('로그인 실패')
    return sessionid

async def receive_state(socket, engine: Engine):
    async for message in socket:
        data = json.loads(message)
        if data.get('type') == 'game.state':
            engine.load_state(data['state'])

async def main(sessionid):
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('GunGame Multi')

    clock = pygame.time.Clock()
    engine = Engine()
    renderer = Renderer(screen)

    async with websockets.connect(
        f"{'wss://' if TLS else 'ws://'}{URL}/ws/game/instance/{INSTANCEID}/",
        additional_headers={'Cookie': f'sessionid={sessionid}'}
    ) as sock:
        receive_task = asyncio.create_task(receive_state(sock, engine))

        try:
            running = True
            while running:
                clock.tick(FPS)

                shoot = False
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            shoot = True

                keys = pygame.key.get_pressed()

                dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
                dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
                x, y = pygame.mouse.get_pos()

                await sock.send(json.dumps({
                    'type': 'game.input',
                    'data': {
                        'dx': dx,
                        'dy': dy,
                        'shoot': shoot,
                        'x': x,
                        'y': y,
                    }
                }))

                renderer.render(engine)

                await asyncio.sleep(0)

        finally:
            receive_task.cancel()
            try:
                await receive_task
            except asyncio.CancelledError:
                pass

    pygame.quit()

if __name__ == '__main__':
    sessionid = get_sessionid()
    asyncio.run(main(sessionid))