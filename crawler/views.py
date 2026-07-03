from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .models import *
from .utils import *
import threading
import requests
import time
import csv

# TOBB'un yeni sitesi (sanayi.org.tr) artik hesap/login gerektirmiyor; asagidaki
# fonksiyonlar crawler/utils.py icindeki genel (public) SVT API yardimcilarini kullanir.
# Firma unvani arama LIKE '%terim%' calistigi icin, TOBB'un resmi 53 sektor
# siniflandirmasini (apiv2/sektor-kodus) baz alarak firma isimlerinde gecmesi
# muhtemel anahtar kelimelerle genis bir tarama listesi olusturuldu.
SANAYI_ARAMA_TERIMLERI = [
    # Gıda / içecek / tütün
    "GIDA", "İÇECEK", "SÜT", "UN ", "YEM", "ŞEKERLEME", "ÇİKOLATA", "UNLU MAMUL",
    "ET ÜRÜNLERİ", "BALIK", "MEYVE", "SEBZE", "BİTKİSEL YAĞ", "MEŞRUBAT", "TÜTÜN",
    # Tekstil / giyim / deri
    "TEKSTİL", "GİYİM", "KONFEKSİYON", "ÖRME", "TRİKO", "DOKUMA", "İPLİK", "HALI",
    "DERİ", "AYAKKABI", "ÇANTA",
    # Ağaç / mobilya / kağıt / matbaa
    "MOBİLYA", "AHŞAP", "KERESTE", "KAĞIT", "KARTON", "AMBALAJ", "MATBAA", "BASKI",
    # Kimya / ilaç / plastik / kauçuk
    "KİMYA", "İLAÇ", "ECZA", "KOZMETİK", "BOYA", "PLASTİK", "KAUÇUK", "LASTİK",
    "TEMİZLİK ÜRÜNLERİ",
    # Mineral / metal
    "CAM", "SERAMİK", "ÇİMENTO", "MERMER", "METAL", "ÇELİK", "DEMİR", "ALÜMİNYUM",
    "DÖKÜM", "GALVANİZ", "KAPLAMA",
    # Makine / elektronik / elektrik / bilişim
    "MAKİNE", "MAKİNA", "ELEKTRONİK", "ELEKTRİK", "BİLGİSAYAR", "YAZILIM",
    "TELEKOMÜNİKASYON", "OPTİK",
    # Otomotiv / ulaşım / gemi / havacılık
    "OTOMOTİV", "OTO YEDEK PARÇA", "TAŞIT", "GEMİ", "TERSANE", "HAVACILIK",
    "SAVUNMA SANAYİ",
    # Enerji / su / çevre
    "ENERJİ", "SOLAR", "GÜNEŞ ENERJİSİ", "SU ARITMA", "GERİ DÖNÜŞÜM", "ATIK",
    # İnşaat / madencilik
    "İNŞAAT", "YAPI MALZEME", "MADEN", "HAFRİYAT",
    # Ticaret / hizmet / diğer
    "PAZARLAMA", "İTHALAT İHRACAT", "LOJİSTİK", "NAKLİYAT", "TURİZM",
    "DANIŞMANLIK", "MÜHENDİSLİK", "SAĞLIK", "TIBBİ CİHAZ", "OYUNCAK", "SPOR",
    "TAKI", "KUYUMCULUK", "ISI SOĞUTMA", "KLİMA", "ASANSÖR", "VİNÇ", "POMPA",
    "VALF", "RULMAN", "KALIP", "YAY", "CIVATA", "BAĞLANTI ELEMANLARI",
    "PRES", "TORNA", "KAYNAK", "İZOLASYON", "YALITIM", "PROFİL", "BORU",
]


@login_required
def http_excel(request, city_slug):
    # Specify the encoding when opening the file
    with open("EXCEL.csv", encoding="utf-8") as file:
        csvreader = csv.reader(file)
        rows = []
        count = 0
        for row in csvreader:
            try:
                company = Companies()
                user = request.user
                sector = row[0]
                name = row[1]
                short_name = row[1][0:5] + str(count)
                phone = str(row[2])
                site = row[3]
                address = row[4]
                fount = Fount.objects.get(name="EXCEL")
                city = Cities.objects.get(slug=city_slug)
                last_status = Status.objects.get(name="Yeni")

                print(count)
                count += 1
                rows.append(
                    Companies(
                        user=user,
                        sector=sector,
                        name=name,
                        short_name=short_name,
                        phone=phone,
                        site=site,
                        fount=fount,
                        city=city,
                        last_status=last_status,
                        address=address,
                    )
                )
            except Exception as e:
                print(f"Error processing row {count}: {e}")

        # Bulk create to improve performance
        Companies.objects.bulk_create(rows)

    return HttpResponse(f"<h1 align='center'>Finish</h1><br><a href='/'>Home</a>")


