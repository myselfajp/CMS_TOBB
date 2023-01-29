from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from .models import KJ
import json

# Create your views here.
@csrf_exempt
def http_kj_kurgu(request):
    kj_list=KJ.objects.all()

    if request.method == "POST":

        if request.POST.get("client"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.client=request.POST.get("client")
            object.save()

        elif request.POST.get("title"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.title=request.POST.get("title")
            object.save()

        elif request.POST.get("instagram"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.instagram=request.POST.get("instagram")
            object.save()
        
        elif request.POST.get("website"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.website=request.POST.get("website")
            object.save()

        elif request.POST.get("tel"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.tel=request.POST.get("tel")
            object.save()

        elif request.POST.get("sponser"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.sponser=request.POST.get("sponser")
            object.save()

        elif request.POST.get("ad_banner"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.ad_banner=request.POST.get("ad_banner")
            object.save()

        elif request.POST.get("play_time_as_minuate"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.play_time_as_minuate=request.POST.get("play_time_as_minuate")
            object.save()

        elif request.POST.get("agreement_price"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.agreement_price=request.POST.get("agreement_price")
            object.save()

        elif request.POST.get("Paid_price"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.Paid_price=request.POST.get("Paid_price")
            object.save()

        elif request.POST.get("note"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.note=request.POST.get("note")
            object.save()



        elif request.POST.get("is_played"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("is_played")=="true":
                object.is_played=True
            else:
                object.is_played=False
            object.save()

        elif request.POST.get("videos"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("videos")=="true":
                object.videos=True
            else:
                object.videos=False
            object.save()

        elif request.POST.get("kj_detials"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("kj_detials")=="true":
                object.kj_detials=True
            else:
                object.kj_detials=False
            object.save()

        elif request.POST.get("banner"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("banner")=="true":
                object.banner=True
            else:
                object.banner=False
            object.save()

        elif request.POST.get("presentation"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("presentation")=="true":
                object.presentation=True
            else:
                object.presentation=False
            object.save()

        elif request.POST.get("subtitle"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("subtitle")=="true":
                object.subtitle=True
            else:
                object.subtitle=False
            object.save()

        elif request.POST.get("youtube"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("youtube")=="true":
                object.youtube=True
            else:
                object.youtube=False
            object.save()

        elif request.POST.get("is_sent"):
            object = KJ.objects.get(id=request.POST.get("id"))
            if request.POST.get("is_sent")=="true":
                object.is_sent=True
            else:
                object.is_sent=False
            object.save()

        elif request.POST.get("play_date"):
            object = KJ.objects.get(id=request.POST.get("id"))
            object.play_date=request.POST.get("play_date")
            object.save()


        return HttpResponse(json.dumps({"status":"ok"}), content_type="application/json")
    return render(request,"kurgu/kj_kurgu.html",{"kj_list":kj_list})


def http_kj_muhasebe(request):
    kj_list=KJ.objects.all()
    return render(request,"kurgu/kj_muhasebe.html",{"kj_list":kj_list})
