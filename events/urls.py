from django.urls import path
from events.views import (
    organizer_dashboard,
    event_list,event_update,event_create,event_delete,home,
    category_create,participant_create
)

urlpatterns=[
    path('home/',home,name="home"),
    path('organizer_dashboard/',organizer_dashboard,name="organizer_dashboard"),
    path('event_list/',event_list,name="event_list"),
    path('event_create/', event_create, name='event_create'),
    path('event_update/<int:id>/', event_update, name='event_update'),
    path('event_delete/<int:id>/', event_delete, name='event_delete'),
    
    path('category_create/', category_create, name='category_create'),
    path('participant_create/<int:event_id>', participant_create, name='participant_create'),
]