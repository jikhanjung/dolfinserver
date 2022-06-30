from django.urls import path
from . import views

urlpatterns = [
    #path('', views.dolfinrest_list),
    #path('', views.index, name='index'),
    path('dfw_date_list/', views.dfw_date_list, name='dfw_date_list'),
    path('dfw_image_list/<str:obs_date>', views.dfw_image_list, name='dfw_image_list'),
]