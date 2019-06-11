from django.contrib import admin

from .models import Post, Subscribers, Courses

# admin.site.register(Post)

class PostAdmin (admin.ModelAdmin):
	list_display = ('title', 'created_at', 'modified_at')

admin.site.register(Post, PostAdmin)

class CoursesAdmin (admin.ModelAdmin):
	list_display = ('id', 'title', 'course', 'priсe', 'created_at', 'modified_at')

admin.site.register(Courses, CoursesAdmin)

class SubscribersAdmin (admin.ModelAdmin):
	list_display = ('email', 'display_courses', 'confirmation', 'randomkey')

admin.site.register(Subscribers, SubscribersAdmin)