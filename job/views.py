from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from job.forms import JobForm, JobModelForm
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
        form = JobModelForm(request.POST)
        if form.is_valid():
            company = Company.objects.get(user=request.user)
            job = form.save(commit=False)
            job.company = company
            form.save()
            messages.success(request,'Job Posted Successfully!')
        else:
            messages.error(request,'Something is Wrong, try again!')
        return render(request, 'job/postjob.html')
    else:
        form = JobForm()
        # To display different options for job field
        fields = Field.objects.all()
        context_dict = {'form':form, 'fields':fields}
        return render(request, 'job/postjob.html',context_dict)

def job_detail(request,slug):
    job = Job.objects.get(slug=slug)
    if request.method == 'POST' and request.FILES['resume']: 
        user = request.user
        user.username =request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        resume = request.FILES['resume']

        # if User applies again to update their credentials
        if Applicant.objects.filter(job=job, applicant=user):
            applicant = Applicant.objects.get(job=job, applicant=user)
            applicant.delete()
            Applicant.objects.create(job=job, applicant=user, resume=resume)
            messages.success(request,'Reapplied with updated credentials')
        
        # Appling for the first time
        else:
            Applicant.objects.create(job=job, applicant=user, resume=resume)
            messages.success(request,'Job applied Successfully!')
            
    related_jobs = Job.objects.filter(job_field= job.job_field).exclude(slug=slug)
    context_dict = {'job':job, 'related_jobs': related_jobs}
    return render(request,'job/job-detail.html',context_dict)

def apply_job(request, slug):
    job = Job.objects.get(slug=slug)
    user = request.user
    if Applicant.objects.filter(job=job, applicant=user):
        messages.info(request,'Already applied for the job!')
    else:
        Applicant.objects.create(job=job, applicant=user)
        messages.success(request,'Job applied Successfully!')
        
    return HttpResponseRedirect('/')

def edit_job(request, slug):
    if request.method == 'POST':
        job = Job.objects.get(slug=slug)
        form = JobModelForm(request.POST, instance=job)
        if form.is_valid():
            
            company = Company.objects.get(user=request.user)
            job = form.save()
            messages.success(request,'Job Posting Edited!')
        else:
            messages.error(request,'Something is Wrong, try again!')
        return HttpResponseRedirect('/')
    else:
        form = JobForm()
        job = Job.objects.get(slug=slug)
        # To display different options for job field
        fields = Field.objects.all()
        context_dict = { 'form':form,'fields':fields, 'job':job}
        return render(request, 'job/edit-job.html',context_dict)


def see_applicants(request, slug):
    job = Job.objects.get(slug = slug)
    applicants = Applicant.objects.filter(job=job)
    
    return render(request,'job/view-applicants.html',{'applicants':applicants} )
