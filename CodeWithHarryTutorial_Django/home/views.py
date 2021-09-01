from django.shortcuts import render
from datetime import datetime
from .models import Contact
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact_obj = Contact(name=name, phone=phone, email=email, desc=desc,
                              date=datetime.today())
        contact_obj.save()
        messages.success(request, "Your message has been sent")
    return render(request, 'contact.html')