from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from selenium.webdriver.common.by import By
from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import *
import requests
import time
import csv


def create_account_tobb():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    check = requests.get("https://rekteam.com/check",headers=headers).text
    if check=='{"response": "ok"}':

        driver = webdriver.Firefox()
        driver.set_window_position(-10000,0)
        driver.minimize_window()

        #-----get user and number from database
        account=AccountReport.objects.get(user_type="account")
        account.number+=1
        account.save()
        #get user and number from database-----

        try:
            username=f"{account.user}{account.number}"
            #---------------------------------------------------------get an email from mohmal
            driver.get("https://www.mohmal.com/en")
            driver.find_element(By.ID, "rand").click()
            mail=driver.find_element(By.ID, "email").find_element(By.CLASS_NAME,"email").text
            time.sleep(7)
            #get an email from mohmal---------------------------------------------------------


            #-----------------------------------------------------------signup in tobb
            driver.get("https://sanayi.tobb.org.tr/firma_kayit3.php")

            business_feild = driver.find_element(By.NAME, "firma_unvani")
            name_feild = driver.find_element(By.NAME, "yetkili")
            post_feild = driver.find_element(By.NAME, "posta_adresi")
            tel02 = driver.find_element(By.NAME, "tel_2")
            tel03 = driver.find_element(By.NAME, "tel_3")
            faks02 = driver.find_element(By.NAME, "faks_2")
            faks03 = driver.find_element(By.NAME, "faks_3")
            mail_feild = driver.find_element(By.NAME, "email")
            status = driver.find_element(By.NAME, "statu")
            username_feild = driver.find_element(By.NAME, "kullanici")
            submit = driver.find_element(By.NAME, "gonder")

            business_feild.send_keys("AliParsa")
            name_feild.send_keys("AliParsa")
            post_feild.send_keys("AliParsa")
            tel02.send_keys("000")
            tel03.send_keys("0000")
            faks02.send_keys("000")
            faks03.send_keys("0000")
            mail_feild.send_keys(mail)
            username_feild.send_keys(username)
            status.click()
            submit.click()
            #signup in tobb-----------------------------------------------------------


            #-------------------------------------------------back to mohmal for get password
            time.sleep(7)
            driver.get("https://www.mohmal.com/en/refresh")
            time.sleep(7)
            driver.find_element(By.CLASS_NAME,"subject").click()
            time.sleep(7)
            inbox =BeautifulSoup(driver.page_source , "html.parser").find("iframe").attrs["src"]
            driver.get("https://www.mohmal.com"+inbox)
            password =BeautifulSoup(driver.page_source , "html.parser").find_all("td")[-1].text.strip()
            driver.close()
            #back to mohmal for get password-------------------------------------------------

            return {"user":username,"pass":password}
        except:
            driver.close()
            return False
    else:
        driver.close()
        return False

@login_required
def http_excel(request,city_slug):
    file = open("EXCEL.csv")
    csvreader = csv.reader(file)
    rows = []
    count=0
    for row in csvreader:
        company = Companies()
        user = request.user
        sector = row[0]
        name = row[1]
        short_name = row[1][0:11]
        phone = str(row[2])
        site = row[3]
        fount = Fount.objects.get(name="EXCEL")
        city = Cities.objects.get(slug=city_slug)
        last_status = Status.objects.get(name="Yeni")
        try:
            print(count)
            count+=1
            rows.append(Companies(user=user,sector=sector,name=name,short_name=short_name,phone=phone,site=site,fount=fount,city=city,last_status=last_status,))

            # company.status.add(Status.objects.get(name="Yeni"))
            # company.save()
        except:
            pass
    objs = Companies.objects.bulk_create(rows)
        # print(row)

    file.close()
    return HttpResponse(f"<h1 align='center' >Finish</h1><br><a href='/'>Home</a>")

