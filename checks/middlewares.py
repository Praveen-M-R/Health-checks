from django.shortcuts import redirect

class DisableCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        # Redirect unauthenticated users to login page
        if not request.user.is_authenticated and request.path != "/login/":
            return redirect('login')

        return response
