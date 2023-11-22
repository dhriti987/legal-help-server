from channels.generic.websocket import AsyncWebsocketConsumer
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from decouple import config


def get_headers_for_chat_pdf():
    headers = {
        'x-api-key': config("CHAT_PDF_API_KEY")
    }
    return headers


def get_files_for_chat_pdf(name):
    return {'file': (name, open("media/"+name, 'rb'), 'application/octet-stream')}


def chatpdf(source_id, msg):
    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': msg,
            }
        ]

    }
    response = requests.post('https://api.chatpdf.com/v1/chats/message',
                             headers=get_headers_for_chat_pdf(), json=data)
    
    if response.status_code == 200:
        return response.json()['content']
    else:
        print(response)
    return "An Error Occured"


@csrf_exempt
def get_source_id(request):
    file = request.FILES.get("file")
    if not file:
        return JsonResponse(data={"msg": "You have to Provide a FIle"}, status=404)

    if not file.name.endswith(".pdf"):
        return JsonResponse(data={"msg": "File provided is not PDF"}, status=404)

    with open("media/" + file.name, "wb") as pdf:
        pdf.write(file.read())

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file',
        headers=get_headers_for_chat_pdf(),
        files=get_files_for_chat_pdf(file.name)
    )
    os.remove("media/" + file.name)
    if response.status_code !=200:
        return JsonResponse(data={"msg": "An Error Occured"}, status=404)


    return JsonResponse(data=response.json())

# Create your views here.


class ChatPDFConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope.get("source_id") == None:
            await self.close()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        reply = chatpdf(self.scope["source_id"],text_data)
        await self.send(text_data=reply)

    
