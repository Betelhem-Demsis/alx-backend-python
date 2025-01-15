import datetime
import time
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_message)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.datetime.now().hour
        if current_hour < 18 or current_hour >= 21: 
            return HttpResponseForbidden("Access to chat is restricted at this time.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        if request.method == "POST":
            ip = self.get_client_ip(request)
            current_time = time.time()

            if ip not in self.requests:
                self.requests[ip] = []
            self.requests[ip] = [
                t for t in self.requests[ip] if current_time - t < 60
            ]  
            if len(self.requests[ip]) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: Only 5 messages per minute are allowed.")

            self.requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/chat/"):  
            user = request.user
            if not user.is_authenticated or not user.groups.filter(name__in=["admin", "moderator"]).exists():
                return HttpResponseForbidden("You do not have permission to access this resource.")
        return self.get_response(request)