@login_required
def http_crawler_tobb(request,city_slug):

    #-------------get last sector saved by this city slug
    city = Cities.objects.get(slug=city_slug)
    subsector_start = city.sub_sector_report
    sector_start = city.sector_report
    #get last sector saved by this city slug-------------


    #------------------------------------------------login
    check=True
    while check:

        #call def for create new account
        account=create_account_tobb()

        #login if account created
        if account:
            try:
                driver = webdriver.Firefox()
                driver.set_window_position(-10000,0)
                driver.minimize_window()

                driver.get("https://sanayi.tobb.org.tr/")

                username_feild = driver.find_element(By.NAME, "user")
                password_feild = driver.find_element(By.NAME, "pass")
                login = driver.find_element(By.NAME, "giris")

                username_feild.send_keys(account["user"])
                password_feild.send_keys(account["pass"])
                login.click()

                limit=0
                check=False
            except:
                driver.close()
                pass
    #login------------------------------------------------


    #---------------------------------------------------------------get sub sectors of saved in city
    try:
        time.sleep(3)
        driver.get("https://sanayi.tobb.org.tr/yeni_il08_0.php")
        city_button=driver.find_element(By.XPATH ,f"//select[@name='il']/option[@value={city_slug}]")
        city_button.click()
        driver.find_element(By.NAME, "arama").click()

        time.sleep(3)
        page=BeautifulSoup(driver.page_source , "html.parser")
        list_of_subsectors = page.find_all("center")[9:-2]
        list_of_subsectors = [f"https://sanayi.tobb.org.tr/yeni_il_urunlistesi02.php?il={city_slug}&sektor_kodu=" + x.find("a").text for x in list_of_subsectors ]
    except Exception as e:
        return HttpResponse(f"<h1 align='center' >error 2</h1> <br> <p align='center'>{e}</p><br><a href='/' align='center'>login</a>")
    #get sub sectors of saved in city---------------------------------------------------------------


    subsector_start_save=subsector_start
    sector_start_save=sector_start


    #---------------------------------------------------------------------------------------------------------get sectors of saved in city
    for subsector in list_of_subsectors[subsector_start_save:]:

        try:
            driver.get(subsector)
            page_0=BeautifulSoup(driver.page_source , "html.parser")
            list_of_sectors = page_0.find_all("td",attrs={"align":"left"})[1:]
            list_of_sectors = ["https://sanayi.tobb.org.tr/" + x.find("a").attrs["href"] for x in list_of_sectors ]
            sub_sector_name = page_0.find("td",attrs={"bgcolor":"#ffffff"}).find("center").find_all("h2")[1].text.strip()
            sub_sector_name = sub_sector_name[sub_sector_name.index("-")+1:].replace(";",".")
        except:
            continue

        for sector in list_of_sectors[sector_start_save:]:
            
            try:
                driver.get(sector)
                limit+=1
                page=BeautifulSoup(driver.page_source , "html.parser")
                table=page.find_all("table")[-2].find_all("tr")

                for row in table[1:]:
                    all_feild = row.find_all("td")
                    title = all_feild[1].text.strip()
                    address = all_feild[3].text.strip()
                    contact = all_feild[4].text.strip()
                    tel = contact[contact.index("T:")+2:contact.index("/")].replace("-","").replace(" ","").strip()
                    if "www" in contact:
                        site = contact[contact.index("www"):].strip()
                    elif "@" in contact:
                        try:
                            site = contact[contact.index("@")+1:contact.index("/",contact.index("@"))].strip()
                            site = "www."+site
                        except:
                            site = contact[contact.index("@")+1:].strip()
                            site = "www."+site
                    else:
                        site="bulunmadı"
                    population = all_feild[5].text.strip()
                    
                    company = Companies()
                    company.user = request.user
                    company.sector = sub_sector_name
                    company.name = title
                    company.short_name = title[0:11]
                    if tel[0]=="0":
                        tel=tel[1:]
                    company.phone = tel
                    company.site = site
                    company.address = address
                    company.personels_caount = population
                    company.note = ""
                    company.fount = Fount.objects.get(name="TOBB")
                    company.city = Cities.objects.get(slug=city_slug)
                    company.last_status = Status.objects.get(name="Yeni")
                    try:
                        if not tel[0:3] in ["444","850"]:
                            company.save()
                            company.status.add(Status.objects.get(name="Yeni"))
                            company.save()
                    except :
                        pass
                if limit>95:
                    driver.close()
                    check=True
                    #login------------------------------------------------
                    while check:
                        account=create_account_tobb()
                        if account:
                            try:
                                driver = webdriver.Firefox()
                                driver.set_window_position(-10000,0)
                                driver.minimize_window()
                                driver.get("https://sanayi.tobb.org.tr/")

                                username_feild = driver.find_element(By.NAME, "user")
                                password_feild = driver.find_element(By.NAME, "pass")
                                login = driver.find_element(By.NAME, "giris")

                                username_feild.send_keys(account["user"])
                                password_feild.send_keys(account["pass"])
                                login.click()

                                limit=0
                                check=False
                            except:
                                driver.close()
                                pass
                    #login------------------------------------------------
                city.sub_sector_report = subsector_start
                city.sector_report = sector_start
                city.save()
                
                sector_start+=1
            except:
                pass
                
        subsector_start+=1
        sector_start=0

    city.sub_sector_report = 0
    city.sector_report = 0
    city.save()
    #get sectors of saved in city---------------------------------------------------------------------------------------------------------

    driver.close()

