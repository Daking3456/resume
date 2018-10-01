from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
#from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
#from requests_oauthlib.compliance_fixes import linkedin
from social_django.models import UserSocialAuth


from accounts.models import Company, Address, UserProfile, Skills
from job.models import Applicant, Job
from accounts.forms import LoginForm, UserForm, BasicProfileForm, EducationForm, TrainingForm, SkillsForm, ExperienceForm 


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
        context_dict = {'form': form,}

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
                return render(request, 'home/login_modal.html',{'error': 'Invalid login credentials'})
        else:
            messages.error(request,'Invalid login credentials!')
            return render(request, 'home/login_modal.html',{'error': form.errors})

    else:
        form = LoginForm()
        return render(request,'login.html',{'forms':form})

# View function to handle logout
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

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

            """
               To display the number of applicants for a job listed by company sending in a list job 
               and all the applicants for the job 
            """
            job_and_applicants = []
            for job in job_posted:
                temp = [job, len(Applicant.objects.filter(job=job))]
                job_and_applicants.append(temp)
            

            context_dict = {'job_and_applicants': job_and_applicants}
        else:
            profile = UserProfile.objects.filter(user=request.user)

            if profile:
                job_applied = Applicant.objects.filter(applicant=user).order_by('-date_applied')
                print(profile)
                context_dict = {'job_applied': job_applied, 'profile':profile[0]  }

                return render(request,'profileview.html', context_dict)
            else:
                skills = Skills.objects.all()
                return render(request, 'profilebuilder.html', {'skills':skills} )

    return render(request,'accounts/profile.html', context_dict)


@login_required
def settings(request):
    user = request.user

    try:
        linkedin_login = user.social_auth.get(provider='linkedin')
    except UserSocialAuth.DoesNotExist:
        linkedin_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'home.html', {
        'linkedin_login': linkedin_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})



# for basic profile data
@login_required
def save_profile_basic(request):
    if request.method=="POST":
        form = BasicProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            print('1')
            profile.save()
    return HttpResponseRedirect('/')

@login_required
def save_profile_education(request):
    userprofile = request.user
    if request.method=="POST":
        form = EducationForm(request.POST)
        a = form.save()
        if form.is_valid():
            print(a)
            education = form.save()
            profile = UserProfile.objects.get(user=request.user)
            profile.education.add(education)
            profile.save()

    return HttpResponseRedirect('/')


@login_required
def save_profile_skills(request):
    if request.method=="POST":
        
        form = SkillsForm(request.POST)

        if form.is_valid():
            profile = UserProfile.objects.get(user=request.user)
            print("a")
            profile.skills = form.save()
            profile.save()


@login_required
def save_profile_training(request):
    if request.method=="POST":
        form = form(request.POST)

        if form.is_valid():
            training = form.save()
            profile = UserProfile.objects.get(user=request.user)
            profile.training.add(training)
            profile.save()


@login_required
def save_profile_experience(request):
    if request.method=="POST":
        form = ExperienceForm(request.POST)  
        print('s')

        if form.is_valid():
            print('a')
            experience = form.save()
            profile = UserProfile.objects.get(user=request.user)
            profile.work_experience.add(experience)
            profile.save()
    return HttpResponseRedirect("/")



def edit_profile_basic(request, id):
    if request.method=="POST":
        form = form(request.POST)

        if form.is_valid():
            form.save(commit=False)


@login_required
def edit_profile_education(request, id):
    if request.method=="POST":
        form = EducationForm(request.POST)

        if form.is_valid():
            print('a')
            education = form.save()
            profile = UserProfile.objects.get(user=request.user)
            profile.education.add(education)
            profile.save()


@login_required
def edit_profile_skills(request, id):
    if request.method=="POST":
        form = form(request.POST)
        if form.is_valid():
            education = form.save()


@login_required
def edit_profile_training(request, id):
    if request.method=="POST":
        form = form(request.POST)

        if form.is_valid():
            form.save()


@login_required
def edit_profile_experience(request, id):
    if request.method=="POST":
        form = form(request.POST)

        if form.is_valid():
            form.save()



def temp_add(request):
    form = EducationsForm()
    return render (request, 'abc.html',{'form':form})

def temp_view(request):
    return render (request, 'profileview.html')