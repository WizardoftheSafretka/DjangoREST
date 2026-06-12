from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class User(AbstractBaseUser):
    class CustomUserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('Email обязателен')
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user

        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            return self.create_user(email, password, **extra_fields)

        def get_by_natural_key(self, username):
            return self.get(**{self.model.USERNAME_FIELD: username})

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    last_name = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Фалимия",
        help_text="Укажите фамилию",
    )


    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите фото",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Meta:
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"


def __str__(self):
    return self.email


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
        related_name='payments'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    paid_course = models.ForeignKey(
        'materials.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс',
        help_text='Укажите оплаченный курс',
        related_name='payments'
    )
    paid_lesson = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок',
        help_text='Укажите оплаченный урок',
        related_name='payments'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text='Укажите сумму оплаты',
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name='Способ оплаты',
        help_text='Выберите способ оплаты'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Платеж {self.amount} от {self.user.email}"

class Pay(models.Model):

    product = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Продукт",
        help_text="Укажите продукт",
    )

    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text='Укажите сумму оплаты',
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Id сессии',
        help_text='Укажите id сессии',
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='Ссылка для оплаты',
        help_text='Укажите ссылку для оплаты',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
    )

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-id']

    def __str__(self):
        return self.amount


