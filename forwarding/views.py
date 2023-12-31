from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from unidecode import unidecode
import config.settings
from blog.models import BlogPost
from config import settings
from forwarding.forms import ClientsForm, ClientsCreateForm, MessagesCreateForm, TransmissionForm, \
    MessagesFormUpdate
from forwarding.models import Clients, Messages, Transmission


# Create your views here.
def home_page(request):
    # Отображение домашней страницы
    return render(request, 'forwarding/home_page.html')


class ClientsView(LoginRequiredMixin, ListView):
    """Show all clients for owner / moderator / admin"""
    model = Clients
    context_object_name = 'Clients'

    template_name = "forwarding/client/clients.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ClientsCreateView(LoginRequiredMixin, CreateView):
    """
    Класс представления для создания блога.
    Отображает форму создания блога и сохраняет данные блога при успешной валидации формы.
    """
    model = Clients
    template_name = 'forwarding/client/client_create.html'
    success_url = reverse_lazy('forwarding:clients')
    form_class = ClientsCreateForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные блога.
        Генерирует уникальный slug на основе заголовка блога и устанавливает количество просмотров в 0.
        """
        instance = form.save(commit=False)
        title = instance.full_name
        slug = slugify(unidecode(title))
        if Clients.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.slug = slug
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)


class ClientsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс представления для обновления блога.
    Отображает форму обновления блога и сохраняет измененные данные блога при успешной валидации формы.
    """
    model = Clients
    template_name = 'forwarding/client/client_update.html'
    context_object_name = 'client'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:clients')

    form_class = ClientsForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные передачи.
        Генерирует уникальный slug на основе заголовка передачи и устанавливает владельца на текущего пользователя.
        """
        instance = form.save(commit=False)
        slug = slugify(unidecode(instance.full_name))
        if Clients.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.save()
        return super().form_valid(form)


class ClientsDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс представления для удаления клиента.
    Отображает подтверждающий экран удаления клиента и удаляет его при подтверждении.
    """
    model = Clients
    template_name = 'forwarding/client/client_delete.html'
    context_object_name = 'client'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:clients')


class ClientsDetailView(DetailView):
    """
    Класс представления для детального просмотра блога.
    Отображает полную информацию о блоге и увеличивает счетчик просмотров при каждом просмотре.
    """
    model = Clients
    template_name = 'forwarding/client/client_detail.html'
    context_object_name = 'client'
    slug_url_kwarg = 'slug'


class MessagesView(LoginRequiredMixin, ListView):
    """Show all messages for owner / moderator / admin"""

    model = Messages  # Use the Messages model
    template_name = "forwarding/message/messages.html"  # Updated template path
    context_object_name = 'Messages'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MessagesDetailView(DetailView):
    model = Messages
    template_name = 'forwarding/message/message_detail.html'
    context_object_name = 'Message'
    slug_url_kwarg = 'slug'


class MessagesCreateView(LoginRequiredMixin, CreateView):
    """
    Class-based view for creating a new message.
    Displays the message creation form and saves the data upon successful form validation.
    """
    model = Messages
    template_name = 'forwarding/message/message_create.html'
    success_url = reverse_lazy('forwarding:messages')
    form_class = MessagesCreateForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные передачи.
        Генерирует уникальный slug на основе заголовка передачи и устанавливает владельца на текущего пользователя.
        """
        instance = form.save(commit=False)
        title = instance.theme
        slug = slugify(unidecode(title))
        if Messages.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.slug = slug
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)


class MessagesUpdateView(LoginRequiredMixin, UpdateView):
    """
    Class-based view for updating a message.
    Displays the message update form and saves the modified message data upon successful form validation.
    """
    model = Messages
    template_name = 'forwarding/message/message_update.html'
    context_object_name = 'message'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:messages')

    form_class = MessagesFormUpdate

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные передачи.
        Генерирует уникальный slug на основе заголовка передачи и устанавливает владельца на текущего пользователя.
        """
        instance = form.save(commit=False)
        title = instance.theme
        slug = slugify(unidecode(title))
        if Messages.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.slug = slug
        instance.save()
        return super().form_valid(form)


class MessagesDeleteView(LoginRequiredMixin, DeleteView):
    """
    Class-based view for deleting a message.
    Displays the confirmation screen for message deletion and deletes the message upon confirmation.
    """
    model = Messages
    template_name = 'forwarding/message/message_delete.html'
    context_object_name = 'message'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:messages')


class TransmissionListView(LoginRequiredMixin, ListView):
    """Показывает все передачи для владельца / модератора / администратора"""

    model = Transmission  # Используем модель Transmission
    template_name = "forwarding/transmissions/transmissions.html"  # Обновленный путь к шаблону
    context_object_name = 'Transmission'
    ordering = 'time'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TransmissionDetailView(DetailView):
    model = Transmission
    template_name = 'forwarding/transmissions/transmission_detail.html'
    context_object_name = 'Transmission'
    slug_url_kwarg = 'slug'


