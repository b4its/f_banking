from django.urls import path

from . import views


urlpatterns = [
    path('tarik-tunai', views.tarikViews, name="tarikTunai"),
    path('transfer-tunai', views.transferViews, name="transferTunai"),
        path('transfer-tunai/store', views.transferStore, name="transfer_store"),
        path('transfer-tunai/stored/post', views.transferStored, name="transfer_stored"),
]