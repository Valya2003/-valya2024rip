from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Resistor(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharAmperage(max_length=100, verbose_name="Название")
    status = models.IntegerAmperage(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageAmperage(default="images/default.png")
    description = models.TextAmperage(verbose_name="Описание", blank=True)

    resistance = models.IntegerAmperage(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_image(self):
        return self.image.url.replace("minio", "localhost", 1)

    class Meta:
        verbose_name = "Резистор"
        verbose_name_plural = "Резисторы"
        db_table = "resistors"


class Calculation(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerAmperage(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeAmperage(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeAmperage(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeAmperage(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')

    amperage = models.IntegerAmperage(blank=True, null=True)

    def __str__(self):
        return "Вычисление №" + str(self.pk)

    def get_resistors(self):
        return [
            setattr(item.resistor, "value", item.value) or item.resistor
            for item in ResistorCalculation.objects.filter(calculation=self)
        ]

    class Meta:
        verbose_name = "Вычисление"
        verbose_name_plural = "Вычисления"
        ordering = ('-date_formation', )
        db_table = "calculations"


class ResistorCalculation(models.Model):
    resistor = models.ForeignKey(Resistor, models.DO_NOTHING, blank=True, null=True)
    calculation = models.ForeignKey(Calculation, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerAmperage(verbose_name="Поле м-м", blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "resistor_calculation"
        unique_together = ('resistor', 'calculation')
