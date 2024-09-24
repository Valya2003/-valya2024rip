import random

from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import random_date, random_timedelta


def add_users():
    User.objects.create_user("user", "user@user.com", "1234")
    User.objects.create_superuser("root", "root@root.com", "1234")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234")

    print("Пользователи созданы")


def add_events():
    Event.objects.create(
        name="Крещение Руси",
        description="В 980 году внук князя Игоря - Владимир I провозгласил себя Великим Киевским князем. При нем все земли восточных славян объединились в составе Киевской Руси, завершилось формирование территориальной структуры русского государства. Отказ от язычества в пользу православия был одним из условий прекращения изоляции Руси от европейского христианского мира.",
        date=980,
        location="Киев, берег Днепра",
        image="images/1.png"
    )

    Event.objects.create(
        name="Татаро-монгольское иго",
        description="Включив в свою империю завоеванные народы Центральной Азии, Китая, Хорезма, Закавказья Чингиз-хан двинулся на русские княжества. В 1223 г. полководцы Чингиз-хана разбили русских князей на реке Калке. После битвы татары разорили города на окраине Черниговского княжества, но вскоре ушли на Волгу, в степи.",
        date=1223,
        image="images/2.png"
    )

    Event.objects.create(
        name="Смута на Руси",
        description="После смерти Ивана IV Грозного в 1584 г. трон перешел к его слабоумному сыну Федору (1584–1598). Новый царь не был способен к управлению государством. Он препоручил тяготы правления Россией своему опекуну Борису Годунову (1552–1605)",
        date=1584,
        location="Киев, берег Днепра",
        image="images/3.png"
    )

    Event.objects.create(
        name="Первая мировая война",
        description="Путь реформ был прерван новой войной. В июле 1914 г. Австро-Венгрия напала на Сербию, с которой у России был договор о взаимопомощи. 1 августа Германия объявила России войну. Союзницами России в этой войне стали Франция и Великобритания (военный блок «Антанта»). Противником Антанты выступал Тройственный союз (1882) в составе Германии, Австро-Венгрии и Италии.",
        date=1914,
        location="Европа",
        image="images/4.png"
    )

    Event.objects.create(
        name="Вторая мировая война",
        description="В конце 1930-х гг. мир неизбежно втягивался в новую войну. Германия стремилась отомстить за поражение в Первой мировой войне и постепенно начала диктовать свои условия. Покорив значительную часть Европы, 22 июня 1941 г. Германия напала на Советский Союз. В начале войны Красная Армия, потерпев поражение, вынуждена была отступать, неся тяжелые потери.",
        date=1930,
        location="Европа",
        image="images/5.png"
    )

    Event.objects.create(
        name="Распад СССР",
        description="18 августа 1991 года в СССР был создан ГКЧП (государственный комитет по чрезвычайному положению). Этот тогда еще государственный орган состоял из членов коммунистической партии Советского Союза, правительства и КГБ",
        date=1991,
        location="Республика Беларусь",
        image="images/6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_publications():
    users = User.objects.filter(is_superuser=False)
    moderators = User.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    events = Event.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        add_publication(status, events, users, moderators)

    add_publication(1, events, users, moderators)

    print("Заявки добавлены")


def add_publication(status, events, users, moderators):
    publication = Publication.objects.create()
    publication.status = status

    if publication.status in [3, 4]:
        publication.date_complete = random_date()
        publication.date_formation = publication.date_complete - random_timedelta()
        publication.date_created = publication.date_formation - random_timedelta()
    else:
        publication.date_formation = random_date()
        publication.date_created = publication.date_formation - random_timedelta()

    publication.owner = random.choice(users)
    publication.moderator = random.choice(moderators)

    publication.title = "Краткая история Руси"
    publication.description = "История России берет начало с возникновения славян, которые появились около 3-3,5 тысяч лет назад, выделившись из индоевропейского этноса. С середины I тысячелетия до н.э. они стали переселяться в Восточную Европу, заселив к VIII в. н.э. бассейн рек Днепр, Днестр, Западная Двина, Оку и верховья Волги."

    for event in random.sample(list(events), 3):
        item = EventPublication(
            publication=publication,
            event=event,
            value="Очень важный комментарий"
        )
        item.save()

    publication.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_events()
        add_publications()



















