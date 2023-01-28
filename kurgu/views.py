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

        return HttpResponse(json.dumps({"status":"ok"}), content_type="application/json")
    return render(request,"kurgu/kj_kurgu.html",{"kj_list":kj_list})
    