from django.urls import path
from . import views

urlpatterns = [
    #path('', views.dolfinrest_list),
    #path('', views.index, name='index'),
    path('dfw_date_list/', views.dfw_date_list, name='dfw_date_list'),
    path('dfw_image_list/<str:obs_date>', views.dfw_image_list, name='dfw_image_list'),
    path('dfw_image_view/<str:pk>', views.dfw_image_view, name='dfw_image_view'),
    path('dfw_edit_finbox/<str:pk>', views.dfw_edit_finbox, name='dfw_edit_finbox'),
    path('dfw_edit_finbox/<str:pk>/<str:finid>', views.dfw_edit_finbox, name='dfw_edit_finbox'),
    path('dfw_fin_list/<str:obs_date>', views.dfw_fin_list, name='dfw_fin_list'),
    path('dfw_fin_image/<str:pk>', views.dfw_fin_image, name='dfw_fin_image'),

]