@login_required
def http_crawler_tobb(request, city_slug):
    """
    sanayi.org.tr (yeni TOBB Sanayi Bilgi Sistemi) artik hesap acmadan/login
    olmadan herkese acik. Firma unvani arama uc noktasini bir dizi anahtar
    kelimeyle tarar, bulunan her firma icin iletisim+kapasite detayini ceker
    ve adres/oda bilgisine gore secilen sehre ait olanlari kaydeder.
    """
    city = Cities.objects.get(slug=city_slug)

    def run():
        saved = 0
        seen_total = 0
        for detail in collect_sanayi_by_search(SANAYI_ARAMA_TERIMLERI):
            seen_total += 1
            if not matches_city(detail, city.name):
                continue

            name = (detail.get("name") or "").strip()
            if not name:
                continue

            company = Companies()
            company.user = request.user
            company.sector = "Sanayi Veri Tabanı"
            company.name = name
            company.short_name = name[0:11]
            company.phone = (detail.get("tel") or "")[:20]
            company.site = detail.get("site")
            company.address = detail.get("address")
            company.personels_caount = detail.get("personel_sayisi")
            company.note = f"Faks: {detail.get('faks')}" if detail.get("faks") else ""
            company.fount = Fount.objects.get(name="TOBB")
            company.city = city
            company.last_status = Status.objects.get(name="Yeni")

            try:
                company.save()
                company.status.add(Status.objects.get(name="Yeni"))
                company.save()
                saved += 1
            except Exception as e:
                print(e)

        print(f"[sanayi.org.tr] {city.name}: {seen_total} firma tarandı, {saved} kayıt eklendi.")

    threading.Thread(target=run, daemon=True).start()
    return HttpResponse(
        "<h1 align='center'>Robot işe başladı, bu sayfayı kapatabilirsiniz!</h1><br><a href='/'>Home</a>"
    )




