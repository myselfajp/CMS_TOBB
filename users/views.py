from django.shortcuts import render
from django.contrib.auth import logout,login,authenticate
from crawler.models import Companies,Status

# Create your views here.
def http_login(request):
    message=''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                companies = Companies.objects.filter(user=request.user)
                return render(request,"companies.html",{'companies': companies})
    else:
        companies = Companies.objects.filter(user=request.user)
        return render(request,"companies.html",{'companies': companies})


    return render(request,"login.html",{"message":message})

    
