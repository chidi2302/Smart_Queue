from django.urls import path
#from .views import index, signup, login_view, logout_view
from . import views 
from .views import book_slot, view_available_queues,view_real_time_queuing_status

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('atm-queue/',views.atm_queue, name='atm_queue'),
    path('deposit-queue/', views.deposit_queue, name='deposit_queue'),
    path('features/', views.features, name='features'),
    path('general_inquiries/', views.general_inquiries, name='general_inquiries'),
    path('how-it-works/',views.how_it_works, name='how_it_works'),
    path('services/', views.services, name='services'),
    path('withdrawal-queue/', views.withdrawal_queue, name='withdrawal_queue'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book_slot/', views.book_slot, name='book_slot'),
    path('available_queues/', view_available_queues, name='view_available_queues'),
    #path('index/', index, name='index'),  # Protect this view
    path('real_time_queuing_status/', view_real_time_queuing_status, name='real_time_queuing_status'),  # New URL for queuing status

   ]