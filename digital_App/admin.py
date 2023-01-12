from django.contrib import admin
from .models import *


# Register your models here.

all_models = [Chairman, Event, Member, Notice, Notice_view, Visitor, User, Watchman, Transaction, Role]
for data in all_models:
    admin.site.register(data)