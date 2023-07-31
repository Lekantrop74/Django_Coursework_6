import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.is_active = False
        self.object.verification_key = ''.join([str(random.randint(0, 9)) for _ in range(21)])
        cache.set(self.object.verification_key, self.object.email, timeout=600)  # 10 минут = 600 секунд

        send_mail(
            'Верификация',
            f'Для регистрации перейдите по ссылке http://localhost:8000/users/confirm_email/{self.object.verification_key}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]

        )
        redirect('users:profile')
        return super().form_valid(form)


def confirm_email(request, verification_key):
    email = cache.get(verification_key)
    if email:
        try:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            cache.delete(verification_key)  # Удаляем ключ из кэша после подтверждения
            return render(request, 'users/confirmation_success.html')  # Перенаправляем на страницу успешного подтверждения
        except User.DoesNotExist:
            # Обработка случая, если пользователя не существует
            # Вывод сообщения об ошибке или перенаправление на другую страницу
            pass
    # Обработка случая, если ключ недействителен или истек срок действия
    # Вывод сообщения об ошибке или перенаправление на другую страницу
    return render(request, 'users/confirmation_error.html')  # Перенаправляем на страницу ошибки подтверждения


class LoginView(BaseLoginView):
    model = User
    template_name = 'users/login1.html'
    success_url = reverse_lazy('users:profile')
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Аккаунт не активирован. Пожалуйста, проверьте вашу почту и подтвердите адрес электронной почты.")
            return redirect('register')  # Перенаправление на страницу входа с сообщением об ошибке.

        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    send_mail(
        subject="Вы сменили пароль",
        message=f"Ваш новый пароль {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]

    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:logout'))
