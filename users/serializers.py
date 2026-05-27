from rest_framework.serializers import ModelSerializer
from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", "last_name", "phone", "avatar", "payments")


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "phone", "avatar")