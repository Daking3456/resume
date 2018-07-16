from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction

from accounts.models import Company, Address
from job.models import Applicant, Job
from accounts.forms import LoginForm, UserForm

# View function for registration of user
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            address = Address.objects.create()
            # Create user
            user = form.save(commit=False)
            user.address = address
            user.save()
            messages.info(request, "created successfully!")
        else:
            messages.error(request, 'Something is Wrong!')
        return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserForm()
        context_dict = {
            'form': form,
        }

    return render(request,'create_user.html', context_dict)

# View function for registration of company
@transaction.atomic
def create_company(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            address = Address.objects.create()

            # Create user
            user = form.save(commit=False)
            user.is_company = True
            user.address = address
            user.save()

            # Add the user to company group
            user_group = Group.objects.get(name='company')
            user_group.user_set.add(user)

            # Create company
            Company.objects.create(website = form.cleaned_data['website'],
                                   user = user)
            messages.info(request, "Company created successfully!")
        else:
            messages.error(request, 'Something is Wrong!')
        return HttpResponseRedirect('/accounts/login/')
    else:
        form = UserForm()
        context_dict = {
            'form': form,
        }

    return render(request,'create_company.html', context_dict)

# View function for login of user
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,
                                password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request,'Invalid login credentials!')
                return render(request, 'login.html')
        else:
            messages.error(request,'Invalid login credentials!')
            return render(request, 'login.html')

    else:
        form = LoginForm()
        return render(request,'login.html',{'forms':form})

# View function to handle logout
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')

def accounts_profile(request):
    user = request.user

    if request.method == "POST":
        address = Address.objects.create(
            city=request.POST.get("city"),
            country=request.POST.get("country"),
            zip_code=request.POST.get("zip_code"),
            address1=request.POST.get("address1"),
            address2=request.POST.get("address2"),
            )
        user.address = address
        user.save()
        return HttpResponseRedirect('/accounts/profile/')

    else:
        if user.is_company == True :
            company = Company.objects.get(user = user)
            job_posted = Job.objects.filter(company = company).order_by('-created_at')

            job_and_applicants = []
            for job in job_posted:
                temp = [job, len(Applicant.objects.filter(job=job))]
                job_and_applicants.append(temp)
            

            context_dict = {'job_and_applicants': job_and_applicants}
        else:
            job_applied = Applicant.objects.filter(applicant=user).order_by('-date_applied')
            context_dict = {'job_applied': job_applied }

    return render(request,'accounts/profile.html', context_dict)
