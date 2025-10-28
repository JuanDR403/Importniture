from urllib.parse import quote

from django.conf import settings
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    """
    Redirects to LOGIN_URL when the user is not authenticated, except for
    a small set of exempt paths (login, register, admin and static files).
    Place after AuthenticationMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Normalize exempt paths with trailing slashes as they are configured
        login_path = settings.LOGIN_URL if settings.LOGIN_URL.startswith('/') else f"/{settings.LOGIN_URL}"
        register_path = '/usuarios/register/'
        admin_path = '/admin/'
        static_url = settings.STATIC_URL if getattr(settings, 'STATIC_URL', '/static/') else '/static/'
        if not static_url.startswith('/'):
            static_url = '/' + static_url
        self.exempt_prefixes = (
            login_path,
            login_path.rstrip('/'),  # also allow without trailing slash
            register_path,
            register_path.rstrip('/'),
            admin_path,
            static_url,
            '/static/',  # safety fallback
        )

    def __call__(self, request):
        path = request.path or '/'

        # Exempt GET for favicon and common assets quickly
        if path in ('/favicon.ico', '/robots.txt'):
            return self.get_response(request)

        # Allow exempted prefixes (login, register, admin, static)
        if any(path == p or path.startswith(p) for p in self.exempt_prefixes):
            return self.get_response(request)

        # If not authenticated, redirect to login with next param
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL
            # Ensure absolute path
            if not login_url.startswith('/'):
                login_url = '/' + login_url
            return redirect(f"{login_url}?next={quote(path)}")

        return self.get_response(request)