@csrf_exempt
def http_crawler_google(request):
    message = ""
    cities = Cities.objects.all()

    if request.method == "POST":
        from serpapi import GoogleSearch

        try:
            api_key = AccountReport.objects.filter(user_type="api_key", number__gte=10)[
                0
            ]
            if not api_key.status:
                print("1")
                message = "Data arama limiti dolmuştur."
                return render(
                    request, "google_map.html", {"message": message, "cities": cities}
                )

            api_key_name = api_key.user
            api_key_limit = api_key.number
        except:
            print("2")
            message = "Data arama limiti dolmuştur."
            return render(
                request, "google_map.html", {"message": message, "cities": cities}
            )

        city = Cities.objects.get(id=int(request.POST.get("city")))
        word = request.POST.get("sector")
        location = request.POST.get("location")

        try:
            GoogleSearchReport.objects.get(word=word, area=location)
            message = "aradigınız kriterlere ait zaten data var"
            return render(
                request, "google_map.html", {"message": message, "cities": cities}
            )
        except:
            print("ok")

        params = {
            "engine": "google_maps",
            "q": f"{word} {location}",
            "type": "search",
            "hl": "tr",
            "api_key": api_key_name,
            "start": 0,
        }

        while True:
            if api_key_limit > 9:

                try:
                    params_locations = {
                        "engine": "google_maps",
                        "q": f"{city.name} {location}",
                        "type": "search",
                        "hl": "tr",
                        "api_key": api_key_name,
                    }
                    search = GoogleSearch(params_locations)
                    api_key_limit -= 1
                    api_key.number = api_key_limit
                    api_key.save()
                    results = search.get_dict()["place_results"]["gps_coordinates"]
                    la = results["latitude"]
                    lo = results["longitude"]
                    params["ll"] = f"@{la},{lo},12z"
                except:
                    message = "girdiğiniz İl veya Bölge hatalı"
                    return render(
                        request,
                        "google_map.html",
                        {"message": message, "cities": cities},
                    )

                search = GoogleSearch(params)
                results = search.get_dict()
                api_key_limit -= 1
                api_key.number = api_key_limit
                api_key.save()

                try:
                    local_results = results["local_results"]
                except:
                    print("error 1")
                    break

                for x in local_results:
                    try:
                        company = Companies()
                        tel = x["phone"].replace("(", "").replace(")", "").split()
                        tel_code = tel[0]
                        tel_number = "".join(tel[1:])
                        print(x)
                        company.user = User.objects.get(username="admin")
                        company.name = x["title"]
                        company.sector = f"{city.name}-{location}-{word}"
                        company.full_name = ""
                        company.short_name = x["title"][0:8]
                        company.phone = tel_number
                        company.phone_code = tel_code
                        try:
                            company.site = (
                                x["website"]
                                .replace("https://", "")
                                .replace("http://", "")
                            )
                        except:
                            company.site = "bulunmadı"
                        try:
                            company.address = x["address"]
                        except:
                            company.address = ""
                        company.note = ""
                        company.fount = Fount.objects.get(name="GoogleMaps")
                        company.city = city
                        company.last_status = Status.objects.get(name="Yeni")
                        try:
                            if not tel_number[0:3] in ["444", "850"]:
                                company.save()
                                company.status.add(Status.objects.get(name="Yeni"))
                                company.save()
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                        pass

                params["start"] += 20

            else:
                try:
                    api_key = AccountReport.objects.filter(
                        user_type="api_key", number__gte=10
                    )[0]
                    api_key_name = api_key.user
                    api_key_limit = api_key.number
                    if not api_key.status:
                        print("3")
                        message = "Data arama limiti dolmuştur."
                        return render(
                            request,
                            "google_map.html",
                            {"message": message, "cities": cities},
                        )
                except:
                    print("4")

                    message = "Data arama limiti dolmuştur."
                    break
        g_s_r = GoogleSearchReport()
        g_s_r.city = city
        g_s_r.area = location
        g_s_r.word = word
        g_s_r.save()
        message = "datalar başarılıyla yüklendi"

    return render(request, "google_map.html", {"message": message, "cities": cities})


@login_required
def http_azexport(request, city_slug):
    url = "https://azexport.az/index.php?route=product/seller/info&seller_id="
    num = 1
    while True:
        link = url + str(num)
        try:
            page = BeautifulSoup(requests.get(link).text, "html.parser")
            beu = page.find("table").find_all("tr")

            azexport = Azexport()

            azexport.user = request.user

            name = (
                page.find("ul", attrs={"class": "breadcrumb"}).find_all("li")[-1].text
            )
            azexport.name = name[:250]
            azexport.short_name = name[:11]
            azexport.link = link
            for x in beu:
                if "Legal Adress" in x.text:
                    address = x.find_all("td")[1].text.strip()
                    azexport.address = address
                elif "Activity Group" in x.text:
                    sector = x.find_all("td")[1].text.strip()
                    azexport.sector = sector
                elif "Phone" in x.text:
                    phone = x.find_all("td")[1].text.strip()
                    azexport.phone = phone
                elif "Mobile" in x.text:
                    Mobile = x.find_all("td")[1].text.strip()
                    azexport.tel = Mobile
                elif "E-mail" in x.text:
                    mail = x.find_all("td")[1].text.strip()
                    azexport.mail = mail
                elif "Website" in x.text:
                    website = x.find_all("td")[1].text.strip()
                    azexport.website = website
                elif "Facebook" in x.text:
                    Facebook = x.find_all("td")[1].text.strip()
                    azexport.social_media = Facebook
                elif "Twitter" in x.text:
                    Twitter = x.find_all("td")[1].text.strip()
                    azexport.social_media = Twitter
            try:
                azexport.city = Cities.objects.get(slug=city_slug)
                azexport.fount = Fount.objects.get(name="AZEXPORT")
                azexport.last_status = Status.objects.get(name="Yeni")
                azexport.save()
            except:
                pass
        except:
            print(link)
            pass
        num += 1
        if num > 1955:
            break
    return HttpResponse(f"<h1 align='center' >Finish</h1><br><a href='/'>Home</a>")


