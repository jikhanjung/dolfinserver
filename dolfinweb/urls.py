from django.urls import path
from . import views

urlpatterns = [
    path('', views.dfw_date_list, name='dashboard'),
    path('dashboard', views.dfw_date_list, name='dashboard'),
    #path('', views.index, name='index'),
    path('dfw_date_list/', views.dfw_date_list, name='dfw_date_list'),
    path('dfw_image_list/<str:obs_date>', views.dfw_image_list, name='dfw_image_list'),
    path('dfw_image_view/<str:pk>', views.dfw_image_view, name='dfw_image_view'),
    path('dfw_edit_finbox/<str:pk>', views.dfw_edit_finbox, name='dfw_edit_finbox'),
    path('dfw_edit_finbox/<str:pk>/<str:finid>', views.dfw_edit_finbox, name='dfw_edit_finbox'),
    path('dfw_fin_list/<str:obs_date>', views.dfw_fin_list, name='dfw_fin_list'),
    path('dfw_fin_image/<str:img_id>/<str:fin_id_or_coords_str>', views.dfw_fin_image, name='dfw_fin_image'),

    # user
    path('dfw_user_register/', views.dfw_user_register, name='dfw_user_register'),
    path('dfw_user_info/', views.dfw_user_info, name='dfw_user_info'),
    path('dfw_user_edit/', views.dfw_user_edit, name='dfw_user_edit'),
    path('dfw_user_change_password/', views.dfw_user_change_password, name='dfw_user_change_password'),
    path('dfw_user_login/', views.dfw_user_login, name='dfw_user_login'),
    path('dfw_user_logout/', views.dfw_user_logout, name='dfw_user_logout'),

]