from django.urls import path
from . import views

app_name = 'customer'  

urlpatterns = [
        path('dashboard/', views.dashboard, name='dashboard'), 
        path('transactions/', views.transaction_list, name='transactions'), 
        path('cards/', views.card, name='cards'),  

        path('download_app/', views.download_app, name='download_app'), 
        path('settings/', views.settings, name='settings'), 
        # path('change_password/', views.change_password, name='change_password'), 
        path('apply_card/', views.apply_card, name='apply_card'), 
        path("blocked/", views.account_blocked, name="blocked"),

        path("change-transaction-pin/", views.change_transaction_pin,name="change_transaction_pin"),
        path('change-password/', views.change_password, name='change_password'),

        path("profile/photo/update/", views.update_passport_photo,name="update_passport_photo"),
]