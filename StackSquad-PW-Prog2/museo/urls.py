from django.urls import path

from . import views

app_name = 'museo'

# Rotte principali dell'applicazione museo
urlpatterns = [
    path('', views.index, name='index'),
    path('autori/', views.autori_list, name='autori'),
    path('autori/<int:pk>/', views.autore_detail, name='autore_detail'),
    path('autori/api/', views.autore_api, name='autore_api'),
    path('opere/', views.opere_list, name='opere'),
    path('opere/<int:pk>/', views.opera_detail, name='opera_detail'),
    path('sale/', views.sale_list, name='sale'),
    path('sale/<int:pk>/', views.sala_detail, name='sala_detail'),
    path('temi/', views.temi_list, name='temi'),
    path('temi/<int:pk>/', views.tema_detail, name='tema_detail'),
]
