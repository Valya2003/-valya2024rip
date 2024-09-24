from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('events/<int:event_id>/', event_details, name="event_details"),
    path('events/<int:event_id>/add_to_publication/', add_event_to_draft_publication, name="add_event_to_draft_publication"),
    path('publications/<int:publication_id>/delete/', delete_publication, name="delete_publication"),
    path('publications/<int:publication_id>/', publication)
]
