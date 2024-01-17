from django import template
from core.models import Notification

register = template.Library()


@register.simple_tag(takes_context=True)
def get_count(context):
    user = context['request'].user
    count_notification = Notification.objects.filter(user_has_seen=False, to_user=user).count()
    return count_notification
