from django.contrib import admin
from movies.models import Genre, Film, Attachment

# Register your models here.
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Attachment)

