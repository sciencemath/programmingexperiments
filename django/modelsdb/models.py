from django.db import models
from datetime import date
# from django.utils.text import slugify

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

class OrderedPerson(Person):
  class Meta:
    ordering = ['shirt_size']
    proxy = True

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
  
class Supplier(Place):
  customers = models.ManyToManyField(Place, related_name='provider')
  
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

# class Blog(models.Model):
#   name = models.CharField(max_length=100)
#   slug = models.TextField()

#   def save(self, **kwargs):
#     self.slug = slugify(self.name)
#     if (
#       update_fields := kwargs.get('update_fields')
#     ) is not None and 'name' in update_fields:
#       kwargs['update_fields'] = {'slug'}.union(update_fields)
#     super().save(**kwargs)

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

class NewManager(models.Manager):
  pass

class ExtraManagers(models.Model):
  secondary = NewManager()
  class Meta:
    abstract = True

class MyPerson(Person, ExtraManagers):
  class Meta:
    proxy = True
  
  def do_something(self):
    pass

# class Article(models.Model):
#   article_id = models.AutoField(primary_key=True)

# class Book(models.Model):
#   book_id = models.AutoField(primary_key=True)

# class BookReview(Book, Article):
#   pass

# OR:
class Piece(models.Model):
  pass

class Article(Piece):
  article_piece = models.OneToOneField(Piece, on_delete=models.CASCADE, parent_link=True)

# class Book(Piece):
#   book_piece = models.OneToOneField(Piece, on_delete=models.CASCADE, parent_link=True)

# class BookReview(Book, Article):
#   pass

class Blog(models.Model):
  name = models.CharField(max_length=100)
  tagline = models.TextField()

  def __str__(self):
    return self.name
  
class Author(models.Model):
  name = models.CharField(max_length=200)
  email = models.EmailField()
  age = models.IntegerField()

  def __str__(self):
    return self.name
  
class Publisher(models.Model):
  name = models.CharField(max_length=300)

class Book(models.Model):
  name = models.CharField(max_length=300)
  pages = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  rating = models.FloatField()
  authors = models.ManyToManyField(Author)
  publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
  pubdate = models.DateField()

  def __str__(self):
    return self.name

class Store(models.Model):
  name = models.CharField(max_length=300)
  books = models.ManyToManyField(Book)
  
class Entry(models.Model):
  blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
  headline = models.CharField(max_length=255)
  body_text = models.TextField()
  pub_date = models.DateField()
  mod_date = models.DateField(default=date.today)
  authors = models.ManyToManyField(Author)
  number_of_comments = models.IntegerField(default=0)
  number_of_pingbacks = models.IntegerField(default=0)
  rating = models.IntegerField(default=5)

  def __str__(self):
    return self.headline
  
class Dog(models.Model):
  name = models.CharField(max_length=200)
  data = models.JSONField(null=True)

  def __str__(self):
    return self.name
  
class EntryDetail(models.Model):
  entry = models.OneToOneField(Entry, on_delete=models.CASCADE)
  details = models.TextField()
  
