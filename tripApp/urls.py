from django.urls import path

from . import views
from. views import *

urlpatterns = [
    path('create/',DestCreateView.as_view(),name='create'),
    path('detail/<int:pk>/', DestDetails.as_view(), name='detail'),
    path('update/<int:pk>/', DestUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', DestDelete.as_view(), name='delete'),
    path('search/<str:place_name>/', DestSearchView.as_view(), name='search'),

    path('',views.base,name='base'),
    path('create-destination/', views.create_destination, name='create-destination'),
    path('update-detail/<int:id>/', views.update_detail, name='update-detail'),
    path('update-destination/<int:id>/', views.update_destination, name='update-destination'),
    path('delete-destination/<int:id>/', views.delete_destination, name='delete-destination'),
    path('fetch-destination/<int:id>/', views.fetch_destination, name='fetch-destination'),
    path('destination-delete/<int:id>/', views.delete_page, name='destination-delete'),

]
