from django.urls import path
from . import views  # ✅ import views properly

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('upload/scan/', views.upload_scanned_image, name='upload_scanned_image'),
    path('upload/image/', views.upload_uploaded_image, name='upload_uploaded_image'),
    path('images/unprocessed/', views.unprocessed_images, name='unprocessed_images'),
    path('images/classified/', views.classified_images, name='classified_images'),
    path('images/classified/detail/', views.classification_detail, name='classification_detail'),
    path('classification/update/', views.update_classification, name='update_classification'),
    path('user/update_recycling/', views.update_user_recycling_count, name='update_user_recycling_count'),
    path('user/profile/', views.user_profile, name='user_profile'),
]
