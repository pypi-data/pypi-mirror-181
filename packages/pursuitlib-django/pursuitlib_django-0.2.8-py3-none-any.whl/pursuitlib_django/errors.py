from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# The site-specific error templates are supposed to be present in "error/<error_code>.html"


def error_400(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "error/400.html")


def error_403(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "error/403.html")


def error_404(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, "error/404.html")


def error_500(request: HttpRequest) -> HttpResponse:
    return render(request, "error/500.html")
