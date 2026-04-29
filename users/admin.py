from django.contrib import admin
from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone']
    search_fields = ['email']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'payment_date', 'paid_course', 'paid_lesson']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['user__email']