def http_azerbaycan_yp(request, city_slug):
    site = "https://www.azerbaijanyp.com/company/"
    for page_number in range(7, 21000):
        try:
            page = site + str(page_number)

            # page="https://www.azerbaijanyp.com/company/15207/GINAR_SANATORIUM" #test
            # page="https://www.azerbaijanyp.com/company/20382/AccountingAz_LLC" #test

            source = BeautifulSoup(requests.get(page).text, "html.parser")
            info = source.find_all("div", attrs={"class": "info"})

            azexport = Azexport()
            name = ""
            tel = ""
            phone = ""
            Person_name = ""
            azexport.link = page

            if "Verified Business" in source.text:
                azexport.is_verified = True
            for x in info:
                try:
                    title = x.find("div").text
                except:
                    title = x.find("span").text

                if title == "Phone Number":
                    c = BeautifulSoup(str(x).replace("<br/>", "\n"), "html.parser")
                    phone = (
                        c.text.replace("Phone Number", "")
                        .replace("\n", " | ")
                        .strip(" | ")
                    )
                    azexport.phone = phone
                    # print(phone)

                elif title == "Mobile phone":
                    c = BeautifulSoup(str(x).replace("<br/>", "\n"), "html.parser")
                    tel = (
                        c.text.replace("Mobile phone", "")
                        .replace("\n", " | ")
                        .strip(" | ")
                    )
                    azexport.tel = tel
                    # print(tel)

                elif title == "Website":
                    website = x.text.replace("Website", "").strip()
                    azexport.website = website
                elif title == "Company name":
                    name = x.text.replace("Company name", "").strip()
                    azexport.name = name
                    azexport.short_name = name[:10]
                elif title == "Address":
                    address = x.text.replace("Address", "").strip()
                    azexport.address = address

                elif title == "Contact Person":
                    full_name = x.text.replace("Contact Person", "").strip()
                    Person_name += full_name + " - "
                    azexport.full_name = Person_name
                elif title == "Company manager":
                    full_name = x.text.replace("Company manager", "").strip()
                    Person_name += full_name + " - "
                    azexport.full_name = Person_name
                elif title == "Employees":
                    try:
                        personels_caount = x.text.replace("Employees", "").strip()
                        azexport.personels_caount = int(
                            personels_caount.spilit("-")[1].strip()
                        )
                    except:
                        pass
                elif title == "Establishment year":
                    note = x.text.replace("Establishment year", "").strip()
                    azexport.note = "firma açılış tarihi: " + note

            if (tel or phone) and name:
                try:
                    azexport.user = request.user
                    azexport.city = Cities.objects.get(slug=city_slug)
                    azexport.fount = Fount.objects.get(name="AZERBAYCANYP")
                    azexport.last_status = Status.objects.get(name="Yeni")
                    azexport.save()
                    print("save")
                except Exception as e:
                    print("not save: ", page)
        except Exception as e:
            print(e, "\nlink: ", page)
            pass
        # break

    return HttpResponse(f"<h1 align='center' >Finish</h1><br><a href='/'>Home</a>")


def firmaTurkiye(request, city_slug):
    print("robot started")
    for url, city in Collect(city_slug):
        obj = getOne(url, city)
        if obj:

            company = Companies()
            company.user = request.user
            if x := obj.get("address"):
                company.address = x
            if x := obj.get("sector"):
                company.sector = x
            if x := obj.get("name"):
                company.name = x
                company.short_name = x[0:11]
            if x := obj.get("tel"):
                company.phone = x
            if x := obj.get("site"):
                company.site = x
            if x := obj.get("note"):
                company.note = x

            company.fount = Fount.objects.get(name="firmaturkiye.com")
            company.city = Cities.objects.get(name=city_slug)
            company.last_status = Status.objects.get(name="Yeni")
            try:
                company.save()
                company.status.add(Status.objects.get(name="Yeni"))
                company.save()
                print("added.")

            except Exception as e:
                print(e)
                pass


class firmaTurkiyeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.request = None
        self.city = None

    def run(self):
        firmaTurkiye(self.request, self.city)


def Http_firmaTurkiye(request, city_slug):
    if request.user.is_superuser:
        text_thread = firmaTurkiyeThread()
        text_thread.request = request
        text_thread.city = city_slug

        text_thread.start()
        return HttpResponse("<h1>Robot işe başladı, bu sayfayı kapatabilirsiniz!</h1>")
    else:
        return redirect("/")
