from django.urls import path

from forwarding.views import home_page, ClientsView, ClientsDeleteView, ClientsUpdateView, ClientsCreateView, \
    ClientsDetailView

app_name = "forwarding"

urlpatterns = [
    path('', home_page, name='home_page'),
    path("clients/", ClientsView.as_view(), name="clients"),
    path("client_create/", ClientsCreateView.as_view(), name="client_create"),
    path("client_delete/<slug:slug>", ClientsDeleteView.as_view(), name="client_delete"),
    path("client_update/<slug:slug>", ClientsUpdateView.as_view(), name="client_update"),
    path("client_card/<slug:slug>", ClientsDetailView.as_view(), name="client_card"),
]