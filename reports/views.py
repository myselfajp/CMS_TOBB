from crawler.models import Companies,Status,Cities,Agreement,AgreementStatus,Fount,Permision,Azexport
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from PIL import Image,ImageDraw,ImageFont
from django.shortcuts import render,redirect
from django.db.models import Q
from kurgu.models import KJ
import datetime
import os




def Agreement_maker(date1,date2,time,company,adres):
    image=Image.open("ham.jpg")

    font=ImageFont.truetype("times",18)
    draw =ImageDraw.Draw(image)


    draw.text(xy=(311,179),text=date1,fill=(0,0,0),font=font)

    draw.text(xy=(311,223),text=date2,fill=(0,0,0),font=font)

    draw.text(xy=(311,245),text=time,fill=(0,0,0),font=font)

    font=ImageFont.truetype("times",20)

    draw.text(xy=(453,330),text=company,fill=(0,0,0),font=font)

    draw.text(xy=(453,353),text=adres,fill=(0,0,0),font=font)

    # image.show()
    save_path = "Sözleşmeler/"+date1
    if not os.path.exists(save_path):
            os.makedirs(save_path)
    image.save(f"{save_path}/{company}.pdf")

# Create your views here.
@csrf_exempt
@login_required
def http_companies(request):
    statuses = Status.objects.all()
    cities = Cities.objects.all()
    users = User.objects.all()
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    permisions=Permision.objects.all()
    if request.method == 'GET':
        companies = Companies.objects.filter(user=request.user).order_by("-last_status")
        sectors = [x.sector for x in companies if x.sector]
        sectors = list(dict.fromkeys(sectors))
        remine_companies = companies.filter(reminder__lte=now)

    filters= {
        "last_status_filter":{"name":"Tümü","value":"0"},
        "tel_filter":{"name":"Tümü","value":"0"},
        "city_filter":{"name":"Tümü","value":"0"},
        "user_filter":{"name":"Tümü","value":"0"},
        "data_type_filter":{"name":"Tümü","value":"0"},
        "sector_filter":"Tümü",
        "search":"",
        }

    count=500
    if request.method == 'POST':
        companies = Companies.objects.filter(user=request.user).order_by("-last_status")
        sectors = [x.sector for x in companies if x.sector]
        sectors = list(dict.fromkeys(sectors))

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
                
                companies = Companies.objects.filter(user=request.user).order_by("-last_status")
                sectors = [x.sector for x in companies if x.sector]
                sectors = list(dict.fromkeys(sectors))
            except:
                pass
            

        #----------------------------------------------------------add new company-----------------------------------
        if request.POST.get('add_data'):
            company=Companies()
            company.user = request.user
            company.name = request.POST.get('company_name')
            company.short_name = request.POST.get('company_name')[0:11]
            company.phone = request.POST.get('company_tel')
            company.site = request.POST.get('company.site')
            company.full_name = request.POST.get('company_fullname')
            company.sector = request.POST.get('company_sector')
            company.note = request.POST.get('company_note')
            try:
                company.fount = Fount.objects.get(name=request.user.username)
            except:
                Fount(name=request.user.username).save()
                company.fount = Fount.objects.get(name=request.user.username)

            company.city = Cities.objects.get(id=int(request.POST.get('company_city')))
            company.last_status = Status.objects.get(id=int(request.POST.get('company_status')))
            company.save()

        #----------------------------------------------------------add new company-----------------------------------
        
        
         
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
            if request.POST.get('data_type_filter'):
                dt=request.POST.get('data_type_filter')
                if dt=="1":
                    companies = companies.filter(fount__name="TOBB")
                    filters["data_type_filter"]["value"]="1"
                    filters["data_type_filter"]["name"]="Bahattin"
                elif dt=="2":
                    companies = companies.filter(fount__name="GoogleMaps")
                    filters["data_type_filter"]["value"]="2"
                    filters["data_type_filter"]["name"]="Google"
                elif dt=="3":
                    companies = companies.filter(fount__name="EXCEL")
                    filters["data_type_filter"]["value"]="3"
                    filters["data_type_filter"]["name"]="EXCEL"

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

            if request.POST.get('sector_filter'):
                print(request.POST.get('sector_filter'))
                if request.POST.get('sector_filter') != "Tümü":
                    companies = companies.filter(sector = request.POST.get('sector_filter'))
                    filters["sector_filter"] = request.POST.get('sector_filter')

            
            if request.POST.get('city_filter'):
                if request.POST.get('city_filter') != "0":
                    companies = companies.filter(city__id = request.POST.get('city_filter'))
                    x=cities.get(id=request.POST.get('city_filter'))
                    filters["city_filter"]["name"]=x.name
                    filters["city_filter"]["value"]=x.id



        sectors = [x.sector for x in companies if x.sector]
        sectors = list(dict.fromkeys(sectors))

        #----------------------------------------------------------filters--------------------------------------------

    context={
        'companies': companies[:count],
        'users':users,
        'statuses':statuses,
        "cities":cities,
        "remine_companies":remine_companies,
        "filters":filters,
        "sectors":sectors,
        "permisions":permisions,
        }
    return render(request,"companies.html",context=context)





