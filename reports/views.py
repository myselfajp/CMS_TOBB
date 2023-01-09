from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from crawler.models import Companies,Status,Cities
from django.contrib.auth.models import User
from django.shortcuts import render
import datetime

# Create your views here.
@csrf_exempt
@login_required
def http_companies(request):
    statuses = Status.objects.all()
    cities = Cities.objects.all()
    users = User.objects.all()
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if request.method == 'GET':
        companies = Companies.objects.filter(user=request.user).order_by("-last_status")
        remine_companies = companies.filter(reminder__lte=now)
    filters= {
        "last_status_filter":{"name":"Tümü","value":"0"},
        "tel_filter":{"name":"Tümü","value":"0"},
        "city_filter":{"name":"Tümü","value":"0"},
        "user_filter":{"name":"Tümü","value":"0"},
        "search":"",}

    count=500
    if request.method == 'POST':

        if request.POST.get('company_id'):
            try:
                company = Companies.objects.get(id=request.POST.get('company_id'))
                company.note=request.POST.get('note')
                company.full_name = request.POST.get('fullname')
                new_status=request.POST.get('status_add')
                new_status=Status.objects.get(id=int(new_status))
                company.status.add(new_status)
                company.last_status = new_status
                company.save()
            except:
                pass
  

        #-----------------------------------------------------------admin share---------------------------------------
        if request.POST.get('user_filter'):
            if request.POST.get('user_filter') != "0":
                companies = Companies.objects.filter(user__id = request.POST.get('user_filter')).order_by("name")
                x=users.get(id=request.POST.get('user_filter'))
                filters["user_filter"]["name"]=x.username
                filters["user_filter"]["value"]=x.id
            else:
                companies = Companies.objects.all().order_by("name")
            if request.POST.get('count'):
                count=int(request.POST.get('count'))
        else:
            companies = Companies.objects.filter(user=request.user).order_by("-last_status")
        
        if request.POST.get('transfer'):
            user_to=users.get(id=request.POST.get('transfer_to'))
            companies_to=[]
            all_posts=request.POST.items()
            for k,v in all_posts:
                if k[:4]=="take":
                    companies_to.append(v)
            Companies.objects.filter(id__in=companies_to).update(user=user_to)

        #--------------------------------------------------------------------------------------------------------------

        #----------------------------------------------------------filters--------------------------------------------

        remine_companies = companies.filter(reminder__lte=now)

        if request.POST.get('search'):
            s=request.POST.get('search')
            companies = companies.filter(phone__contains=s)
            filters["search"]=s

        if not filters["search"]:
            if request.POST.get('last_status_filter'):
                if request.POST.get('last_status_filter') != "0":
                    companies = companies.filter(last_status__id = request.POST.get('last_status_filter'))
                    x=Status.objects.get(id=request.POST.get('last_status_filter'))
                    filters["last_status_filter"]["name"]=x.name
                    filters["last_status_filter"]["value"]=x.id

            if request.POST.get('tel_filter'):
                if request.POST.get('tel_filter') != "0":
                    if request.POST.get('tel_filter')=="tel":
                        companies = companies.filter(phone__istartswith="5")
                        filters["tel_filter"]["value"]="tel"
                        filters["tel_filter"]["name"]="Cep"
                    else:
                        companies = companies.exclude(phone__istartswith="5")
                        filters["tel_filter"]["value"]="office"
                        filters["tel_filter"]["name"]="Sabit"

            if request.POST.get('city_filter'):
                if request.POST.get('city_filter') != "0":
                    companies = companies.filter(city__id = request.POST.get('city_filter'))
                    x=cities.get(id=request.POST.get('city_filter'))
                    filters["city_filter"]["name"]=x.name
                    filters["city_filter"]["value"]=x.id
            
        #----------------------------------------------------------filters--------------------------------------------

    return render(request,"companies.html",{'companies': companies[:count],'users':users,'statuses':statuses,"cities":cities,"remine_companies":remine_companies,"filters":filters})


@login_required
def http_company(request,company_id):
    if request.method == 'POST':
        company = Companies.objects.get(id=company_id)
        company.note=request.POST.get('note')
        company.full_name = request.POST.get('fullname')
        new_status=request.POST.get('status_add')

        new_status=Status.objects.get(id=int(new_status))
        company.status.add(new_status)
        company.last_status = new_status
        company.save()
    company = Companies.objects.get(id=company_id)
    statuses = Status.objects.all()
    last_status = company.last_status
    return render(request,"company.html",{'company': company,'statuses':statuses,"last_status":last_status})


@login_required
def http_send_mail(request):
    message=''
    if request.method == "POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        if fullname and email:
            subject, from_email = f'{fullname}', 'iletisim@sektorunonculeri.com'
            text_content = '''
            MERHABALAR EFENDİM
            SHOWTURK TE YAYINLANAN VE EŞ ZAMANDA 64 ÜLKEDE YAYIN İMKANI OLAN  SEKTÖREL HABER PROGRAMIMIZ VE AYNI ZAMANDA REKLAM İÇERİĞİ OLAN KONSEPTİYLE SİZ DEĞERLİ FİRMA SAHİPLERİNİ VE ALANINDAKİ ÇALIŞMALARINI TANITTIĞIMIZ SUNUCULUĞUNU ESRA BALAMİRİN ÜSTLENDİĞİ , ESRA BALAMİR İLE SEKTÖRÜN ÖNCÜLERİ PROGRAMIMIZDA SİZLEREDE YER VERMEK İSTERİZ. TARAFINIZA YÖNLENDİRİLMİŞ OLAN LANSMAN TANITIMIMIZI LÜTFEN İNCELEYİNİZ UYGUN GÖRDÜĞÜNÜZ TAKDİRDE BİRLİKTE BİR ÇALIŞMA YAPMAKTAN MEMNUNİYET DUYARIZ. SEKTÖRÜN ÖNCÜLERİ AİLESİ OLARAK İŞ HAYATINIZDA BAŞARILAR  DİLERİZ.
            '''
            try:
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_file('LANSMAN - SEKTÖRÜN ÖNCÜLERİ.pdf')
                msg.send()
                message='Başarılıyla gönderildi'
            except:
                message="Mail gönderilmedi."
        else:
            message = "Boşlukları doldurmanız gerekiyor"

    return render(request,"send_mail.html",{"message":message})

@csrf_exempt
@login_required
def http_reminder(request,company_id):
    message=''
    if request.method == "POST":
        company = Companies.objects.get(id=company_id)
        company.reminder = request.POST.get('time')
        company.save()
        message='Hatırlatma kaydedildi'
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return render(request,"reminder.html",{"message":message,"now":now,"company":company_id})


@csrf_exempt
@login_required
def http_reminder_report(request):
    if request.method == "POST":
        company = Companies.objects.get(id=request.POST.get("company_id"))
        company.reminder = None
        company.save()
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
    companies = Companies.objects.filter(user=request.user).exclude(reminder__isnull=True)
    lte = companies.filter(reminder__lte=now)
    gte = companies.exclude(reminder__lte=now)
    return render(request,"reminder_report.html",{"lte":lte,"gte":gte})
