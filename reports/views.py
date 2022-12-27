from django.shortcuts import render
from crawler.models import Companies,Status
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def http_companies(request):
    if request.method == 'POST':
        company = Companies.objects.get(id=request.POST.get('company_id'))
        company.note=request.POST.get('note')
        new_status=request.POST.get('status_add')
        if new_status:
            new_status=Status.objects.get(id=int(new_status))
            company.status.add(new_status)
            company.last_status = new_status
        company.save()
    statuses = Status.objects.all()
    companies = Companies.objects.filter(user=request.user)
    return render(request,"companies.html",{'companies': companies,'statuses':statuses})


@login_required
def http_company(request,company_id):
    if request.method == 'POST':
        company = Companies.objects.get(id=company_id)
        company.note=request.POST.get('note')
        new_status=request.POST.get('status_add')
        if new_status:
            new_status=Status.objects.get(id=int(new_status))
            company.status.add(new_status)
            company.last_status = new_status
        company.save()
    company = Companies.objects.get(id=company_id)
    statuses = Status.objects.all()
    return render(request,"company.html",{'company': company,'statuses':statuses})