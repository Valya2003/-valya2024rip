from django.contrib.auth import authenticate
from django.utils.dateparse import parse_datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_calculation(request):
    user = identity_user(request)

    if user is None:
        return None

    calculation = Calculation.objects.filter(owner=user).filter(status=1).first()

    return calculation


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'query',
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING
        )
    ]
)
@api_view(["GET"])
def search_resistors(request):
    resistor_name = request.GET.get("resistor_name", "")

    resistors = Resistor.objects.filter(status=1)

    if resistor_name:
        resistors = resistors.filter(name__icontains=resistor_name)

    serializer = ResistorSerializer(resistors, many=True)

    draft_calculation = get_draft_calculation(request)

    resp = {
        "resistors": serializer.data,
        "resistors_count": ResistorCalculation.objects.filter(calculation=draft_calculation).count() if draft_calculation else None,
        "draft_calculation_id": draft_calculation.pk if draft_calculation else None
    }

    return Response(resp)


@api_view(["GET"])
def get_resistor_by_id(request, resistor_id):
    if not Resistor.objects.filter(pk=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    resistor = Resistor.objects.get(pk=resistor_id)
    serializer = ResistorSerializer(resistor)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_resistor(request, resistor_id):
    if not Resistor.objects.filter(pk=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    resistor = Resistor.objects.get(pk=resistor_id)

    image = request.data.get("image")
    if image is not None:
        resistor.image = image
        resistor.save()

    serializer = ResistorSerializer(resistor, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_resistor(request):
    resistor = Resistor.objects.create()

    serializer = ResistorSerializer(resistor)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
def delete_resistor(request, resistor_id):
    if not Resistor.objects.filter(pk=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    resistor = Resistor.objects.get(pk=resistor_id)
    resistor.status = 2
    resistor.save()

    resistor = Resistor.objects.filter(status=1)
    serializer = ResistorSerializer(resistor, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_resistor_to_calculation(request, resistor_id):
    if not Resistor.objects.filter(pk=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    resistor = Resistor.objects.get(pk=resistor_id)

    draft_calculation = get_draft_calculation(request)

    if draft_calculation is None:
        draft_calculation = Calculation.objects.create()
        draft_calculation.date_created = timezone.now()
        draft_calculation.owner = identity_user(request)
        draft_calculation.save()

    if ResistorCalculation.objects.filter(calculation=draft_calculation, resistor=resistor).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = ResistorCalculation.objects.create()
    item.calculation = draft_calculation
    item.resistor = resistor
    item.save()

    serializer = CalculationSerializer(draft_calculation)
    return Response(serializer.data["resistors"])


@api_view(["POST"])
@permission_classes([IsModerator])
def update_resistor_image(request, resistor_id):
    if not Resistor.objects.filter(pk=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    resistor = Resistor.objects.get(pk=resistor_id)

    image = request.data.get("image")
    if image is not None:
        resistor.image = image
        resistor.save()

    serializer = ResistorSerializer(resistor)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_calculations(request):
    status_id = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    calculations = Calculation.objects.exclude(status__in=[1, 5])

    user = identity_user(request)
    if not user.is_staff:
        calculations = calculations.filter(owner=user)

    if status_id > 0:
        calculations = calculations.filter(status=status_id)

    if date_formation_start and parse_datetime(date_formation_start):
        calculations = calculations.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        calculations = calculations.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = CalculationsSerializer(calculations, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_calculation_by_id(request, calculation_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)
    serializer = CalculationSerializer(calculation)

    return Response(serializer.data)


@swagger_auto_schema(method='put', request_body=CalculationSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_calculation(request, calculation_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)
    serializer = CalculationSerializer(calculation, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, calculation_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)

    if calculation.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    calculation.status = 2
    calculation.date_formation = timezone.now()
    calculation.save()

    serializer = CalculationSerializer(calculation)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, calculation_id):
    if not Calculation.objects.filter(pk=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    calculation = Calculation.objects.get(pk=calculation_id)

    if calculation.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    calculation.status = request_status
    calculation.date_complete = timezone.now()
    calculation.moderator = identity_user(request)
    calculation.save()

    serializer = CalculationSerializer(calculation)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_calculation(request, calculation_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    calculation = Calculation.objects.get(pk=calculation_id)

    if calculation.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    calculation.status = 5
    calculation.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_resistor_from_calculation(request, calculation_id, resistor_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ResistorCalculation.objects.filter(calculation_id=calculation_id, resistor_id=resistor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ResistorCalculation.objects.get(calculation_id=calculation_id, resistor_id=resistor_id)
    item.delete()

    calculation = Calculation.objects.get(pk=calculation_id)

    serializer = CalculationSerializer(calculation)
    resistors = serializer.data["resistors"]

    if len(resistors) == 0:
        calculation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(resistors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_resistor_calculation(request, calculation_id, resistor_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ResistorCalculation.objects.filter(resistor_id=resistor_id, calculation_id=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ResistorCalculation.objects.get(resistor_id=resistor_id, calculation_id=calculation_id)

    serializer = ResistorCalculationSerializer(item)

    return Response(serializer.data)


@swagger_auto_schema(method='PUT', request_body=ResistorCalculationSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_resistor_in_calculation(request, calculation_id, resistor_id):
    user = identity_user(request)

    if not Calculation.objects.filter(pk=calculation_id, owner=user).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not ResistorCalculation.objects.filter(resistor_id=resistor_id, calculation_id=calculation_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = ResistorCalculation.objects.get(resistor_id=resistor_id, calculation_id=calculation_id)

    serializer = ResistorCalculationSerializer(item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # old_session = get_session(request)
    # if old_session:
    #     cache.delete(old_session)

    session = create_session(user.id)
    cache.set(session, settings.SESSION_LIFETIME)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    response.set_cookie('session', session, httponly=True)

    return response


@swagger_auto_schema(method='post', request_body=UserRegisterSerializer)
@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    session = create_session(user.id)
    cache.set(session, settings.SESSION_LIFETIME)

    serializer = UserSerializer(user)

    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    response.set_cookie('session', session, httponly=True)

    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    session = get_session(request)

    cache.delete(session)

    return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(method='PUT', request_body=UserSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = identity_user(request)

    if user.pk != user_id:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data, status=status.HTTP_200_OK)
