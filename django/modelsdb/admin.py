from django.contrib import admin

from .models import Person, Musician, Album, Publisher

admin.site.register(Person)
admin.site.register(Musician)
admin.site.register(Album)

admin.site.register(Publisher)