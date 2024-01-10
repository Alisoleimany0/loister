from django.shortcuts import render


def http404(request, exception):
    return render(request, '404.html', status=404)
