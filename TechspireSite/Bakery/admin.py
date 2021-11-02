from django.contrib import admin
from django.contrib.auth.models import User, Group
from .reverse_inline import ReverseModelAdmin
from django.db.models import CharField
from . import forms
from . import models
from . import widgets


def format_phone(target_string):
    last4 = target_string[-4:]
    target_string = target_string[:-4]
    last3 = target_string[-3:]
    target_string = target_string[:-3]
    area = target_string[-3:]
    target_string = target_string[:-3]
    country = target_string
    return country + "-" + area + "-" + last3 + "-" + last4


class TwentyPageAdmin(admin.ModelAdmin):
    list_per_page = 20
    save_on_top = True
    change_form_template = "admin/hide_inline.html"


class ReverseTwentyAdmin(ReverseModelAdmin):
    list_per_page = 20
    save_on_top = True
    change_form_template = "admin/hide_inline.html"


@admin.register(models.StoreProduct)
class MenuAdmin(TwentyPageAdmin):
    list_display = ["product", "store"]


@admin.register(models.Reward)
class RewardAdmin(TwentyPageAdmin):
    model = models.Reward
    list_display = ["reward_name", "point_cost", "display_discount", "reward_status", "date_added", "tier"]
    list_filter = ["reward_status", "tier"]

    @admin.display(description='Discount', ordering="discount_amount")
    def display_discount(self, obj):
        return "$" + str(round(obj.discount_amount, 2))


@admin.register(models.Employee)
class EmployeeAdmin(ReverseTwentyAdmin):
    inline_type = "stacked"
    inline_reverse = ["location", ]
    widgets = {
        'phone_number': forms.PhoneForm
    }
    list_filter = ["employee_status"]
    list_display = ["first_name", "last_name", "email_address", "display_phone", "employee_status"]
    inlines = [forms.EmployeeCategoryForm, forms.EmployeeJobForm, forms.EmployeeSocialForm]

    change_form_template = 'admin/location_form.html'

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'Bakery/js/Location.js',
        )

    @admin.display(description='Phone Number', ordering="phone_number")
    def display_phone(self, obj):
        return format_phone(str(obj.phone_number))


@admin.register(models.Customer)
class CustomerAdmin(ReverseTwentyAdmin):
    widgets = {
        'phone_number': forms.PhoneForm
    }
    list_filter = ["customer_status", "tier"]
    search_fields = ["email_address", "phone_number"]
    list_display = ["first_name", "last_name", "email_address", "display_phone", "customer_status", "tier"]
    inlines = [forms.CustomerCategoryForm, forms.CustomerSocialForm]
    inline_type = "stacked"
    inline_reverse = ["location", ]
    raw_id_fields = ("create_employee",)
    readonly_fields = ["points_earned", "points_spent", "point_total", "tier"]

    change_form_template = 'admin/location_form.html'

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'Bakery/js/Location.js',
        )

    @admin.display(description='Phone Number', ordering="phone_number")
    def display_phone(self, obj):
        return format_phone(str(obj.phone_number))


@admin.register(models.Order)
class OrderAdmin(TwentyPageAdmin):
    list_display = ["customer", "store", "employee", "order_date", "display_original_total"]
    readonly_fields = ["original_total", "discount_amount", "eligible_for_points",
                       "points_consumed", "points_produced", "points_total", "final_total"]
    inlines = [forms.OrderLineForm, forms.RewardLineForm]
    change_form_template = 'admin/order_change_form.html'
    raw_id_fields = ("customer",)
    list_filter = ["store"]

    @admin.display(description='Total', ordering="original_total")
    def display_original_total(self, obj):
        return "$" + str(round(obj.original_total, 2))

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'Bakery/js/OrderChange.js',
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ["order_date", "customer", "store", "payment_type", "employee"] + self.readonly_fields
        return self.readonly_fields

    def get_inlines(self, request, obj):
        if obj:
            return [forms.OrderLineFormRead, forms.RewardLineFormRead]
        return self.inlines

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return True

    def save_model(self, request, obj, form, change):
        points_added = models.PointLog(employee=obj.employee, customer=obj.customer,
                                       reason_id=4, order=obj, points_amount=obj.points_produced)
        points_removed = models.PointLog(employee=obj.employee, customer=obj.customer,
                                         reason_id=5, order=obj, points_amount=obj.points_consumed)
        obj.save()
        points_added.save()
        points_removed.save()


@admin.register(models.Product)
class ProductAdmin(TwentyPageAdmin):
    list_filter = ["product_type", "product_status"]
    list_display = ["product_name", "product_type", "product_status", "display_product_price"]

    @admin.display(description='Price', ordering="product_price")
    def display_product_price(self, obj):
        return "$" + str(round(obj.product_price, 2))


@admin.register(models.StoreReward)
class StoreRewardAdmin(TwentyPageAdmin):
    list_filter = ["store"]
    list_display = ["reward", "store", "reward_assigned"]


@admin.register(models.Store)
class StoreAdmin(ReverseTwentyAdmin):
    inline_type = "stacked"
    inline_reverse = ["location", ]
    inlines = [forms.StoreSocialForm]
    list_display = ["store_name", "display_phone", "email_address", "website_address"]
    change_form_template = 'admin/location_form.html'

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            'Bakery/js/Location.js',
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super(StoreAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['website_address'].widget.attrs['style'] = 'width: 40em;'
        form.base_fields['email_address'].widget.attrs['style'] = 'width: 40em;'
        return form

    @admin.display(description='Phone Number', ordering="phone_number")
    def display_phone(self, obj):
        return format_phone(str(obj.phone_number))


@admin.register(models.PointLog)
class PointLogAdmin(TwentyPageAdmin):
    list_display = ["customer", "reason", "points_amount", "created_date"]
    list_filter = ["reason"]
    raw_id_fields = ["order", "employee", "customer"]


# Register all the models for bakery that don't have a custom admin model
def register_models():
    basic_admin_models = [models.ProductType, models.ProductStatus, models.CustomerStatus,
                          models.EmployeeStatus, models.RewardStatus, models.StoreStatus,
                          models.CustomerLabel, models.EmployeeLabel, models.EmployeeType,
                          models.Job, models.BanType, models.PointReason, models.SocialMediaType, models.PaymentType]
    for target_model in basic_admin_models:
        admin.site.register(target_model, )


register_models()
admin.site.unregister(User)
admin.site.unregister(Group)
