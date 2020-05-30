from django.contrib import admin
from .models import book
from .models import hits
from .models import user

admin.site.register(book)
admin.site.register(hits)
admin.site.register(user)
