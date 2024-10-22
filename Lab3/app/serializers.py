from rest_framework import serializers

from .models import *


class ResistorSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, resistor):
        return resistor.image.url.replace("minio", "localhost", 1)

    class Meta:
        model = Resistor
        fields = "__all__"


class ResistorItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_image(self, resistor):
        return resistor.image.url.replace("minio", "localhost", 1)

    def get_value(self, resistor):
        return self.context.get("value")

    class Meta:
        model = Resistor
        fields = ("id", "name", "image", "value")


class CalculationSerializer(serializers.ModelSerializer):
    resistors = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, calculation):
        return calculation.owner.username

    def get_moderator(self, calculation):
        if calculation.moderator:
            return calculation.moderator.username
            
    def get_resistors(self, calculation):
        items = ResistorCalculation.objects.filter(calculation=calculation)
        return [ResistorItemSerializer(item.resistor, context={"value": item.value}).data for item in items]

    class Meta:
        model = Calculation
        fields = '__all__'


class CalculationsSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, calculation):
        return calculation.owner.username

    def get_moderator(self, calculation):
        if calculation.moderator:
            return calculation.moderator.username

    class Meta:
        model = Calculation
        fields = "__all__"


class ResistorCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResistorCalculation
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
