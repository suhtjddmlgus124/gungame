from django.utils.functional import SimpleLazyObject
from .models import Profile

class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.profile = SimpleLazyObject(
            lambda: self._get_profile(request)
        )
        return self.get_response(request)

    def _get_profile(self, request):
        user = getattr(request, 'user', None)
        if not user or user.is_anonymous:
            return None
        try:
            return user.profile
        except Profile.DoesNotExist:
            return None