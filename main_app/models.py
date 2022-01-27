from django.db import models
from django.urls import reverse 
from datetime import date 
from django.contrib.auth.models import User

STRINGS = (
    ('X', 'Extra Lite'),
    ('L', 'Lite'),
    ('M', 'Medium')
)

class Accessory(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=50)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('accessories_detail', kwargs={'pk': self.id})

class Guitar(models.Model):  
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()

    accessories = models.ManyToManyField(Accessory)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'guitar_id': self.id})      

    def restrung_recently(self):
        return self.restring_set.filter(date=date.today()).count() >= 1 

class Photo(models.Model):
    url = models.CharField(max_length=200)
    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for guitar_id: {self.guitar_id} @{self.url}"

class Restring(models.Model):
    date = models.DateField('restring date')
    string = models.CharField(
        max_length=1,
        choices=STRINGS,
        default=STRINGS[0][0]
    )

    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_string_display()} on {self.date}"

    # change the default sort
    class Meta:
        ordering = ['-date']