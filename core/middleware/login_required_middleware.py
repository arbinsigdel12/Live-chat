from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLS = [
    reverse('account_login'), 
    reverse('account_signup'), 
    reverse('account_logout'),
    '/admin/',
    '/static/',  # if you serve static files without whitenoise or similar
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if not request.user.is_authenticated:
            # Allow exempt URLs
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                return redirect('account_login')

        response = self.get_response(request)
        return response
