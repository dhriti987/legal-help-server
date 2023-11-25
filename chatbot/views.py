from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import ChatBotFile, ChatBotFileSerializer
import openai
import requests
import os
from decouple import config
from asgiref.sync import sync_to_async
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

openai.api_key = config('OPEN_AI_API_KEY')

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

def get_completion(prompt): 
    print(prompt) 
    query = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {
            "role":"user",
            "content":prompt+ " what can be the legal solution according to Indian Constituition "
            }
        ]
    )
  
    response = query.choices[0].message["content"]
    print(response) 
    return response 

class ChatBotAPIView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        if not prompt:
            raise ValidationError("prompt is empty")
        response = get_completion(prompt)
        return Response({"response":response})


class ChatPDFConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope.get("source_id") == None:
            await self.close()
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        reply = chatpdf(self.scope["source_id"],text_data)
        await self.send(text_data=reply)

    
class UploadChatBotFileAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = ChatBotFile.objects.all()
    serializer_class = ChatBotFileSerializer

class ChatPDFConsumerV2(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['pdf_id']:
            return
        self.pdf_id = self.scope["pdf_id"]
        try:
            # print(self.pdf_id)
            self.file = await self.get_file(self.pdf_id)
            
        except Exception as e:
            # print(e)
            await self.accept()
            await self.send(text_data="File not Found please Upload the Document again")
            await self.close()
            return

        await self.set_up_pdf(self.file.path)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        result = await self.get_result(text_data)
        await self.send(result)

    @database_sync_to_async
    def get_file(self, id):
        return ChatBotFile.objects.get(pk=id).file
    
    @sync_to_async
    def set_up_pdf(self, filepath):
        pdfreader = PdfReader(filepath)
        raw_text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                raw_text += content
        text_splitter = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 800,
            chunk_overlap  = 200,
            length_function = len,
        )
        texts = text_splitter.split_text(raw_text)
        embeddings = OpenAIEmbeddings()
        self.document_search = FAISS.from_texts(texts, embeddings)
        self.chain = load_qa_chain(OpenAI(), chain_type="stuff")
    @sync_to_async
    def get_result(self, query):
        docs = self.document_search.similarity_search(query)
        return self.chain.run(input_documents=docs, question=query)