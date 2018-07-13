from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
	path('accounts/create/user/',views.create_user,name="createuser"),
    path('accounts/create/company/',views.create_company, name="createcompany"),
    path('accounts/profile/',views.accounts_profile,name='accounts_profile'),

    path('accounts/login/',views.login_page,name="login"),
    path('accounts/logout/',views.logout_page,name="logout"),
    
    # using default auth view for pasword change and reset
        
    path('accounts/change_password/', auth_views.PasswordChangeView.as_view()),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view()),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]