from django.urls import path
from django.views.generic import RedirectView

from forwarding.views import home_page, ClientsView, ClientsDeleteView, ClientsUpdateView, ClientsCreateView, \
    ClientsDetailView, MessagesView, MessagesCreateView, MessagesDeleteView, MessagesUpdateView, MessagesDetailView, \
    TransmissionListView, TransmissionCreateView, TransmissionDeleteView, TransmissionUpdateView, \
    TransmissionDetailView, SendTransmissionView, MainView

app_name = "forwarding"

urlpatterns = [
    path('main_page/', MainView.as_view(), name="main_page"),

    path('', home_page, name='home_page'),

    path("clients/", ClientsView.as_view(), name="clients"),
    path("client_create/", ClientsCreateView.as_view(), name="client_create"),
    path("client_delete/<slug:slug>", ClientsDeleteView.as_view(), name="client_delete"),
    path("client_update/<slug:slug>", ClientsUpdateView.as_view(), name="client_update"),
    path("client_card/<slug:slug>", ClientsDetailView.as_view(), name="client_card"),

    path("messages/", MessagesView.as_view(), name="messages"),
    path("message_create/", MessagesCreateView.as_view(), name="message_create"),
    path("message_delete/<slug:slug>", MessagesDeleteView.as_view(), name="message_delete"),
    path("message_update/<slug:slug>", MessagesUpdateView.as_view(), name="message_update"),
    path("message_detail/<slug:slug>", MessagesDetailView.as_view(), name="message_detail"),

    path("transmissions/", TransmissionListView.as_view(), name="transmissions"),
    path("transmission_create/", TransmissionCreateView.as_view(), name="transmission_create"),
    path("transmission_delete/<slug:slug>", TransmissionDeleteView.as_view(), name="transmission_delete"),
    path("transmission_update/<slug:slug>", TransmissionUpdateView.as_view(), name="transmission_update"),
    path("transmission_detail/<slug:slug>", TransmissionDetailView.as_view(), name="transmission_detail"),
    path("transmission_send/<slug:slug>", SendTransmissionView.as_view(), name='transmission_send'),

]