from django.core.cache import cache
from django.http import HttpResponse


class AdminLoginRateLimitMiddleware:
    """Lock admin login after repeated failed attempts from same IP + username."""

    MAX_FAILED_ATTEMPTS = 5
    LOCK_SECONDS = 30 * 60
    ATTEMPT_WINDOW_SECONDS = 30 * 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._is_admin_login_post(request):
            username = self._username(request)
            ip_addr = self._ip(request)
            lock_key = self._lock_key(username, ip_addr)
            if cache.get(lock_key):
                return HttpResponse(
                    "Too many failed admin login attempts. Try again in 30 minutes.",
                    status=429,
                    content_type="text/plain",
                )

        response = self.get_response(request)

        if self._is_admin_login_post(request):
            username = self._username(request)
            ip_addr = self._ip(request)
            attempts_key = self._attempts_key(username, ip_addr)
            lock_key = self._lock_key(username, ip_addr)

            is_success = bool(getattr(request, "user", None) and request.user.is_authenticated and response.status_code in (301, 302, 303))
            if is_success:
                cache.delete(attempts_key)
                cache.delete(lock_key)
            else:
                attempts = cache.get(attempts_key, 0) + 1
                cache.set(attempts_key, attempts, timeout=self.ATTEMPT_WINDOW_SECONDS)
                if attempts >= self.MAX_FAILED_ATTEMPTS:
                    cache.set(lock_key, 1, timeout=self.LOCK_SECONDS)

        return response

    @staticmethod
    def _is_admin_login_post(request):
        return request.method == "POST" and request.path.rstrip("/") == "/admin/login"

    @staticmethod
    def _username(request):
        return (request.POST.get("username") or "").strip().lower()[:150] or "unknown"

    @staticmethod
    def _ip(request):
        forwarded = (request.META.get("HTTP_X_FORWARDED_FOR") or "").split(",")[0].strip()
        return forwarded or request.META.get("REMOTE_ADDR", "unknown")

    @staticmethod
    def _attempts_key(username, ip_addr):
        return f"admin_login_fail:{username}:{ip_addr}"

    @staticmethod
    def _lock_key(username, ip_addr):
        return f"admin_login_lock:{username}:{ip_addr}"
