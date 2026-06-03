from django.shortcuts import render
from rest_framework import request

from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from materials.permissions import IsOwner
from users.models import Payment, User
from users.serializers import PaymentSerializer, PrivateUserSerializer, PublicUserSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = (AllowAny,)


class UserCreateAPIView(CreateAPIView):
    serializer_class = PrivateUserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer


class UserRetrieveApiView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        obj = self.get_object()

        if request.user == obj:
            return PrivateUserSerializer
        else:
            return PublicUserSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj)
        return Response(serializer.data)


class UserUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class UserDestroyApiView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = PrivateUserSerializer
    permission_classes = (IsAuthenticated, IsOwner)
