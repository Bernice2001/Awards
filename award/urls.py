from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name='MainPage'), 
    path('profile/<username>/', views.profile, name='profile'), 
    path('profile/<username>/edit', views.profile_edit, name='editProfile'),
    path('add_new_project/', views.post_project, name='addProject'),
    path('<uuid:post_id>', views.single_project, name='post'),
    path('<uuid:post_id>/like', views.like, name='likePost'),
    path('search/', views.search_results, name='search'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.signin, name='login'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)