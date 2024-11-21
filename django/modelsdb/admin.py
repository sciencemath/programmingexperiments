from django.contrib import admin

from .models import Person, Musician, Album

admin.site.register(Person)
admin.site.register(Musician)
admin.site.register(Album)