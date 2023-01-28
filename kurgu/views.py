from django.shortcuts import render

# Create your views here.
def http_kj_kurgu(request):
    return render(request,"kurgu/ks_kurgu.html")
    