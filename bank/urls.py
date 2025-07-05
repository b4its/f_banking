from django.urls import path

from . import views


urlpatterns = [
    path('transfer-tunai', views.transferViews, name="transferTunai"),
    path('tarik-tunai', views.tarikViews, name="tarikTunai"),
]