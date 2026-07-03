import time
import concurrent.futures
import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# sanayi.org.tr (yeni TOBB Sanayi Bilgi Sistemi) - login gerektirmeyen genel API
# ---------------------------------------------------------------------------

SANAYI_API_BASE = "https://sanayi.org.tr/"
SANAYI_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
}

PLACEHOLDER_VALUES = {"", "yok", "bulunmamaktadır", "bulunmamaktır", "belirtilmemiş"}


def _clean(value):
    if value is None:
        return None
    value = str(value).strip()
    if value.lower().rstrip(".") in PLACEHOLDER_VALUES:
        return None
    return value


def _sanayi_call(endpoint, method_name, params, first=0, rows=20, auto=True, timeout=30):
    body = {
        "params": params,
        "lazyLoadingEvent": {
            "first": first,
            "rows": rows,
            "filter": None,
            "sortField": None,
            "sortOrder": 1,
            "auto": auto,
        },
        "methodName": method_name,
    }
    resp = requests.post(
        SANAYI_API_BASE + f"api/svt/{endpoint}",
        json=body,
        headers=SANAYI_HEADERS,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def get_iller():
    """İl (şehir) referans listesi. Giriş gerektirmez."""
    resp = requests.get(
        SANAYI_API_BASE + "api/ils",
        params={"size": 100},
        headers=SANAYI_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_sektor_kodus():
    """Üst düzey sektör kodu referans listesi. Giriş gerektirmez."""
    resp = requests.get(
        SANAYI_API_BASE + "apiv2/sektor-kodus",
        params={"size": 500},
        headers=SANAYI_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def search_firma_unvan(text, rows=500):
    """Firma unvanına göre arama (sanayi.org.tr 'Ünvandan Bulma' sayfasının kullandığı çağrı)."""
    return _sanayi_call("invokeEager", "firmaUnvanSorgula", {"firmaUnvani": text}, rows=rows, auto=True)


def firma_isyeri_detay(firma_basvuru_id):
    data = _sanayi_call(
        "invokeEager",
        "firmaIsyeriDetaySorgula",
        {"firmaBasvuruId": firma_basvuru_id},
        rows=5,
        auto=True,
    )
    return data[0] if data else {}


def firma_kapasite_detay(firma_basvuru_id):
    data = _sanayi_call(
        "invokeEager",
        "firmaKapasiteDetaySorgula",
        {"firmaBasvuruId": firma_basvuru_id},
        rows=5,
        auto=True,
    )
    return data[0] if data else {}


def get_company_detail(firma_basvuru_id):
    """Bir firma başvurusu için iletişim + kapasite detaylarını birleştirir."""
    isyeri = firma_isyeri_detay(firma_basvuru_id)
    kapasite = firma_kapasite_detay(firma_basvuru_id)
    return {
        "name": kapasite.get("KURUM_UNVANI"),
        "oda_adi": kapasite.get("ODA_ADI"),
        "ticaret_sicil_no": kapasite.get("TICARET_SICIL_NO"),
        "address": _clean(isyeri.get("ACIK_ADRES")),
        "tel": _clean(isyeri.get("TELEFON")),
        "faks": _clean(isyeri.get("FAKS")),
        "email": _clean(isyeri.get("E_POSTA")),
        "site": _clean(isyeri.get("WEB_ADRESI")),
        "personel_sayisi": isyeri.get("TOPLAM_PERSONEL_SAYISI"),
    }


def matches_city(detail, city_name):
    """
    Adres serbest metin olduğu için ortasında geçen bir sokak/cadde adı
    (ör. Bursa'daki "İstanbul Caddesi") yanlış eşleşmeye yol açabilir.
    Türkiye adres formatı ".../İlçe/İl" ile bittiğinden, il adını sadece
    adresin SON parçasında veya oda adının başında arıyoruz.
    """
    city_name_up = city_name.upper()
    address = (detail.get("address") or "").upper().strip()
    tail_segments = [seg.strip() for seg in address.split("/") if seg.strip()]
    if tail_segments and tail_segments[-1] == city_name_up:
        return True
    if address.endswith(city_name_up):
        return True
    oda_adi = (detail.get("oda_adi") or "").upper().strip()
    if oda_adi.startswith(city_name_up + " "):
        return True
    return False


def collect_sanayi_by_search(search_terms, delay=0.1, max_workers=6):
    """
    sanayi.org.tr'nin genel (login gerektirmeyen) firma unvanı arama uç noktasını
    her arama terimi için çağırır, bulunan her benzersiz firma için iletişim/kapasite
    detaylarını (paralel olarak, max_workers kadar aynı anda) çeker ve sözlük olarak
    yield eder.

    Not: Şehir/ürün koduna göre toplu listeleme uç noktası (api/svt/invoke,
    ureticiFirmalarByUrunKoduIl) şu anda TOBB'un kendi sitesinde de yanıt vermiyor
    (hem doğrudan istekte hem gerçek tarayıcıda "Bekleyiniz..." ekranında donuyor),
    bu yüzden güvenilir çalışan arama+detay uç noktaları kullanılıyor.
    """
    seen = set()
    for term in search_terms:
        try:
            results = search_firma_unvan(term)
        except requests.RequestException as e:
            print(f"[sanayi.org.tr] arama başarısız '{term}': {e}")
            continue

        candidates = []
        for row in results:
            firma_basvuru_id = row.get("ID")
            if not firma_basvuru_id or firma_basvuru_id in seen:
                continue
            seen.add(firma_basvuru_id)
            candidates.append(row)

        if not candidates:
            continue

        def fetch_one(row):
            firma_basvuru_id = row.get("ID")
            try:
                detail = get_company_detail(firma_basvuru_id)
            except requests.RequestException as e:
                print(f"[sanayi.org.tr] detay başarısız {firma_basvuru_id}: {e}")
                return None
            detail["firma_basvuru_id"] = firma_basvuru_id
            detail["kurum_id"] = row.get("KURUM_ID")
            if not detail.get("name"):
                detail["name"] = row.get("FIRMA_UNVANI")
            return detail

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            for detail in pool.map(fetch_one, candidates):
                if detail:
                    yield detail
                if delay:
                    time.sleep(delay)


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
