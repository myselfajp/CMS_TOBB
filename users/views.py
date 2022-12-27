from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from crawler.models import Companies,User

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
                if request.user.username=="Ali" or request.user.username=="admin":
                    return render(request,"user/index.html",{"message":message})
                companies = Companies.objects.filter(user=request.user)
                return render(request,"companies.html",{'companies': companies})
        return render(request,"login.html",{"message":message})
    else:
        if request.user.username=="Ali" or request.user.username=="admin":
            return render(request,"user/index.html",{"message":message})
        companies = Companies.objects.filter(user=request.user)
        return render(request,"companies.html",{"message":message})



def http_share(request):
    if request.user.username=="Ali" or request.user.username=="admin":
        companies = Companies.objects.filter(user=request.user)
        companies_tel = companies.filter(phone__istartswith="5")
        companies_comtel =companies.exclude(phone__istartswith="5")
        users = User.objects.all()

        context={
            "companies":companies,
            "users":users,
            "companies_tel":companies_tel,
            "companies_comtel":companies_comtel,
            }

        return render(request,"user/share.html",context=context)

