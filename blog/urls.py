from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.post_search, name='post_search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('training/', views.training, name='training'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post_detail'),
    path('<int:id>/share/', views.post_share, name='post_share'),
]
