# from django.db import models
# from django.contrib.auth import get_user_model

# def create_path_image(self,filename):
#     query_id = str(self.query.id)
#     return f'query/{query_id}/{filename}'

# # Create your models here.
# class Expertise(models.Model):
#     name = models.CharField(max_length=100)

# class Expert(models.Model):
#     user = models.OneToOneField(get_user_model(), related_name="expert", on_delete=models.CASCADE)
#     years_of_experience = models.PositiveSmallIntegerField()
#     expertise = models.ForeignKey(Expertise, related_name="experts", on_delete=models.CASCADE)
#     laguages = models.CharField(max_length=255)