from django.urls import path
from . import views

urlpatterns = [
    path('',  views.index, name='index'),
    path('profile',  views.profile, name='profile'),
    path('account',  views.account, name='account'),
    path('logout',  views.logout, name='logout'),
    path('policy',  views.policy, name='policy'),
    path('savequestion',  views.savequestion, name='savequestion'),
    path('private/anonymous-message/<slug:username>',  views.PrivateMessage, name='private_message'),
    path('private/anonymous-message/<slug:username>/',  views.PrivateMessage, name='private_message'),
    path('business/anonymous-message/<slug:username>',  views.BusinessMessage, name='business_message'),
    path('business/anonymous-message/<slug:username>/',  views.BusinessMessage, name='business_message'),
    path('contact',  views.contact, name='contact'),
]