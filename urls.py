from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),  # Home page
    path("signup/", views.signup_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
     path("enter-pin/<int:pk>/", views.enter_pin, name='enter_pin'),
    path("vault/<int:pk>/", views.vault_views, name='vault'),
    path("add/", views.add_password, name="add_password"),
    path("logout/", views.logout_user, name="logout"),
    path("update/<int:pk>/", views.update_password, name="update_password"),
    path("delete/<int:pk>/", views.delete_password, name="delete_password"),
    path('help/', views.help_page, name='help')
    
    

]