@csrf_exempt
@login_required
def http_azexport(request):
    statuses = Status.objects.all()
    cities = Cities.objects.all()
    users = User.objects.all()
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    if request.method == 'GET':
        companies = Azexport.objects.filter(user=request.user).order_by("-last_status")
        sectors = [x.sector for x in companies if x.sector]
        sectors = list(dict.fromkeys(sectors))
        remine_companies = companies.filter(reminder__lte=now)

    filters= {
        "last_status_filter":{"name":"Tümü","value":"0"},
        "tel_filter":{"name":"Tümü","value":"0"},
        "city_filter":{"name":"Tümü","value":"0"},
        "user_filter":{"name":"Tümü","value":"0"},
        "data_type_filter":{"name":"Tümü","value":"0"},
        "sector_filter":"Tümü",
        "search":"",
        }

    count=500
    if request.method == 'POST':
        companies = Azexport.objects.filter(user=request.user).order_by("-last_status")

        if request.POST.get('company_id'):
            try:
                company = Azexport.objects.get(id=request.POST.get('company_id'))
                company.note=request.POST.get('note')
                company.full_name = request.POST.get('fullname')
                new_status=request.POST.get('status_add')
                new_status=Status.objects.get(id=int(new_status))
                company.status.add(new_status)
                company.last_status = new_status
                company.save()
                
                companies = Azexport.objects.filter(user=request.user).order_by("-last_status")
            except:
                pass
            

        #----------------------------------------------------------add new company-----------------------------------
        if request.POST.get('add_data'):
            company=Azexport()
            company.user = request.user
            company.name = request.POST.get('company_name')
            company.short_name = request.POST.get('company_name')[0:11]
            company.phone = request.POST.get('company_tel')
            company.site = request.POST.get('company.site')
            company.full_name = request.POST.get('company_fullname')
            company.sector = request.POST.get('company_sector')
            company.note = request.POST.get('company_note')
            try:
                company.fount = Fount.objects.get(name=request.user.username)
            except:
                Fount(name=request.user.username).save()
                company.fount = Fount.objects.get(name=request.user.username)

            company.city = Cities.objects.get(id=int(request.POST.get('company_city')))
            company.last_status = Status.objects.get(id=int(request.POST.get('company_status')))
            company.save()

        #----------------------------------------------------------add new company-----------------------------------
        
        
         
        #-----------------------------------------------------------admin share---------------------------------------
        if request.POST.get('user_filter'):
            if request.POST.get('user_filter') != "0":
                companies = Azexport.objects.filter(user__id = request.POST.get('user_filter')).order_by("name")
                x=users.get(id=request.POST.get('user_filter'))
                filters["user_filter"]["name"]=x.username
                filters["user_filter"]["value"]=x.id
            else:
                companies = Azexport.objects.all().order_by("name")
            if request.POST.get('count'):
                count=int(request.POST.get('count'))


        if request.POST.get('transfer'):
            user_to=users.get(id=request.POST.get('transfer_to'))
            companies_to=[]
            all_posts=request.POST.items()
            for k,v in all_posts:
                if k[:4]=="take":
                    companies_to.append(v)
            Azexport.objects.filter(id__in=companies_to).update(user=user_to)

        #--------------------------------------------------------------------------------------------------------------

        #----------------------------------------------------------filters--------------------------------------------

        remine_companies = companies.filter(reminder__lte=now)

        if request.POST.get('search'):
            s=request.POST.get('search')
            companies = companies.filter(tel__contains=s)
            filters["search"]=s

        if not filters["search"]:
        
            if request.POST.get('tel_filter'):
                if request.POST.get('tel_filter') != "0":
                    if request.POST.get('tel_filter')=="tel":
                        companies = companies.exclude(tel__isnull=True)
                        filters["tel_filter"]["value"]="tel"
                        filters["tel_filter"]["name"]="Cep"

                    elif request.POST.get('tel_filter')=="office":
                        companies = companies.exclude(phone__isnull=True)
                        filters["tel_filter"]["value"]="office"
                        filters["tel_filter"]["name"]="Sabit"

            if request.POST.get('is_verified')=="2":
                companies = companies.filter(is_verified = True)

            if request.POST.get('last_status_filter'):
                if request.POST.get('last_status_filter') != "0":
                    companies = companies.filter(last_status__id = request.POST.get('last_status_filter'))
                    x=Status.objects.get(id=request.POST.get('last_status_filter'))
                    filters["last_status_filter"]["name"]=x.name
                    filters["last_status_filter"]["value"]=x.id
            if request.POST.get('data_type_filter'):
                dt=request.POST.get('data_type_filter')
                if dt=="1":
                    companies = companies.filter(fount__name="AZEXPORT")
                    filters["data_type_filter"]["value"]="1"
                    filters["data_type_filter"]["name"]="ihracat"
                elif dt=="2":
                    companies = companies.filter(fount__name="AZERBAYCANYP")
                    filters["data_type_filter"]["value"]="2"
                    filters["data_type_filter"]["name"]="azerbaycan_yp"


        sectors = [x.sector for x in companies if x.sector]
        sectors = list(dict.fromkeys(sectors))

        #----------------------------------------------------------filters--------------------------------------------

    context={
        'companies': companies[:count],
        'users':users,
        'statuses':statuses,
        "cities":cities,
        "remine_companies":remine_companies,
        "filters":filters,
        "sectors":sectors,
        }
    return render(request,"companies_azexport.html",context=context)


