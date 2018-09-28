from django.urls import path

from . import views



urlpatterns = [
    path('', views.index_available, name='available'),
    path('addproperty', views.property_form, name='add'),
    path('addperson', views.person_form, name='addperson'),
    path('available', views.index_available, name='available'),
    path('unavailable', views.index_unavailable, name='unavailable'),
    path('getjson', views.get_json, name='getjson')
]