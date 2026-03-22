from django.urls import path
from . import views

app_name = 'entries'

urlpatterns = [    
    path('', views.entries_list, name="list"),    
    path('new-entry/', views.entry_new, name="new-entry"),    
    path('<slug:slug>', views.entry_page, name="page"),    
]