@login_required
def http_company_azexport(request,company_id):
    if request.method == 'POST':
        company = Azexport.objects.get(id=company_id)
        company.note=request.POST.get('note')
        company.full_name = request.POST.get('fullname')
        new_status=request.POST.get('status_add')
        new_status=Status.objects.get(id=int(new_status))
        company.status.add(new_status)
        company.last_status = new_status
        company.save()
    company = Azexport.objects.get(id=company_id)
    statuses = Status.objects.all()
    last_status = company.last_status
    return render(request,"company_azexport.html",{'company': company,'statuses':statuses,"last_status":last_status})


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


@login_required
def http_send_agreement(request,company_id):
    message=''
    now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") 
    company = Companies.objects.get(id=company_id)
    agreement = Agreement()
    if request.method == "POST":
            agreement.user=request.user
            agreement.company_name=company
            if request.POST.get("fullname"):
                agreement.person_name=request.POST.get("fullname")
            if request.POST.get("tel"):
                agreement.person_number = request.POST.get("tel")
            if request.POST.get("adres"):
                agreement.record_place = request.POST.get("adres")
            if request.POST.get("whatsapp"):
                agreement.whatsapp = request.POST.get("whatsapp")
            if request.POST.get("mail"):
                agreement.mail = request.POST.get("mail")
            if request.POST.get("created_date"):
                agreement.created_date = request.POST.get("created_date")
            if request.POST.get("record_date"):
                agreement.record_date = request.POST.get("record_date")
            try:
                agreement.save()
                message="kayd edildi"

            except Exception as e:
                print(e)
                message="Hata oluştu,bilgileri tam girdiğinizden emin olunuz"
    return render(request,"agreement.html",{"message":message,"company":company,"now":now})


