from django.shortcuts import render

resistors = [
    {
        "id": 1,
        "name": "Углеродный резистор",
        "description": "Углеродные резисторы являются одним из наиболее распространенных типов электроники. Они изготавливаются из твердого цилиндрического элемента резистора со встроенными проволочными выводами или металлическими торцевыми заглушками. Углеродные резисторы бывают разных физических размеров с пределами рассеиваемой мощности, обычно от 1 Вт до 1/8 Вт.",
        "resistance": "от нескольких Омов до нескольких мегомов",
        "power": "1/8 Вт, 1/4 Вт, 1/2 Вт, 1 Вт",
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Углеродный пленочный резистор",
        "description": "Углеродный пленочный резистор является электронным компонентом, который обеспечивает сопротивление электрическому току. Хотя существует много типов резисторов, изготовленных из множества различных материалов, углеродный пленочный резистор имеет тонкую пленку углерода, образованную вокруг цилиндра.",
        "resistance": "от 1 Ом до нескольких мегомов",
        "power": "от 1/8 Вт до 3 Вт",
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "Металло пленочный резистор",
        "description": "Металлопленочные резисторы имеют тонкий металлический слой в качестве резистивного элемента на непроводящем теле . Они являются одними из самых распространенных типов аксиальных резисторов.",
        "resistance": "от нескольких Ом до сотен мегомов",
        "power": "от 1/8 Вт до 2 Вт",
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "Металло оксидный резистор",
        "description": "Металлооксидные пленочные резисторы используют пленку, в которой оксиды металлов смешаны с резистивным элементом . Они используются в относительно промежуточных приложениях мощности около нескольких ватт и недороги.",
        "resistance": "от нескольких Ом до сотен мегомов",
        "power": "от 1/8 Вт до 10 Вт",
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "Проволочный резистор",
        "description": "Проволочные резисторы — это резисторы, в которых резистивным элементом является высокоомная проволока (изготавливается из высокоомных сплавов: константан, нихром, никелин).",
        "resistance": "от нескольких Ом до миллионов Ом",
        "power": "от 1 Вт до 100 Вт",
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "Разрывной резистор",
        "description": "Разрывной резистор, также известный как предохранительный резистор или антирезистор, — это специальный компонент, который используется в электрических и электронных устройствах для защиты цепей от перегрузок, коротких замыканий или других аномальных условий. ",
        "resistance": "от единиц Ом до сотен килоом",
        "power": "от 1/2 Вт до 10 Вт",
        "image": "http://localhost:9000/images/6.png"
    }
]

draft_calculation = {
    "id": 123,
    "status": "Черновик",
    "date_created": "12 сентября 2024г",
    "power": "2",
    "resistors": [
        {
            "id": 4,
            "name": "Металло оксидный резистор",
            "description": "Металлооксидные пленочные резисторы используют пленку, в которой оксиды металлов смешаны с резистивным элементом . Они используются в относительно промежуточных приложениях мощности около нескольких ватт и недороги.",
            "resistance": "от нескольких Ом до сотен мегомов",
            "power": "от 1/8 Вт до 10 Вт",
            "image": "http://localhost:9000/images/4.png",
            "count": 5
        },
        {
            "id": 5,
            "name": "Проволочный резистор",
            "description": "роволочные резисторы — это резисторы, в которых резистивным элементом является высокоомная проволока (изготавливается из высокоомных сплавов: константан, нихром, никелин).",
            "resistance": "от нескольких Ом до миллионов Ом",
            "power": "от 1 Вт до 100 Вт",
            "image": "http://localhost:9000/images/5.png",
            "count": 3
        },
        {
            "id": 6,
            "name": "Разрывной резистор",
            "description": "Разрывной резистор, также известный как предохранительный резистор или антирезистор, — это специальный компонент, который используется в электрических и электронных устройствах для защиты цепей от перегрузок, коротких замыканий или других аномальных условий. ",
            "resistance": "от единиц Ом до сотен килоом",
            "power": "от 1/2 Вт до 10 Вт",
            "image": "http://localhost:9000/images/6.png",
            "count": 8
        }
    ]
}


def getResistorById(resistor_id):
    for resistor in resistors:
        if resistor["id"] == resistor_id:
            return resistor


def searchResistors(resistor_name):
    res = []

    for resistor in resistors:
        if resistor_name.lower() in resistor["name"].lower():
            res.append(resistor)

    return res


def getDraftCalculation():
    return draft_calculation


def getCalculationById(calculation_id):
    return draft_calculation


def index(request):
    name = request.GET.get("name", "")
    resistors = searchResistors(name)
    draft_calculation = getDraftCalculation()

    context = {
        "resistors": resistors,
        "name": name,
        "resistors_count": len(draft_calculation["resistors"]),
        "draft_calculation": draft_calculation
    }

    return render(request, "home_page.html", context)


def resistor(request, resistor_id):
    context = {
        "id": resistor_id,
        "resistor": getResistorById(resistor_id),
    }

    return render(request, "resistor_page.html", context)


def calculation(request, calculation_id):
    context = {
        "calculation": getCalculationById(calculation_id),
    }

    return render(request, "calculation_page.html", context)

