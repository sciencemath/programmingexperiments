from django.db import models
from django.utils.text import slugify

class Person(models.Model):
  SHIRT_SIZES = {
    "S": "Small",
    "M": "Medium",
    "L": "Large",
  }
  name = models.CharField(max_length=60)
  shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

  def __str__(self):
    return self.name

class Musician(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  instrument = models.CharField(max_length=100)

class Album(models.Model):
  artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  release_date = models.DateField()
  num_stars = models.IntegerField()

class Runner(models.Model):
  MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
  name = models.CharField(max_length=60)
  medal = models.CharField(blank=True, choices=MedalType, max_length=10)

class Fruit(models.Model):
  name = models.CharField(max_length=100, primary_key=True)

class Manufacturer(models.Model):
  pass

class Car(models.Model):
  company_that_makes_it = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

class Topping(models.Model):
  pass

class Pizza(models.Model):
  toppings = models.ManyToManyField(Topping)

class Group(models.Model):
  name = models.CharField(max_length=128)
  members = models.ManyToManyField(Person, through='Membership')

  def __str__(self):
    return self.name
  
class Membership(models.Model):
  person = models.ForeignKey(Person, on_delete=models.CASCADE)
  group = models.ForeignKey(Group, on_delete=models.CASCADE)
  date_joined = models.DateField()
  invite_reason = models.CharField(max_length=64)

class Place(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=80)

  def __str__(self):
    return f'{self.name} the palce'

class Restaurant(models.Model):
  place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
  serves_hot_dogs = models.BooleanField(default=False)
  serves_pizza = models.BooleanField(default=False)

  def __str__(self):
    return f'{self.place.name} the restaurant'
  
class Waiter(models.Model):
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)

  def __str__(self):
    return f'{self.name} the waiter at {self.restaurant}'
  
class Ox(models.Model):
  horn_length = models.IntegerField()

  class Meta:
    ordering = ['horn_length']
    verbose_name_plural = "oxen"

class PersonStatus(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  birth_date = models.DateField()

  def baby_boomer_status(self):
    """Returns baby-boomer status."""
    import datetime

    if self.birth_date < datetime.date(1945, 8, 1):
      return "Pre-boomer"
    elif self.birth_date < datetime.date(1965, 1, 1):
      return "Baby boomer"
    else:
      return "Post-boomer"
    
  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'

"""
you can define your own save()
def save(self **kwargs):
  do_something()
  super().save(**kwargs)
  do_something_else()
"""

class Blog(models.Model):
  name = models.CharField(max_length=100)
  slug = models.TextField()

  def save(self, **kwargs):
    self.slug = slugify(self.name)
    if (
      update_fields := kwargs.get('update_fields')
    ) is not None and 'name' in update_fields:
      kwargs['update_fields'] = {'slug'}.union(update_fields)
    super().save(**kwargs)

class CommonInfo(models.Model):
  name = models.CharField(max_length=100)
  age = models.PositiveIntegerField()

  class Meta:
    abstract = True
    ordering = ['name']

class Unmanaged(models.Model):
  class Meta:
    abstract = True
    managed = False

class Student(CommonInfo, Unmanaged):
  home_group = models.CharField(max_length=5)
  
  class Meta(CommonInfo.Meta, Unmanaged.Meta):
    db_table = 'student_info'