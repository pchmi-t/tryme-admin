from django.contrib import admin
from trymeadmin.models import Answer, Question, Category, Test

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Test)