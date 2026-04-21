from django.utils import timezone
from .models import Profile

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Обновляем время только если это НЕ фоновый запрос к API чата
            if not request.path.startswith('/messages/api/'):
                Profile.objects.filter(user=request.user).update(last_seen=timezone.now())
        
        return self.get_response(request)