@csrf_exempt
def http_crawler_google(request):
    message = ""
    cities=Cities.objects.all()

    if request.method == "POST":
        from serpapi import GoogleSearch
        try:
            api_key= AccountReport.objects.filter(user_type="api_key",owner=request.user,number__gte=10)[0]
            if not api_key.status:
                message = "Data arama limiti dolmuştur."
                return render(request,"google_map.html",{"message":message,"cities":cities})

            api_key_name = api_key.user
            api_key_limit = api_key.number
        except:
            message = "Data arama limiti dolmuştur."
            return render(request,"google_map.html",{"message":message,"cities":cities})
    
        city = Cities.objects.get(id=int(request.POST.get('city')))
        word = request.POST.get('sector')
        location = request.POST.get('location')

        try:
            GoogleSearchReport.objects.get(word=word,area=location)
            message = "aradigınız kriterlere ait zaten data var"
            return render(request,"google_map.html",{"message":message,"cities":cities})
        except:
            print("ok")

        params = {
        "engine": "google_maps",
        "q": f"{word} {location}",
        "type": "search",
        'hl': 'tr',
        "api_key": api_key_name,
        "start" : 0,
        }


        while True:
            if api_key_limit >9:

                try:
                    params_locations={
                        "engine": "google_maps",
                        "q": f"{city.name} {location}",
                        "type": "search",
                        'hl': 'tr',
                        "api_key": api_key_name,
                        }
                    search = GoogleSearch(params_locations)
                    api_key_limit -= 1
                    api_key.number = api_key_limit
                    api_key.save()
                    results = search.get_dict()["place_results"]["gps_coordinates"]
                    la=results['latitude']
                    lo=results['longitude']
                    params["ll"]=f"@{la},{lo},12z"
                except:
                    message = "girdiğiniz İl veya Bölge hatalı"
                    return render(request,"google_map.html",{"message":message,"cities":cities})

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
                        tel=x["phone"].replace("(","").replace(")","").split()
                        tel_code=tel[0]
                        tel_number="".join(tel[1:])
                        print(x)
                        company.user = request.user
                        company.name = x["title"]
                        company.sector = f"{city.name}-{location}-{word}"
                        company.full_name =""
                        company.short_name = x["title"][0:8]
                        company.phone = tel_number
                        company.phone_code = tel_code
                        try:
                            company.site = x["website"].replace("https://","").replace("http://","")
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
                            if not tel_number[0:3] in ["444","850"]:
                                company.save()
                                company.status.add(Status.objects.get(name="Yeni"))
                                company.save()
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                        pass
                
                params["start"]+=20

            else:
                try:
                    api_key= AccountReport.objects.filter(user_type="api_key",owner=request.user,number__gte=10)[0]
                    api_key_name = api_key.user
                    api_key_limit = api_key.number
                    if not api_key.status:
                        message = "Data arama limiti dolmuştur."
                        return render(request,"google_map.html",{"message":message,"cities":cities})
                except:
                    message = "Data arama limiti dolmuştur."
                    break
        g_s_r=GoogleSearchReport()
        g_s_r.city = city
        g_s_r.area = location
        g_s_r.word = word
        g_s_r.save()
        message = "datalar başarılıyla yüklendi"

    return render(request,"google_map.html",{"message":message,"cities":cities})

