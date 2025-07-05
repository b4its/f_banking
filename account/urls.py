from django.urls import path
from .import views


urlpatterns = [
    
    path('authenticate/register/', views.register, name="register"),
    path('', views.customerlogin, name="customerlogin"),
    path('authenticate/logout/', views.logout_view, name="logout"),
    # path('lupa_password/', views.lupa_password, name="lupa_password"),
    # path('change_password/<token>', views.change_password, name="change_password"),

]