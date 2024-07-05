from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip authentication for admin and static files
        if request.path.startswith("/admin") or request.path.startswith("/static/"):
            return None

        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token_name, token_key = auth_header.split(" ")
                if token_name.lower() != "token" or not token_key:
                    return JsonResponse(
                        {"detail": "Invalid token header. Token keyword missing or token is empty."}, status=401
                    )

                try:
                    token = Token.objects.get(key=token_key)
                    request.user = token.user
                except Token.DoesNotExist:
                    return JsonResponse({"detail": "Invalid token."}, status=401)
            except ValueError:
                return JsonResponse({"detail": "Invalid token header. No credentials provided."}, status=401)
        else:
            request.user = AnonymousUser()
        return None
