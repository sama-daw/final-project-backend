from django.shortcuts import render

def api_home(request):
    """
    صفحة ترحيبية للـ API
    """
    return render(request, 'home.html')
