from django.shortcuts import render
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from materials.models import Course, Lesson, Subscribe
from materials.paginations import CustomPagination
from materials.permissions import IsModer, IsOwner, IsOwnerOrModer
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    SubscribeSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            # Все могут создавать курсы
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # Владелец или модератор могут просматривать/редактировать
            permission_classes = [IsAuthenticated, IsOwnerOrModer]
        elif self.action == "destroy":
            # Только модератор может удалять
            permission_classes = [IsAuthenticated, IsModer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModer]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer]


class SubscribeViewSet(ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscribe.objects.filter(user=request.user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
            return Response({"message": message}, status=status.HTTP_204_NO_CONTENT)
        else:
            Subscribe.objects.create(
                course=course_item, user=request.user, is_subscribe=True
            )
            message = "подписка добавлена"
            return Response({"message": message}, status=status.HTTP_201_CREATED)
