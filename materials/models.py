from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', help_text='Укажите название курса')
    review = models.ImageField(upload_to='materials/photos', blank=True, null=True, verbose_name='Первью',
                                help_text='Загрузите фото')
    description = models.TextField(blank=True, null=True, verbose_name='Описание', help_text='Укажите описание курса')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', help_text='Укажите название урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс',
                               help_text='Укажите название курса', related_name='lessons')
    description = models.TextField(blank=True, null=True, verbose_name='Описание', help_text='Укажите описание урока')
    review = models.ImageField(upload_to='materials/photos', blank=True, null=True, verbose_name='Первью',
                                help_text='Загрузите фото')
    url = models.TextField(blank=True, null=True, verbose_name='Ссылка на видео',
                           help_text='Укажите ссылку на видео с уроком')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f"{self.title} (курс: {self.course.title})"

