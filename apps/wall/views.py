from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
    
# Create your views here.
def wall_index(request):
    return render(request, "index.html")

def hello_name(request, name):
    if request.method == "GET":
        context = {
            "htmlname": name,
            "namelist": ["Andres", "Eduardo", "Matias"]
        }
        return render(request, "index.html", context)
    else:
        return redirect('app_index')