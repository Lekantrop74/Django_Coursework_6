from django.urls import path
from django.views.generic import RedirectView

from .views import (
    BlogPostListView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    BlogPostDetailView,
)
app_name = "blog"

urlpatterns = [
    path('blog_page/blog_base/', BlogPostListView.as_view(), name='blog_base_page'),
    path('blog_page/blog_post_detail/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('blog_page/blog_base/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blog_post_update'),
    path('blog_page/blog_base/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blog_post_delete'),
    path('blog_page/blog_base/blog_post_create', BlogPostCreateView.as_view(), name='blog_post_create'),

]