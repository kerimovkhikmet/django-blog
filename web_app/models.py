from django.db import models

# Create your models here.


class Article (models.Model):
    TOPIC_CHOICES = [
        ('Sp', 'Sport'),
        ('Ent', 'Entertainment'),
        ('Sc', 'Science')
    ]
    name = models.CharField(max_length=200)
    theme = models.CharField(max_length=8, choices=TOPIC_CHOICES)
    text = models.TextField(null=True)
    author = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Commentary (models.Model):
    text = models.CharField(max_length=4000)
    author = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', on_delete=models.PROTECT)

    def __str__(self):
        return self.text


class ConnectedUsers(models.Model):
    first_name = models.CharField(max_length=50)
    connected = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '%s connected at %s' % (self.first_name, self.connected)