"""
Noting here the queries I might forget

F() compares fields
Entry.objects.filter(number_of_comments__gt=F("number_of_pingbacks"))
Entry.objects.filter(rating__lt=F("number_of_comments") + F("number_of_pingbacks"))

can act like a join (__)
Entry.objects.filter(authors__name=F('blog__name'))

Entry.objects.filter(mod_date__gt=F("pub_date") + timedelta(days=3))

to find all Entry objects published in the same year as they were last modified:
Entry.objects.filter(pub_date__year=F('mod_date__year'))

from django.db.models import Min
Entry.objects.aggregate(first_published_year=Min("pub_date__year"))

finds the value of the highest rated entry and the total number of comments on all entries for each year:

from django.db.models import OuterRef, Subquery, Sum
Entry.objects.values("pub_date__year").annotate(
    top_rating=Subquery(
        Entry.objects.filter(
            pub_date__year=OuterRef("pub_date__year"),
        )
        .order_by("-rating")
        .values("rating")[:1]
    ),
    total_comments=Sum("number_of_comments"),
)

Get blogs entries with id 1, 4 and 7
Blog.objects.filter(pk__in=[1, 4, 7])

reuse Querysets to utilize the cache!
BAD:
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

GOOD:
queryset = Entry.objects.all()
print([p.headline for p in queryset])
print([p.pub_date for p in queryset])

entire queryset has to be evaluated in order to leverage the cache
example:
BAD:
queryset = Entry.objects.all()
print(queryset[5])  # Queries the database
print(queryset[5])  # Queries the database again

GOOD
queryset = Entry.objects.all()
[entry for entry in queryset]  # Queries the database
print(queryset[5])  # Uses cache
print(queryset[5])  # Uses cache

it is possible to store JSON scalar null instead of SQL NULL by using Value(None, JSONField()).
Whichever of the values is stored, when retrieved from the database,
the Python representation of the JSON scalar null is the same as SQL NULL,
i.e. None. Therefore, it can be hard to distinguish between them.

Storing JSON scalar null does not violate null=False

Transactions are not currently supported with asynchronous queries and updates.
You will find that trying to use one raises SynchronousOnlyOperation.

If you wish to use a transaction, we suggest you write your ORM code inside a separate,
synchronous function and then call that using sync_to_async 

from django.db.models.fields.json import KT
looks up JSON data:
Dog.objects.create(
    name="Shep",
    data={
        "owner": {"name": "Bob"},
        "breed": ["collie", "lhasa apso"],
    },
)
Dogs.objects.annotate(
    first_breed=KT("data__breed__1"), owner_name=KT("data__owner__name")
).filter(first_breed__startswith="lhasa", owner_name="Bob")

Dog.objects.create(name="Rufus", data={"breed": "labrador", "owner": "Bob"})
Dog.objects.create(name="Meg", data={"breed": "collie", "owner": "Bob"})
Dog.objects.filter(data__contains={"owner": "Bob"})
<QuerySet [<Dog: Rufus>, <Dog: Meg>]>

A Q object (django.db.models.Q) is an object used to encapsulate a collection of keyword arguments.
These keyword arguments are specified as in “Field lookups” above.
Q objects can be combined using the &, |, and ^ operators. When an operator is used on two Q objects, it yields a new Q object.
Q(question__startswith="Who") | Q(question__startswith="What")
SQL equivalent: WHERE question LIKE 'Who%' OR question LIKE 'What%'

Poll.objects.get(
    Q(question__startswith="Who"),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
)
SQL equivalent: 
SELECT * from polls WHERE question LIKE 'Who%'
    AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

must precede the definition of any keyword arguments.
BAD:
Poll.objects.get(
    question__startswith="Who",
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
)
GOOD:
Poll.objects.get(
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
    question__startswith="Who",
)

it is possible to easily create new instance with all fields values copied.
you can set pk to None and _state.adding to True.
blog.pk = None
blog._state.adding = True
blog.save()
doesn't copy relations that aren't part of the models database table

update() doesn't run save() you can do it in a loop of a QuerySet:
for item in query_set:
  item.save()
updating a counter with F()
Entry.objects.update(number_of_pingbacks=F("number_of_pingbacks") + 1)

MANY-TO-MANY
e = Entry.objects.get(id=3)
e.authors.all()  # Returns all Author objects for this Entry.
e.authors.count()
e.authors.filter(name__contains="John")

a = Author.objects.get(id=5)
a.entry_set.all()  # Returns all Entry objects for this Author.

if things get complicated on the Django layer, can always write raw SQL.
It’s difficult to intuit how the ORM will translate complex querysets 
into SQL queries so when in doubt, inspect the SQL with str(queryset.query)
and write plenty of tests.

Aggregations
from django.db.models import FloatField
Book.objects.aggregate(
    price_diff=Max("price", output_field=FloatField()) - Avg("price")
)

from django.db.models import Count
pubs = Publisher.objects.annotate(num_books=Count('book'))
pubs[0].num_books

from django.db.models import Q
above_5 = Count('book', filter=Q(book__rating__gt=5))
below_5 = Count('book', filter=Q(book__rating__lte=5))
pubs = Publisher.objects.annotate(below_5=below_5).annotate(above_5=above_5)
pubs[0].above_5
pubs[0].below_5

pubs = Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]
pubs[0].num_books

aggregate returns name/value pairs
Book.objects.aggregate(average_price=Avg("price"))
{'average_price': 34.35} 

q = Book.objects.annotate(Count("authors"))
q[0]
q[0].authors__count
you can override the default by providing your own alias:
q = Book.objects.annotate(num_authors=Count("authors"))
q[0].num_authors

annotate() clause is a QuerySet
aggregate() clause terminal clause

combining aggregations with annotate will result in joins
sometimes leading to WRONG results distinct may help
q = Book.objects.annotate(
    Count("authors", distinct=True), Count("store", distinct=True)
)
q[0].authors__count
q[0].store__count

When specifying the field to be aggregated in an aggregate function,
Django will allow you to use the same double underscore notation that
is used when referring to related fields in filters.
Store.objects.annotate(min_price=Min("books__price"), max_price=Max("books__price"))
Store.objects.aggregate(min_price=Min("books__price"), max_price=Max("books__price"))

annotate(): Adds aggregation to individual objects in the queryset (per Store in this case).
aggregate(): Calculates a global aggregate across the entire queryset and returns a summary.

reverse many-to-many hop:
Author.objects.annotate(total_pages=Sum("book__pages"))
If no such alias were specified: book__pages__sum
Author.objects.aggregate(average_rating=Avg("book__rating"))

using annotate with filter
Book.objects.filter(name__startswith="Django").annotate(num_authors=Count("authors"))
all books
Book.objects.filter(name__startswith="Django").aggregate(Avg("price"))

generate a list of authors with a count of highly rated books
highly_rated = Count("book", filter=Q(book__rating__gte=7))
Author.objects.annotate(num_books=Count("book"), highly_rated_books=highly_rated)

when using annotate() and filter/values() order matters!
if the values() clause precedes the annotate() clause,
any annotations will be automatically added to the results.
If the values() clause is applied after the annotate() clause,
you need to explicitly include the aggregate column.

usually you want order_by() last
"""