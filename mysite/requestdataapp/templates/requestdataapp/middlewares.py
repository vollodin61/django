import time

from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):

    print('initial call')

    def middleware(request: HttpRequest):
        print('before get_response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get_response')
        return response

    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.request_time = {}
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        time_delay = 1

        if not self.request_time:
            print('It\'s first call may be')
        else:
            if (round(time.time()) - self.request_time['time'] < time_delay
                    and self.request_time['ipaddress'] == request.META.get('REMOTE_ADDR')):
                print('Слишком много запросов, подождите несколько секунд')
                return render(request, 'requestdataapp/error-request.html')

        self.request_time = {'time': round(time.time()), 'ipaddress': request.META.get('REMOTE_ADDR')}

        self.requests_count += 1
        print('requests_count', self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exception so far')
