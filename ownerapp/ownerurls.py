from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'ownerapp'

urlpatterns = [
    path('ownerhome/', views.ownerhome, name='ownerhome'),
    path('add_property/', views.add_property, name='add_property'),
    path('add_property/', views.add_property, name='add_property'),
    path('listed-properties/', views.listed_properties, name='listed_properties'),
    path('property/<int:property_id>/inlist/', views.inlist_property, name='inlist_property'),
    path('property/<int:property_id>/applicants/', views.property_applicants, name='property_applicants'),
    path('property/<int:property_id>/applicants/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('property/<int:property_id>/applicants/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('sold-properties/', views.sold_properties, name='sold_properties'),
    path('pending-properties/', views.pending_properties, name='pending_properties'),
    path('profile/', views.owner_profile, name='owner_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.owner_logout, name='owner_logout'),
    path('inlisted_properties/', views.inlisted_properties, name='inlisted_properties'),
    path('relist-property/<int:property_id>/', views.relist_property, name='relist_property'),
    path('profile/edit/', views.edit_owner_profile, name='edit_owner_profile'),
    path('owner_complaint/', views.owner_complaint, name='owner_complaint'),



]