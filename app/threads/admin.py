from django.contrib import admin
from .models import Thread, Comment, Categories, ThreadCategory

# Register your models here.


admin.site.register(Thread)
admin.site.register(ThreadCategory)
admin.site.register(Comment)
admin.site.register(Categories)
