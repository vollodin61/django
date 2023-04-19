from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.forms.forms import BaseForm
from django.shortcuts import reverse

from myauth.forms import ProfileForm
from myauth.models import Profile, ProfileImage


# class AboutMeView(DetailView):
    # template_name = 'myauth/about-me.html'
    # model = User
    # context_object_name = 'user_profile'
class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'myauth/profile_update_form.html'
    model = Profile
    fields = 'avatar', 'bio'

    def test_func(self):
        return self.request.user.id == self.request.user.profile.id or \
            self.request.user.is_superuser or \
            self.request.user.is_staff

    def get_success_url(self):
        return reverse('myauth:about-me')


# class ProfileUpdateView(UserPassesTestMixin, UpdateView):
#     model = Profile
#     template_name_suffix = '_update_form'
#     permission_required = 'change_profile'
#     form_class = ProfileForm
#     context_object_name = 'user_profile'
#
#     def get_success_url(self):
#         return reverse(
#             'myauth:about-me',
#             # kwargs={'pk': self.object.pk}
#         )
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         for image in form.files.getlist('images'):
#             ProfileImage.objects.create(
#                 profile=self.object,
#                 image=image,
#             )
#         return response
#
#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#
#         profile = self.get_object()
#         permissions = self.request.user.get_all_permissions()
#         return ('myauth.change_profile' in permissions) \
#             and (profile.pk == self.request.user.pk)


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request,
                            username=username,
                            password=password,)
        login(request=self.request, user=user)
        return response


@user_passes_test(lambda u: u.is_superuser)  # Эта проверка может увести в цикл, т.к. там редирект на авторизацию
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value {value!r}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
