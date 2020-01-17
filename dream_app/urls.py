from django.urls import path     
from . import views

urlpatterns = [
    path('', views.reg_login),
    path('registration', views.registration),
    path('login', views.login),
    path('logout', views.logout),
    path('dreams', views.dreams), 
    path('dreams/new', views.createadream),
    path('creating', views.creating),
    path('dreams/<int:dreamid>', views.viewadream),
    # path('trips/edit/<int:dreamid>', views.editadream),
    # path('editing/<int:dreamid>', views.editing),
    # path('deleteatrip/<int:dreamid>', views.deleteadream),
]