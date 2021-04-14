from django.db import models

# Create your models here.

class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200, unique=True)

class Dictionary(models.Model):
    word = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together=("word", "document_id")
