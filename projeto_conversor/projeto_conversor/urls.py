from django.contrib import admin
from django.urls import path
from aplicacao_conversor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('youtube/', views.youtube, name='youtube'),
    path('instagram/', views.instagram, name='instagram'),
    path('facebook/', views.facebook, name='facebook'),
    path('twitter/', views.twitter, name='twitter'),
]
