import asyncio
import logging
import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from .services.fibonacci import calculate_fibonacci
from channels.db import database_sync_to_async

logger = logging.getLogger(__name__)

class FibonacciConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            self.send_current_time_task = asyncio.create_task(self.send_current_time())
        except Exception as e:
            logger.error(f"Erro ao conectar: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'username'):
                await self.set_user_inactive(self.username)
            self.send_current_time_task.cancel()
        except Exception as e:
            logger.error(f"Erro ao desconectar: {e}")


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            
            if 'username' in data:
                self.username = data['username']
                await self.set_user_active(self.username)
            
            elif 'n' in data:
                n = data['n']
                result = calculate_fibonacci(n)
                await self.send(text_data=json.dumps({
                    'result': result
                }))
        except json.JSONDecodeError:
            logger.warning("Formato JSON inválido recebido.")
            await self.send(text_data=json.dumps({
                'error': 'Formato JSON inválido'
            }))
        except ValueError as e:
            logger.warning(f"Dados inválidos recebidos: {e}")
            await self.send(text_data=json.dumps({
                'error': f"Dados inválidos: {str(e)}"
            }))
        except Exception as e:
            logger.error(f"Erro inesperado ao processar a mensagem: {e}")
            await self.send(text_data=json.dumps({
                'error': f"Erro inesperado: {str(e)}"
            }))
            
    async def send_current_time(self):
        while True:
            now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            await self.send(text_data=json.dumps({
                'hora_atual': now
            }))
            await asyncio.sleep(1)  

    @database_sync_to_async
    def set_user_active(self, username):
        try:
            from .models import ConnectedUser
            ConnectedUser.objects.update_or_create(username=username, defaults={'is_active': True})
        except Exception as e:
            logger.error(f"Erro ao registrar o usuário: {e}")
            raise

    @database_sync_to_async
    def set_user_inactive(self, username):
       try:
            from .models import ConnectedUser
            ConnectedUser.objects.filter(username=username).update(is_active=False)
       except Exception as e:
            logger.error(f"Erro ao definir o usuário como inativo: {e}")
            raise
