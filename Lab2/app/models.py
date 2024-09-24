from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from app.utils import STATUS_CHOICES


class Event(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="images/default.png")
    description = models.TextField(verbose_name="Описание", blank=True)

    date = models.IntegerField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        db_table = "events"


class Publication(models.Model):
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    title = models.CharField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Публикация №" + str(self.pk)

    def get_events(self):
        return [
            setattr(item.event, "value", item.value) or item.event
            for item in EventPublication.objects.filter(publication=self)
        ]

    def get_status(self):
        return dict(STATUS_CHOICES).get(self.status)

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ('-date_formation', )
        db_table = "publications"


class EventPublication(models.Model):
    event = models.ForeignKey(Event, models.DO_NOTHING, blank=True, null=True)
    publication = models.ForeignKey(Publication, models.DO_NOTHING, blank=True, null=True)
    value = models.TextField(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "event_publication"
