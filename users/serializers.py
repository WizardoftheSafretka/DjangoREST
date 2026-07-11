from rest_framework.serializers import ModelSerializer

from users.models import Pay, Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "last_name", "phone", "avatar", "payments")
        extra_kwargs = {"password": {"write_only": True}}


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "avatar")  # Убрали username


class PaySerializer(ModelSerializer):
    class Meta:
        model = Pay
        fields = "__all__"
