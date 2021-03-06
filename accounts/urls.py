from django.urls import path, include
from django.contrib.auth import views as auth_views

from accounts import views

urlpatterns = [
    path('accounts/signup/', views.create_user, name="createuser"),
    path('accounts/create/company/', views.create_company, name="createcompany"),
    path('accounts/profile/', views.accounts_profile, name='accounts_profile'),

    path('accounts/login/', views.login_page, name="login"),
    path('accounts/logout/', views.logout_page, name="logout"),
    
    # using default auth view for pasword change and reset
    path('accounts/change_password/', auth_views.PasswordChangeView.as_view()),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view()),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('settings/', views.settings, name='settings'),
    path('settings/password/', views.password, name='password'),
    path('oauth/', include('social_django.urls', namespace='social')),


    path('accounts/profile/basic/', views.save_profile_basic, name="profile_basic"),
    path('accounts/profile/experience/', views.save_profile_experience, name="profile_experience"),
    path('accounts/profile/education/', views.save_profile_education, name="profile_education"),
    path('accounts/profile/skills/', views.save_profile_skills, name="profile_skills"),
    path('accounts/profile/training/', views.save_profile_training, name="profile_training"),

    path('accounts/profile/experience/edit/<id>/', views.edit_profile_experience, name="edit_experience"),
    path('accounts/profile/skills/edit/<id>/', views.edit_profile_skills, name="edit_skills"),
    path('accounts/profile/training/edit/<id>/', views.edit_profile_training, name="edit_training"),
    path('accounts/profile/education/edit/<id>/', views.edit_profile_education, name="edit_education"),

    path('accounts/profile/experience/delete/<int:id>/', views.delete_profile_experience, name="delete_experience"),
    path('accounts/profile/skills/delete/<int:id>/', views.delete_profile_skills, name="delete_skills"),
    path('accounts/profile/training/delete/<int:id>/', views.delete_profile_training, name="delete_training"),
    path('accounts/profile/education/delete/<int:id>/', views.delete_profile_education, name="delete_education"),

    #  <temporary for static representation of design

    path('static_page/profile/add', views.temp_add),
    path('static_page/profile/view', views.temp_view),
    path('formset', views.formset),
]