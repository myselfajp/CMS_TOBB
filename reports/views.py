from django.shortcuts import render
from crawler.models import Companies,Status
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
@login_required
def http_companies(request):
    if request.method == 'POST':
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

    statuses = Status.objects.all()
    companies = Companies.objects.filter(user=request.user)
    return render(request,"companies.html",{'companies': companies,'statuses':statuses})

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
def http_test_send_mail(request):
    message=''
    if request.method == "POST":
        try:
            fullname=request.POST.get('fullname')
            email=request.POST.get('email')
            if fullname and email:
                subject, from_email = f'{fullname} dikkatine ... SEKTÖRÜN ÖNCÜLERİ LANSMAN TANITIMIDIR', 'info@sektorunonculeri.com'
                text_content = '''
                MERHABALAR EFENDİM
                SHOWTURK TE YAYINLANAN VE EŞ ZAMANDA 64 ÜLKEDE YAYIN İMKANI OLAN  SEKTÖREL HABER PROGRAMIMIZ VE AYNI ZAMANDA REKLAM İÇERİĞİ OLAN KONSEPTİYLE SİZ DEĞERLİ FİRMA SAHİPLERİNİ VE ALANINDAKİ ÇALIŞMALARINI TANITTIĞIMIZ SUNUCULUĞUNU ESRA BALAMİRİN ÜSTLENDİĞİ , ESRA BALAMİR İLE SEKTÖRÜN ÖNCÜLERİ PROGRAMIMIZDA SİZLEREDE YER VERMEK İSTERİZ. TARAFINIZA YÖNLENDİRİLMİŞ OLAN LANSMAN TANITIMIMIZI LÜTFEN İNCELEYİNİZ UYGUN GÖRDÜĞÜNÜZ TAKDİRDE BİRLİKTE BİR ÇALIŞMA YAPMAKTAN MEMNUNİYET DUYARIZ. SEKTÖRÜN ÖNCÜLERİ AİLESİ OLARAK İŞ HAYATINIZDA BAŞARILAR  DİLERİZ.
                '''
                msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
                msg.attach_file('LANSMAN - SEKTÖRÜN ÖNCÜLERİ.pdf')
                msg.send()
                message='Başırılıyla gönderildi'
            else:
                message = "Boşlukları doldurmanız gerekiyor"
        except:
            message = "Mesaj gönderilmedi"
    return render(request,"send_mail.html",{"message":message})
