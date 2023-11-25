from django.db import models
from django.dispatch import receiver

# Create your models here.
class ChatBotFile(models.Model):
    file = models.FileField(upload_to="chatpdf/")

@receiver(models.signals.post_delete, sender = ChatBotFile)
def auto_delete_image_on_delete(sender,instance,*args,**kwargs):
    try:
        instance.file.delete(save=False)
    except:
        return