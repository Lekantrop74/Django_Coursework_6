from django.shortcuts import render


# Create your views here.
def home_page(request):
    # Отображение домашней страницы
    return render(request, 'forwarding/home_page.html')
