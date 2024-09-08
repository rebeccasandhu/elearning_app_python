from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications = request.user.notifications.filter(is_read=False).order_by('-created_at')
        return {
            'unread_notifications': unread_notifications,
        }
    return {}