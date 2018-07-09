from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from job.forms import JobForm
from job.models import Job, Field, Applicant
from accounts.models import Company, Address
            
# This function is for the authorization
def job_poster(user):
    return user.groups.filter(name='company').exists()

def load_home(request):
    jobs = Job.objects.filter(status=True)
    return render(request, 'home.html',{'jobs':jobs})

def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        print(request.POST.get("Field"))
        if form.is_valid():
            company = Company.objects.get(user=request.user)


            Job.objects.create(
                title = form.cleaned_data['title'],
                responsibilities = form.cleaned_data['responsibilities'],
                qualification = form.cleaned_data['qualification'],
                education = form.cleaned_data['education'],
                salary = form.cleaned_data['salary'],
                no_opening = form.cleaned_data['no_opening'],
                company = company,
                job_field = Field.objects.get(id=request.POST.get("Field")),
                deadline = form.cleaned_data['deadline']

            )
            messages.info(request,'Job Posted Successfully!')
        else:
            messages.error(request,'Something is Wrong, try again!')
        return render(request, 'job/postjob.html')
    else:
        form = JobForm()
        fields = Field.objects.all()
        context_dict = {'form':form, 'fields':fields}
        return render(request, 'job/postjob.html',context_dict)

def job_detail(request,slug):
    job = Job.objects.get(slug=slug)
    return render(request,'job/job-detail.html',{'job':job})

def apply_job(request, slug):

    job = Job.objects.get(slug=slug)
    user = request.user
    Applicant.objects.create(job=job, applicant=user)
    messages.info(request,'Job applied Successfully!')
    jobs = Job.objects.all()
    return render(request, 'home.html',{'jobs':jobs})


