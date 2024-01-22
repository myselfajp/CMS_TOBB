import requests
from bs4 import BeautifulSoup


def Collect(city):
    sectors = ["insaat-yapi","tekstil-giyim","hizmet","alisveris","gida","otomotiv","mobilya","elektrik-elektronik","turizm","tasimacilik"]
    for sector in sectors:
        pageNumber = 1
        while True:
            url = f"https://www.firmaturkiye.com/{city}/{sector}/{str(pageNumber)}"
            req = requests.get(url)

            if req.status_code == 200:
                req = req.text
            else:
                print("\n\n\nHata:  Bu sayf bulınmadı: ",url,"\n\n\n")
                return

            try:
                lst = BeautifulSoup(req,"html.parser").find_all("a",attrs={"itemprop":"url"})
                if not lst: return
            except:
                return

            urls = ["https://www.firmaturkiye.com"+x.attrs["href"] for x in lst]
            for url in urls:
                yield url,city
            pageNumber += 1

def getOne(url,city) -> dict:
    obj = {}
    obj["city"] = city
    req = requests.get(url)

    if req.status_code == 200:
        req = req.text
    else:
        return

    try:
        company = BeautifulSoup(req,"html.parser")

        address = company.find("div",attrs={"class":"ft-free-address"})
        if address:
            obj["address"] = address.text.replace("Adres:","").strip()

        title = company.find("div",attrs={"id":"companyTitle"})
        if title:
            obj["name"] = title.find("span").text.strip()
            obj["sector"] = title.find_all("h2")[-1].text.strip()

        site = company.find("span",attrs={"id":"website"})
        if site:
            site = site.find("a")
            if site:
                obj["site"] = "https://" + site.attrs["href"].replace("www.","")

        full_name = company.find("span",attrs={"id":"officalName"})

        if full_name:
            obj["full_name"] = full_name.text.strip()

        tels = company.find_all("span",attrs={"id":"website"})
        if len(tels) > 1:
            tel =  tels[1].find("a")
            if tel:
                tel = tel.attrs["href"].replace("tel:","").replace(" ","").strip()
                if tel[0] == "0": obj["tel"] = tel[1:]
                elif tel[0:3] == "+90": obj["tel"] = tel[3:]
                else: obj["tel"] = tel
                if len(obj["tel"]) < 10:
                    obj["tel"] = "000" + obj["tel"]
            if len(tels) > 2:
                obj["note"] = " , ".join([tel.find("a").attrs["href"].replace("tel:","").replace(" ","").strip() for tel in tels])
                print(obj["note"])
        else:
            tel = company.find("span",attrs={"id":"telephone"})
            if tel:
                tel = tel.find("a").attrs["href"].replace("tel:","").replace(" ","").strip()
                if tel[0] == "0": obj["tel"] = "000" + tel[1:]
                elif tel[0:3] == "+90": obj["tel"] = "000" + tel[3:]
                else: obj["tel"] = "000" + tel
            
        obj["tel"]
        obj["name"]
        return obj
    except Exception as e:
        print (e , url)
        return
