from django.contrib import admin

from users.models import Pay, Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "phone"]
    search_fields = ["email"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "amount",
        "payment_method",
        "payment_date",
        "paid_course",
        "paid_lesson",
    ]
    list_filter = ["payment_method", "payment_date"]
    search_fields = ["user__email"]


@admin.register(Pay)
class PayAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "amount", "session_id", "link"]
    search_fields = ["user__email", "product"]
