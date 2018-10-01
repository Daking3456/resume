from django.contrib import admin
from accounts.models import User, UserProfile, Education, Skills

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(Skills)