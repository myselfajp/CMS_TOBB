from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import logout,login,authenticate

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
                return redirect("/companies")
        return render(request,"login.html",{"message":message})
    else:
        if request.method=="POST":
            return redirect("/companies")
        if request.user.username=="Ali" or request.user.username=="admin":
            return render(request,"user/index.html",{"message":message})
        return HttpResponseRedirect("/companies")

def http_logout(request):
    logout(request)
    return redirect('/')