@login_required
def http_azexport(request,city_slug):
    url="https://azexport.az/index.php?route=product/seller/info&seller_id="
    num=1    
    while True:
        link=url+str(num)
        try:
            page=BeautifulSoup(requests.get(link).text,'html.parser')
            beu=page.find("table").find_all("tr")


            azexport = Azexport()

            azexport.user = request.user

            name=page.find("ul",attrs={"class":"breadcrumb"}).find_all("li")[-1].text
            azexport.name=name[:250]
            azexport.short_name = name[:11]
            azexport.link = link
            for x in beu:
                if "Legal Adress" in x.text:
                    address=x.find_all("td")[1].text.strip()
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
        num+=1
        if num>1955:break
    return HttpResponse(f"<h1 align='center' >Finish</h1><br><a href='/'>Home</a>")


def http_azerbaycan_yp(request,city_slug):
    site="https://www.azerbaijanyp.com/company/"
    for page_number in range(7,21000):
        try:
            page=site+str(page_number)


            # page="https://www.azerbaijanyp.com/company/15207/GINAR_SANATORIUM" #test
            # page="https://www.azerbaijanyp.com/company/20382/AccountingAz_LLC" #test


            source = BeautifulSoup(requests.get(page).text,'html.parser')
            info = source.find_all("div",attrs={"class":"info"})

            azexport = Azexport()
            name=""
            tel=""
            phone=""
            Person_name=""
            azexport.link=page

            if "Verified Business" in source.text:
                azexport.is_verified=True
            for x in info:
                try:
                    title=x.find("div").text
                except:
                    title=x.find("span").text

                if title=="Phone Number":
                    c=BeautifulSoup(str(x).replace("<br/>","\n"),'html.parser')
                    phone = c.text.replace("Phone Number","").replace("\n"," | ").strip(" | ")
                    azexport.phone = phone
                    # print(phone)

                elif title=="Mobile phone":
                    c=BeautifulSoup(str(x).replace("<br/>","\n"),'html.parser')
                    tel = c.text.replace("Mobile phone","").replace("\n"," | ").strip(" | ")
                    azexport.tel = tel
                    # print(tel)

                elif title=="Website":
                    website = x.text.replace("Website","").strip()
                    azexport.website=website
                elif title=="Company name":
                    name = x.text.replace("Company name","").strip()
                    azexport.name=name
                    azexport.short_name=name[:10]
                elif title=="Address":
                    address = x.text.replace("Address","").strip()
                    azexport.address=address


                elif title=="Contact Person":
                    full_name = x.text.replace("Contact Person","").strip()
                    Person_name += full_name+" - "
                    azexport.full_name += Person_name
                elif title=="Company manager":
                    full_name = x.text.replace("Company manager","").strip()
                    Person_name += full_name+" - "
                    azexport.full_name += Person_name
                elif title=="Employees":
                    try:
                        personels_caount = x.text.replace("Employees","").strip()
                        azexport.personels_caount = int(personels_caount.spilit("-")[1].strip())
                    except:
                        pass
                elif title=="Establishment year":
                    note = x.text.replace("Establishment year","").strip()
                    azexport.note = "firma açılış tarihi: "+note


            if (tel or phone) and name:
                try:
                    azexport.user = request.user
                    azexport.city = Cities.objects.get(slug=city_slug)
                    azexport.fount = Fount.objects.get(name="AZERBAYCANYP")
                    azexport.last_status = Status.objects.get(name="Yeni")
                    azexport.save()
                    print("save")
                except Exception as e:
                    print("not save: ",page)
        except Exception as e:
            print(e,"\nlink: ",page)
            pass
        # break

    return HttpResponse(f"<h1 align='center' >Finish</h1><br><a href='/'>Home</a>")
    