from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver

def create_path_image(self,filename):
    query_id = str(self.query.id)
    return f'query/{query_id}/{filename}'

# Create your models here.
class Expertise(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Expert(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="expert", on_delete=models.CASCADE)
    years_of_experience = models.PositiveSmallIntegerField()
    expertise = models.ForeignKey(Expertise, related_name="experts", on_delete=models.CASCADE)
    languages = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.user.name

class Query(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="queries", on_delete=models.CASCADE)
    description = models.TextField()
    catagory = models.ForeignKey(Expertise, related_name="queries", on_delete=models.CASCADE)
    contacted_before = models.CharField(max_length=5, default="No")
    is_resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.description[30]

    @property
    def status(self):
        return "Active"

class QueryFile(models.Model):
    query = models.ForeignKey(Query, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to=create_path_image, null=True)


@receiver(models.signals.post_delete, sender = QueryFile)
def auto_delete_image_on_delete(sender,instance,*args,**kwargs):
    try:
        instance.file.delete(save=False)
    except:
        return