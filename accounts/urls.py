from django.urls import path
from accounts import views

urlpatterns = [
	path('accounts/create/user/',views.create_user,name="createuser"),
    path('accounts/create/company/',views.create_company, name="createcompany"),
    path('accounts/login/',views.login_page,name="login"),
    path('accounts/logout/',views.logout_page,name="logout"),
    path('accounts/profile/',views.accounts_profile,name='accounts_profile'),
]