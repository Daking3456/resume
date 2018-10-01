from django import forms
from accounts.models import User, Address, Company, UserProfile, Education, Training, Skills, WorkExperience

# Form for registration of user
class UserForm(forms.ModelForm):

	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	website = forms.CharField(max_length=300, required=False)

	class Meta:
		model = User
		fields = ('username','email')

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
			return password2

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

# Form for Login
class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		fields = ('email','password')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'



class BasicProfileForm(forms.ModelForm):
 	class Meta:
 		model = UserProfile
 		exclude = ('skills', 'trainings', 'education', 'work_experience', 'user')

class EducationForm(forms.ModelForm):
 	class Meta:
 		model = Education
 		fields = '__all__'

class TrainingForm(forms.ModelForm):
 	class Meta:
 		model = Training
 		fields = '__all__'

class SkillsForm(forms.ModelForm):
 	class Meta:
 		models= Skills
 		fields = '__all__'


class ExperienceForm(forms.ModelForm):
 	class Meta:
 		model = WorkExperience
 		fields = '__all__'