@login_required
def http_report_agreement(request):
    agreements = Agreement.objects.all().order_by("updated_date").order_by("status__name")
    statuses = AgreementStatus.objects.all()
    filters= {
        "status_filter":{"name":"Tümü","value":"0"},
            }
    if request.method == 'POST':
        if request.POST.get('status_filter'):
            if request.POST.get('status_filter') != "0":
                agreements = agreements.filter(status__id = request.POST.get('status_filter')).order_by("updated_date")
                x=AgreementStatus.objects.get(id=request.POST.get('status_filter'))
                filters["status_filter"]["name"]=x.name
                filters["status_filter"]["value"]=x.id
            else:
                agreements = Agreement.objects.all().order_by("updated_date").order_by("status__name")
        else:
            agreements = Agreement.objects.all().order_by("updated_date").order_by("status__name")
        
    return render(request,"user/agreement_report.html",{"agreements":agreements,"filters":filters,"statuses":statuses})


@csrf_exempt
@login_required
def http_report_agreement_admin(request,agreement_id):
    agreement_status = AgreementStatus.objects.all()
    agreement = Agreement.objects.get(id=agreement_id)

    message = ""
    if request.method == "POST":

        if request.POST.get("person_name"):
            agreement.person_name=request.POST.get("person_name")
        else:
            agreement.person_name = ""    

        if request.POST.get("person_number"):
            agreement.person_number = request.POST.get("person_number")
        else:
            agreement.person_number = ""

        if request.POST.get("agreement_status"):
            status =AgreementStatus.objects.get(id=request.POST.get("agreement_status"))
            agreement.status = status
            if "Onaylandı" in status.name:
                try:
                    xx=KJ.objects.get(company=agreement)
                except:
                    kj = KJ()
                    kj.company=agreement
                    kj.save()

        if request.POST.get("record_place"):
            agreement.record_place = request.POST.get("record_place")
        else:
            agreement.record_place = "Belirtilmemiş"

        if request.POST.get("whatsapp"):
            agreement.whatsapp = request.POST.get("whatsapp")
        else:
            agreement.whatsapp = ""

        if request.POST.get("mail"):
            agreement.mail = request.POST.get("mail")
        else:
            agreement.mail = ""

        if request.POST.get("created_date"):
            agreement.created_date = request.POST.get("created_date")
            c_date=str(agreement.created_date).split("T")
        if request.POST.get("record_date"):
            agreement.record_date = request.POST.get("record_date")
            r_date=str(agreement.record_date).split("T")
            

        if request.POST.get("note"):
            company=Companies.objects.get(id=agreement.company_name.id)
            company.note = request.POST.get("note")
            company.save()

        try:
            agreement.save()
            Agreement_maker(c_date[0],r_date[0],r_date[1],request.POST.get("company_name"),agreement.record_place)
            message="kayd edildi"
        except Exception as e:
            print(e)
            message="Hata oluştu,bilgileri tam girdiğinizden emin olunuz"
        # return redirect("reports:agreement_admin",agreement_id=agreement_id)
    return render(request,"user/agreement_admin.html",{"agreement":agreement,"agreement_status":agreement_status,"message":message})


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

@csrf_exempt
@login_required
def http_azerbaycan(request):
    companies = Companies.objects.filter(city__slug=716)
    if request.POST.get('search'):
            s=request.POST.get('search')
            companies = companies.filter(name__contains=s)

    return render(request,"azerbaycan.html",{"companies":companies[0]})
