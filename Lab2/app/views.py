from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Event, Publication, EventPublication


def index(request):
    event_name = request.GET.get("event_name", "")
    events = Event.objects.filter(status=1)

    if event_name:
        events = events.filter(name__icontains=event_name)

    draft_publication = get_draft_publication()

    context = {
        "event_name": event_name,
        "events": events
    }

    if draft_publication:
        context["events_count"] = len(draft_publication.get_events())
        context["draft_publication"] = draft_publication

    return render(request, "home_page.html", context)


def add_event_to_draft_publication(request, event_id):
    event = Event.objects.get(pk=event_id)

    draft_publication = get_draft_publication()

    if draft_publication is None:
        draft_publication = Publication.objects.create()
        draft_publication.owner = get_current_user()
        draft_publication.date_created = timezone.now()
        draft_publication.save()

    if EventPublication.objects.filter(publication=draft_publication, event=event).exists():
        return redirect("/")

    item = EventPublication(
        publication=draft_publication,
        event=event
    )
    item.save()

    return redirect("/")


def event_details(request, event_id):
    context = {
        "event": Event.objects.get(id=event_id)
    }

    return render(request, "event_page.html", context)


def delete_publication(request, publication_id):
    if not Publication.objects.filter(pk=publication_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM event_publication WHERE publication_id = %s", [publication_id])
        cursor.execute("DELETE FROM publications WHERE id = %s", [publication_id])

    return redirect("/")


def publication(request, publication_id):
    if not Publication.objects.filter(pk=publication_id).exists():
        return redirect("/")

    context = {
        "publication": Publication.objects.get(id=publication_id),
    }

    return render(request, "publication_page.html", context)


def get_draft_publication():
    return Publication.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()