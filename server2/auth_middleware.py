from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack

from django.db import close_old_connections

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        try: 
            source_id  = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('sourceId', None)
        except:
            source_id = None
        try: 
            pdf_id  = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('pdfId', None)
        except:
            pdf_id = None
        scope['source_id'] = source_id
        scope['pdf_id'] = pdf_id
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
    
TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))