class TransmissionCreateView(LoginRequiredMixin, CreateView):
    """
    Класс-представление для создания новой передачи.
    Отображает форму создания передачи и сохраняет данные при успешной валидации формы.
    """
    model = Transmission
    template_name = 'forwarding/transmissions/transmission_create.html'
    success_url = reverse_lazy('forwarding:transmissions')
    form_class = TransmissionForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные передачи.
        Генерирует уникальный slug на основе заголовка передачи и устанавливает владельца на текущего пользователя.
        """
        instance = form.save(commit=False)
        title = instance.title
        slug = slugify(unidecode(title))
        if Transmission.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.slug = slug
        instance.owner = self.request.user
        instance.save()
        return super().form_valid(form)


class TransmissionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс-представление для обновления передачи.
    Отображает форму обновления передачи и сохраняет измененные данные при успешной валидации формы.
    """
    model = Transmission
    template_name = 'forwarding/transmissions/transmission_update.html'
    context_object_name = 'Transmission'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:transmissions')

    form_class = TransmissionForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные передачи.
        Генерирует уникальный slug на основе заголовка передачи.
        """
        instance = form.save(commit=False)
        title = instance.title
        slug = slugify(unidecode(title))
        if Transmission.objects.filter(slug=slug).exists():
            return self.form_invalid(form)
        instance.slug = slug
        instance.save()
        return super().form_valid(form)


class TransmissionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс-представление для удаления передачи.
    Отображает экран подтверждения удаления передачи и удаляет передачу после подтверждения.
    """
    model = Transmission
    template_name = 'forwarding/transmissions/transmission_delete.html'
    context_object_name = 'Transmission'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('forwarding:transmissions')


class SendTransmissionView(View):
    # Указываем шаблон, который будет использован для отображения страницы
    template_name = 'forwarding/transmissions/transmission_send.html'

    # Обработчик GET-запроса
    def get(self, request, *args, **kwargs):
        try:
            # Получаем значение slug из параметров запроса
            slug = self.kwargs.get('slug')
            # Ищем объект передачи (Transmission) по переданному slug
            transmission = Transmission.objects.get(slug=slug)
        except Transmission.DoesNotExist:
            # Если передача не найдена, возвращаем HTTP-ответ со статусом 404 (страница не найдена)
            return HttpResponse("Передача не найдена.", status=404)

        # Формируем контекст данных для отображения на странице
        context = {
            'transmission': transmission,
        }
        # Отображаем страницу с переданным контекстом
        return render(request, self.template_name, context)

    # Обработчик POST-запроса
    def post(self, request, *args, **kwargs):
        try:
            # Получаем значение slug из параметров запроса
            slug = self.kwargs.get('slug')
            # Ищем объект передачи (Transmission) по переданному slug
            transmission = Transmission.objects.get(slug=slug)
        except Transmission.DoesNotExist:
            # Если передача не найдена, возвращаем HTTP-ответ со статусом 404 (страница не найдена)
            return HttpResponse("Передача не найдена.", status=404)

        # Получаем связанный объект сообщения (Messages) для передачи
        message = transmission.message
        if message:
            # Если есть сообщение, отправляем письмо каждому клиенту из списка
            for client in transmission.clients.all():
                send_mail(
                    message.theme,  # Используем тему из модели Messages в качестве темы электронной почты
                    message.body,  # Используем тело из модели Messages в качестве тела электронной почты
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email],  # Предполагается, что у модели Client есть поле 'email'
                )

        # Обновляем статус передачи после отправки сообщений
        transmission.status = Transmission.TransmissionStatus.Finished
        transmission.save()

        # Перенаправляем пользователя обратно на список передач или другую желаемую страницу
        return redirect('forwarding:transmissions')


class MainView(ListView):
    """Main page with blog and statistic"""
    model = Messages
    template_name = "forwarding/main.html"

    def get_queryset(self):
        """Execute blog part cash on main page"""
        if config.settings.CACHE_ENABLED:
            key = 'main_blog'
            cache_data = cache.get(key)
            if cache_data is None:
                cache_data = BlogPost.objects.order_by('?')[:3]
                cache.set(key, cache_data)
        else:
            cache_data = BlogPost.objects.order_by('?')[:3]
        return cache_data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Main"
        # show blogs
        context["Blog"] = self.get_queryset()
        # show statistic
        context["all_transmissions"] = len(Transmission.objects.all())
        context["active_transmissions"] = len(Transmission.objects.filter(is_published=True))
        context["all_clients"] = len(Clients.objects.all())
        context["unique_clients"] = len(Clients.objects.all().values('email').distinct())
        return context
