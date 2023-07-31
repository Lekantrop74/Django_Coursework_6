from django.urls import path

from forwarding.views import home_page

app_name = "forwarding"

urlpatterns = [
    path('', home_page, name='home_page'),
    ]