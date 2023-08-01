from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, UpdateView, CreateView, ListView
from django.template.defaultfilters import slugify
from unidecode import unidecode

from blog.forms import BlogPostFilterForm, BlogPostForm
from blog.models import BlogPost


# Create your views here.
class BlogPostListView(ListView):
    """
    Класс представления для списка блогов.
    Отображает список блогов и позволяет фильтровать их по параметру is_published.
    """
    model = BlogPost
    template_name = 'catalog/blog_page/blog_base.html'
    context_object_name = 'blog_posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        Добавляет форму фильтрации блогов в контекст страницы.
        """
        context = super().get_context_data(**kwargs)
        context['filter_form'] = BlogPostFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset блогов в зависимости от параметра is_published.
        """
        queryset = super().get_queryset()
        is_published = self.request.GET.get('is_published')

        if is_published:
            queryset = queryset.filter(is_published=True)

        return queryset


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """
    Класс представления для создания блога.
    Отображает форму создания блога и сохраняет данные блога при успешной валидации формы.
    """
    model = BlogPost
    template_name = 'catalog/blog_page/blog_post_create.html'
    success_url = reverse_lazy('blog:blog_base_page')
    form_class = BlogPostForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет данные блога.
        Генерирует уникальный slug на основе заголовка блога и устанавливает количество просмотров в 0.
        """
        instance = form.save(commit=False)
        title = instance.title
        slug = slugify(unidecode(title))
        if BlogPost.objects.filter(slug=slug).exists():
            form.errors['title'] = form.error_class(['Блог с таким названием уже существует.'])
            return self.form_invalid(form)
        instance.slug = slug

        views_count = self.request.POST.get('views_count', '')
        instance.views_count = int(views_count) if views_count else 0

        instance.save()
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс представления для обновления блога.
    Отображает форму обновления блога и сохраняет измененные данные блога при успешной валидации формы.
    """
    model = BlogPost
    template_name = 'catalog/blog_page/blog_post_update.html'
    context_object_name = 'blog_post'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    form_class = BlogPostForm

    def form_valid(self, form):
        """
        Проверяет валидность формы и сохраняет измененные данные блога.
        Устанавливает автора блога на текущего пользователя.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Возвращает URL для перенаправления после успешного обновления блога.
        """
        return reverse_lazy('blog:blog_post_detail', kwargs={'slug': self.object.slug})


class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    """
    Класс представления для удаления блога.
    Отображает подтверждающий экран удаления блога и удаляет блог при подтверждении.
    """
    model = BlogPost
    template_name = 'catalog/blog_page/blog_delete.html'
    context_object_name = 'blog_post'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    success_url = reverse_lazy('blog:blog_base_page')


class BlogPostDetailView(DetailView):
    """
    Класс представления для детального просмотра блога.
    Отображает полную информацию о блоге и увеличивает счетчик просмотров при каждом просмотре.
    """
    model = BlogPost
    template_name = 'catalog/blog_page/blog_post_detail.html'
    context_object_name = 'blog_post'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        """
        Увеличивает счетчик просмотров блога при каждом просмотре.
        """
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)