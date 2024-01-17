from django.contrib import admin

from core.models import ProfileImage, Comment, Notification, ViewCount


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'date_create')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_create')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification_type', 'to_user', 'from_user', 'date', 'user_has_seen')
    list_editable = ('user_has_seen',)


admin.site.register(ViewCount)
