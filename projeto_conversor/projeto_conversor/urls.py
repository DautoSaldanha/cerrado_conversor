from django.contrib import admin
from django.urls import path
from aplicacao_conversor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('youtube/', views.youtube, name='youtube'),
]
