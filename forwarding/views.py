from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from unidecode import unidecode

from forwarding.forms import ClientsForm, ClientsCreateForm
from forwarding.models import Clients


# Create your views here.
def home_page(request):
    # Отображение домашней страницы
    return render(request, 'forwarding/home_page.html')


class ClientsView(ListView):
    """Show all clients for owner / moderator / admin"""
    model = Clients
    template_name = "forwarding/client/clients.html"

    def get_queryset(self):
        queryset = super().get_queryset().all()
        if not self.request.user.is_staff:
            queryset = super().get_queryset().filter(owner=self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Title"] = "Clients"
        context["Clients"] = self.get_queryset()
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
            form.errors['full_name'] = form.error_class(['Клиент с таким названием уже существует.'])
            return self.form_invalid(form)
        instance.slug = slug

        views_count = self.request.POST.get('views_count', '')
        instance.views_count = int(views_count) if views_count else 0

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
        Проверяет валидность формы и сохраняет измененные данные блога.
        Устанавливает автора блога на текущего пользователя.
        """
        form.instance.author = self.request.user
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