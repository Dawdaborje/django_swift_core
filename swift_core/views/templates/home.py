from django.shortcuts import render


def home(request):
    return render(request, "swift_core/home.html", {"message": "Hello from HTMX!"})
