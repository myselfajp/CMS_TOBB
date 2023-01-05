from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import logout,login,authenticate
from crawler.models import Companies,User,Cities,Status

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



def http_share(request):
    if request.user.username=="Ali" or request.user.username=="admin":
        if request.method == "POST":
            user_get = request.POST.get('user')
            city = request.POST.get('city')
            tel_count = request.POST.get('tel_count')
            comtel_count = request.POST.get('comtel_count')

            if user_get and city and (tel_count or comtel_count):
                user_clear=User.objects.get(id=int(user_get))
                try:
                    tel_counted = Companies.objects.filter(user=request.user ,phone__istartswith="5",city__id=int(city)).order_by("?")[0:int(tel_count)]
                    for x in tel_counted:
                        x.user=user_clear
                        x.save()
                except:
                    pass
                try:
                    comtel_counted = Companies.objects.exclude(phone__istartswith="5").filter(user=request.user ,city__id=int(city)).order_by("?")[0:int(comtel_count)]
                    for z in comtel_counted:
                        z.user=user_clear
                        z.save()
                except:
                    pass


        city_count_reports={}
        companies = Companies.objects.filter(user=request.user)
        cities = Cities.objects.all()
        companies_tel = companies.filter(phone__istartswith="5")
        companies_comtel =companies.exclude(phone__istartswith="5")
        users = User.objects.all()

        for city in cities:
            city_count_reports[city.name]=(companies_tel.filter(city=city).count(),companies_comtel.filter(city=city).count())

        context={
            "cities":cities,
            "companies":companies,
            "users":users,
            "companies_tel":companies_tel,
            "companies_comtel":companies_comtel,
            "city_count_reports":city_count_reports,
            }

        return render(request,"user/share.html",context=context)

def http_logout(request):
    logout(request)
    return redirect('/')