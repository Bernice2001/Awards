from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'), 
    path('profile/', views.profile, name='profile'),  
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.signin, name='login'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)