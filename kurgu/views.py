from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from .models import KJ,KJStatus,KJStatusAccounting
import json

# Create your views here.
@csrf_exempt
def http_kj_kurgu(request):
    kj_list=KJ.objects.all().order_by("play_date")
    statuses=KJStatus.objects.all()
    if request.method == "POST":
        message={"Status":"200"}
        if "client" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.client=request.POST.get("client")
            object.save()

        elif "title" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.title=request.POST.get("title")
            object.save()

        elif "instagram" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.instagram=request.POST.get("instagram")
            object.save()

        elif "website" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.website=request.POST.get("website")
            object.save()

        elif "tel" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.tel=request.POST.get("tel")
            object.save()

        elif "sponser" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.sponser=request.POST.get("sponser")
            object.save()

        elif "ad_banner" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.ad_banner=request.POST.get("ad_banner")
            object.save()

        elif "play_time_as_minuate" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.play_time_as_minuate=request.POST.get("play_time_as_minuate")
            object.save()

        elif "agreement_price" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.agreement_price=request.POST.get("agreement_price")
            object.save()

        elif "Paid_price" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.Paid_price=request.POST.get("Paid_price")
            object.save()

        elif "note" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.note=request.POST.get("note")
            object.save()

        elif "presentation" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.presentation=request.POST.get("presentation")
            object.save()




        elif "is_played" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("is_played")=="true":
                object.is_played=True
            else:
                object.is_played=False
            object.save()

        elif "videos" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("videos")=="true":
                object.videos=True
            else:
                object.videos=False
            object.save()

        elif "kj_detials" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("kj_detials")=="true":
                object.kj_detials=True
            else:
                object.kj_detials=False
            object.save()

        elif "banner" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("banner")=="true":
                object.banner=True
            else:
                object.banner=False
            object.save()

        elif "subtitle" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("subtitle")=="true":
                object.subtitle=True
            else:
                object.subtitle=False
            object.save()

        elif "youtube" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("youtube")=="true":
                object.youtube=True
            else:
                object.youtube=False
            object.save()

        elif "is_sent" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("is_sent")=="true":
                object.is_sent=True
            else:
                object.is_sent=False
            object.save()

        elif "montaj" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("montaj")=="true":
                object.montaj=True
            else:
                object.montaj=False
            object.save()

        elif "play_date" in request.POST:
            object = KJ.objects.get(id=request.POST.get("id"))
            object.play_date=request.POST.get("play_date")
            object.save()

        elif "status" in request.POST:
            status=KJStatus.objects.get(id=request.POST.get("status"))
            object = KJ.objects.get(id=request.POST.get("id"))
            object.status=status
            object.save()


        elif "status_accounting" in request.POST:
            status=KJStatusAccounting.objects.get(id=request.POST.get("status_accounting"))
            object = KJ.objects.get(id=request.POST.get("id"))
            object.status_accounting=status
            object.save()

        return HttpResponse(json.dumps(message), content_type="application/json")
    return render(request,"kurgu/kj_kurgu.html",{"kj_list":kj_list,"statuses":statuses})


def http_kj_muhasebe(request):
    kj_list=KJ.objects.all()
    status_accounting = KJStatusAccounting.objects.all()

    return render(request,"kurgu/kj_muhasebe.html",{"kj_list":kj_list,"status_accounts":status_accounting})
