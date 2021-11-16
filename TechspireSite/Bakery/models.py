from django.db import models
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from .Owners import Owners
from django.utils import timezone
import os
from django.db import connection, ProgrammingError, DataError


def past_validator(value):
    if value > timezone.now().date():
        raise forms.ValidationError("The date must be in the past!")
    return value


class MoneyField(models.DecimalField):
    def __init__(self):
        super().__init__(max_digits=19, decimal_places=4, default=0)

    def __str__(self):
        return "$" + super.__str__(self)
    widget = forms.Textarea


class DescriptiveModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = "Blank Description"
    pk_desc = "Standard Auto-Increment PK"
    owner = Owners.TableOwner
    load_order = -1

    class Meta:
        abstract = True
        managed = False


# Used as an abstract parent for status codes
class StatusCode(DescriptiveModel):
    description = "Used to soft delete rows with a reason name and desc"
    status_name = models.CharField(max_length=40)
    status_desc = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    load_order = 1
    category = "Other"

    def __str__(self):
        return self.status_name

    class Meta:
        abstract = True
        managed = False


# Used as an abstract parent for labels
class LabelCode(DescriptiveModel):
    description = "Allows for multiple named categories"
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200, blank=True, null=True)
    load_order = 1
    category = "Other"

    def __str__(self):
        return self.type_name

    class Meta:
        abstract = True
        managed = False


class CustomerLabel(DescriptiveModel):
    description = 'Categorizes customers based on the opinion of the store owner.'
    owner = Owners.Rebecca
    category_name = models.CharField(max_length=40)
    category_desc = models.CharField(max_length=200, blank=True, null=True)
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "CustomerCategory"
        verbose_name_plural = "Customer Category"
        managed = False

    def __str__(self):
        return self.category_name


class EmployeeLabel(DescriptiveModel):
    description = 'Categorizes employee based on the opinion of the store owner.'
    owner = Owners.Kyle
    category_name = models.CharField(max_length=40)
    category_desc = models.CharField(max_length=200, blank=True, null=True)
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "EmployeeCategory"
        verbose_name_plural = "Employee Category"
        managed = False

    def __str__(self):
        return self.category_name


class EmployeeStatus(StatusCode):
    description = 'Defines whether an employee is currently active or inactive'
    owner = Owners.Alanna

    class Meta:
        db_table = "EmployeeStatus"
        verbose_name_plural = "Employee Status"
        managed = False


class CustomerStatus(StatusCode):
    description = 'Describes the current relationship between the ' \
                  'customer and the business (are they an ' \
                  'Active customer? are they an inactive customer?)'
    owner = Owners.Umair

    class Meta:
        db_table = "CustomerStatus"
        verbose_name_plural = "Customer Status"
        managed = False


class ProductStatus(StatusCode):
    description = 'Refers to whether a product is available or not. ' \
                  'Not that it is unavailable but also if it is not offered anymore'
    owner = Owners.Srijana

    class Meta:
        db_table = "ProductStatus"
        verbose_name_plural = "Product Status"
        managed = False


class StoreStatus(StatusCode):
    description = 'Soft delete of store.'
    owner = Owners.Alanna

    class Meta:
        db_table = "StoreStatus"
        verbose_name_plural = "Store Status"
        managed = False


class RewardStatus(StatusCode):
    description = 'Defines whether a particular reward is active/inactive. Core attributes: active, inactive'
    owner = Owners.Alanna

    class Meta:
        db_table = "RewardStatus"
        verbose_name_plural = "Reward Status"
        managed = False


class BanType(DescriptiveModel):
    description = "Describes why a specific product that is banned"
    owner = Owners.Alanna
    load_order = 1
    ban_name = models.CharField(max_length=40)
    ban_desc = models.CharField(max_length=200, blank=True, null=True)
    category = "Other"

    class Meta:
        db_table = "BanType"
        verbose_name_plural = "Ban Type"
        managed = False

    def __str__(self):
        return self.ban_name


class PointReason(DescriptiveModel):
    description = "Describes why points were added or removed"
    owner = Owners.Jade
    reason_name = models.CharField(max_length=40)
    reason_desc = models.CharField(max_length=200, blank=True, null=True)
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "PointReasonType"
        verbose_name_plural = "Point Log Type"
        managed = False

    def __str__(self):
        return self.reason_name


class Country(DescriptiveModel):
    description = 'The nation that a particular entity (a store, a customer) is located in.'
    country_name = models.CharField(max_length=60)
    owner = Owners.Rebecca
    load_order = 1
    category = "Other"

    def __str__(self):
        return self.country_name

    class Meta:
        db_table = "Country"
        verbose_name_plural = "Country"
        managed = False


class StateProvince(DescriptiveModel):
    description = 'The state/province that a particular entity (a store, a customer) is located in.'
    state_name = models.CharField(max_length=60)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, default=233)
    owner = Owners.Rebecca
    load_order = 2
    category = "Other"

    def __str__(self):
        return self.state_name

    class Meta:
        db_table = "StateProvince"
        verbose_name_plural = "State/Province"
        managed = False


class Location(DescriptiveModel):
    description = "Represents a complete address for a location"
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=35, default="Houston")
    address = models.CharField(max_length=100, default="3242 StreetName")
    state = models.ForeignKey(StateProvince, on_delete=models.RESTRICT, default=1407)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT, default=233)
    owner = Owners.BrettM
    load_order = 3

    class Meta:
        db_table = "Location"
        verbose_name_plural = "Address"
        verbose_name = "Address"
        managed = False

    def __str__(self):
        return "{} {} {} {}".format(self.address, self.zip_code, self.state, self.country)


class Tier(DescriptiveModel):
    description = 'Categories that loyalty customers are a part of based on ' \
                  'number of points accumulated over time. Tiers such as bronze, silver, and gold tier for example.'
    owner = Owners.Umair
    tier_name = models.CharField(max_length=40)
    tier_desc = models.CharField(max_length=200, blank=True, null=True)
    min_points = models.IntegerField(default=0)
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "Tier"
        verbose_name_plural = "Tier"
        managed = False

    def __str__(self):
        return self.tier_name

    def save(self, *args, **kwargs):
        super(Tier, self).save(*args, **kwargs)
        module_dir = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(module_dir), "TechspireSite", "SQL",
                            "Brett M", "UpdateCustomerTier.sql")
        sql = open(path).read()
        with connection.cursor() as cursor:
            cursor.execute(sql)


# Used as an abstract parent for people
class Person(DescriptiveModel):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email_address = models.EmailField(max_length=254)
    phone_number = PhoneNumberField(max_length=15, help_text="xxx-xxx-xxxx", default="+19043335252")
    birthdate = models.DateField(validators=[past_validator])
    begin_date = models.DateField(auto_now_add=True, help_text="YYYY-MM-DD")
    location = models.ForeignKey(Location, on_delete=models.RESTRICT, verbose_name="Address")
    comments = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        managed = False

    def __str__(self):
        return self.first_name + " " + self.last_name


class EmployeeType(LabelCode):
    description = 'The working type of an employee such as part-time or full-time. '
    owner = Owners.Kyle

    class Meta:
        db_table = "EmployeeType"
        verbose_name_plural = "Employee Type"
        managed = False


class Employee(Person):
    description = 'Person that works at the store and ' \
                  'deals with either the store products or maintenance of said store.'
    end_date = models.DateField(blank=True, null=True)
    employee_status = models.ForeignKey(EmployeeStatus, on_delete=models.RESTRICT)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.RESTRICT)
    owner = Owners.BrettM
    load_order = 4
    category = "Core"

    class Meta:
        db_table = "Employee"
        verbose_name_plural = "Employee"
        managed = False


class Customer(Person):
    description = 'Someone who potentially purchases an item/service ' \
                  'from our client and whose general information has been collected by our loyalty system database.'
    create_employee = models.ForeignKey(Employee, on_delete=models.RESTRICT, blank=True, null=True)
    customer_status = models.ForeignKey(CustomerStatus, on_delete=models.RESTRICT)
    points_earned = models.IntegerField(default=0)
    points_spent = models.IntegerField(default=0)
    point_total = models.IntegerField(default=0)
    tier = models.ForeignKey(Tier, on_delete=models.RESTRICT, default=1)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, blank=True, null=True)
    owner = Owners.Julia
    load_order = 5
    category = "Cashier"

    class Meta:
        db_table = "Customer"
        verbose_name_plural = "Loyalty Customer"
        managed = False


class Job(DescriptiveModel):
    description = 'The type of role that an employee of a store holds such as cashier, manager, etc.'
    job_name = models.CharField(max_length=40)
    job_desc = models.CharField(max_length=200, blank=True, null=True)
    owner = Owners.BrettM
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "Job"
        verbose_name_plural = "Job"
        managed = False

    def __str__(self):
        return self.job_name


class AssocEmployeeLabel(DescriptiveModel):
    description = 'Allows an employee to have multiple categories'
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    employee_category = models.ForeignKey(EmployeeLabel, on_delete=models.RESTRICT)
    owner = Owners.Kyle
    load_order = 5

    class Meta:
        db_table = "EmployeeEmployeeCategory"
        verbose_name = "Employee Category"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['employee', 'employee_category'], name='unique_emp_cat')]

    def __str__(self):
        return str(self.employee) + " " + str(self.employee_category)


class AssocCustomerLabel(DescriptiveModel):
    description = 'Allows a customer to have multiple categories'
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    customer_category = models.ForeignKey(CustomerLabel, on_delete=models.RESTRICT)
    owner = Owners.Rebecca
    load_order = 6

    class Meta:
        db_table = "CustomerCustomerCategory"
        verbose_name = "Customer Category"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['customer', 'customer_category'], name='unique_cust_cat')]

    def __str__(self):
        return str(self.customer) + " " + str(self.customer_category)


class PaymentType(LabelCode):
    description = 'The way a customer pays for a service or product such as cash, credit, Google Pay, etc.'
    owner = Owners.Umair

    class Meta:
        db_table = "PaymentType"
        verbose_name_plural = "Payment Type"
        managed = False


class Store(DescriptiveModel):
    description = 'A physical location where customers go to complete transactions.'
    store_name = models.CharField(max_length=40)
    phone_number = PhoneNumberField(max_length=15, blank=True, null=True, help_text="xxx-xxx-xxxx", default="+19043335252")
    email_address = models.EmailField(max_length=254, blank=True, null=True)
    website_address = models.CharField(max_length=300, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.RESTRICT)
    store_status = models.ForeignKey(StoreStatus, on_delete=models.RESTRICT)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    employees = models.ManyToManyField(Employee, through="EmployeeJob")
    owner = Owners.Srijana
    load_order = 4
    category = "Core"

    class Meta:
        db_table = "Store"
        verbose_name_plural = "Store"
        managed = False

    def __str__(self):
        return self.store_name


class EmployeeJob(DescriptiveModel):
    description = 'Allows an employee to have multiple jobs at the same or different stores.'
    assign_date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    job = models.ForeignKey(Job, on_delete=models.RESTRICT)
    owner = Owners.BrettM
    load_order = 5

    class Meta:
        db_table = "EmployeeJob"
        verbose_name = "Employee Job"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['store', 'job', 'employee'], name='unique_store_job')]

    def __str__(self):
        return str(self.employee) + " " + str(self.store) + " " + str(self.job)


class Order(DescriptiveModel):
    description = 'The customer’s finalized transaction of products purchased. ' \
                  'This order generates customer loyalty points based on the monetary total of the transaction.'
    order_date = models.DateField(auto_now_add=True)
    original_total = MoneyField()
    final_total = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    discount_amount = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    eligible_for_points = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    points_consumed = models.IntegerField(default=0)
    points_produced = models.IntegerField(default=0)
    points_total = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    owner = Owners.Torrey
    load_order = 6
    category = "Cashier"

    class Meta:
        db_table = "Order"
        verbose_name_plural = "Order/Transaction"
        managed = False

    def __str__(self):
        return str(self.store) + "-" + str(self.customer) + "-" + str(self.order_date)



class ProductType(DescriptiveModel):
    description = 'Identifying certain product types that are eligible ' \
                  'to be purchased with points, versus products ' \
                  'that are not eligible to earn points on; used to distinguish exclusions. '
    product_type_name = models.CharField(max_length=40)
    product_type_desc = models.CharField(max_length=200, blank=True, null=True)
    owner = Owners.Srijana
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "ProductType"
        verbose_name_plural = "Product Type"
        managed = False

    def __str__(self):
        return self.product_type_name


class Product(DescriptiveModel):
    description = 'An item purchased by the customer in a transaction.'
    product_name = models.CharField(max_length=80)
    product_desc = models.CharField(max_length=200, blank=True, null=True)
    product_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    product_status = models.ForeignKey(ProductStatus, on_delete=models.RESTRICT)
    ban_reason = models.ForeignKey(BanType, on_delete=models.SET_NULL, blank=True, null=True)
    owner = Owners.Srijana
    load_order = 2
    category = "Core"

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Product"
        managed = False

    def __str__(self):
        return self.product_name


class OrderLine(DescriptiveModel):
    description = 'Represents information located on a ' \
                  'singular line found on a receipt/invoice ' \
                  'produced after a completed transaction ' \
                  'that describes the customer’s transaction ' \
                  'and product details (quantity, product type, ' \
                  'total price for that order line).'
    quantity = models.IntegerField(default=0)
    ind_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    total_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    points_eligible = models.BooleanField(default=True)
    owner = Owners.Julia
    load_order = 7

    class Meta:
        db_table = "OrderLine"
        verbose_name = "Order Line"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['order', 'product'], name='unique_order_product')]

    def save(self, *args, **kwargs):
        target_product = Product.objects.get(pk=self.product.id)
        self.ind_price = target_product.product_price
        self.total_price = self.ind_price * self.quantity
        self.points_eligible = target_product.ban_reason is None
        super(OrderLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order) + " " + str(self.product)


class Reward(DescriptiveModel):
    description = 'All benefits that are offered by the business ' \
                  'for being an active loyalty customer that can be ' \
                  'claimed by converting some of their earned points. ' \
                  '“Rewards” can be coupons ($5 off) or birthday reward ' \
                  '(does not need point conversion, it’s just a redemption code for a freebie)'
    reward_name = models.CharField(max_length=80)
    reward_desc = models.CharField(max_length=200, blank=True, null=True)
    reward_status = models.ForeignKey(RewardStatus, on_delete=models.RESTRICT)
    point_cost = models.IntegerField(default=0)
    reset_period = models.IntegerField(default=0, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    free_product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)
    date_disabled = models.DateField(blank=True, null=True)
    owner = Owners.Umair
    load_order = 3
    category = "Core"

    class Meta:
        db_table = "Reward"
        verbose_name_plural = "Reward"
        managed = False

    def __str__(self):
        return self.reward_name


class SocialMediaType(DescriptiveModel):
    description = 'The different types of social media that exist for use such as Instagram, Snapchat, etc.'
    social_media_name = models.CharField(max_length=40)
    social_media_desc = models.CharField(max_length=200, blank=True, null=True)
    owner = Owners.Torrey
    load_order = 1
    category = "Other"

    class Meta:
        db_table = "SocialMediaType"
        verbose_name_plural = "Social Media Type"
        managed = False

    def __str__(self):
        return self.social_media_name


class StoreSocialMedia(DescriptiveModel):
    description = 'Social media of the store.'
    social_media_code = models.CharField(max_length=60)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    social_media_type = models.ForeignKey(SocialMediaType, on_delete=models.RESTRICT)
    date_added = models.DateField(auto_now_add=True)
    owner = Owners.Saja
    load_order = 5

    class Meta:
        db_table = "StoreSocialMedia"
        verbose_name_plural = "Store Social Media"
        managed = False

    def __str__(self):
        return str(self.social_media_type) + " " + str(self.store)


class EmployeeSocialMedia(DescriptiveModel):
    description = 'Employee social media.'
    social_media_code = models.CharField(max_length=60)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    social_media_type = models.ForeignKey(SocialMediaType, on_delete=models.RESTRICT)
    date_added = models.DateField(auto_now_add=True)
    owner = Owners.Saja
    load_order = 5

    class Meta:
        db_table = "EmployeeSocialMedia"
        verbose_name_plural = "Employee Social Media"
        managed = False

    def __str__(self):
        return str(self.social_media_type) + " " + str(self.employee)


class CustomerSocialMedia(DescriptiveModel):
    description = 'Customer social media.'
    social_media_code = models.CharField(max_length=60)
    social_media_type = models.ForeignKey(SocialMediaType, on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    date_added = models.DateField(auto_now_add=True)
    owner = Owners.Jade
    load_order = 6

    class Meta:
        db_table = "CustomerSocialMedia"
        verbose_name_plural = "Customer Social Media"
        managed = False

    def __str__(self):
        return str(self.social_media_type) + " " + str(self.customer)


class StoreProduct(DescriptiveModel):
    description = 'Products that are either associated with or are offered at a specific store location.'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    product_assigned = models.DateField(auto_now_add=True)
    owner = Owners.Torrey
    load_order = 5
    category = "Core"

    class Meta:
        db_table = "StoreProduct"
        verbose_name = "StoreProduct/Menu"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['product', 'store'], name='unique_store_product')]

    def __str__(self):
        return str(self.store) + " " + str(self.product)


class StoreReward(DescriptiveModel):
    description = 'Rewards available to loyalty customers based on which specific store points are redeemed at.'
    reward = models.ForeignKey(Reward, on_delete=models.RESTRICT)
    store = models.ForeignKey(Store, on_delete=models.RESTRICT)
    reward_assigned = models.DateField(auto_now_add=True)
    owner = Owners.Saja
    load_order = 5
    category = "Core"

    class Meta:
        db_table = "StoreReward"
        verbose_name = "Store Reward"
        verbose_name_plural = verbose_name
        managed = False
        constraints = [models.UniqueConstraint(fields=['reward', 'store'], name='unique_store_reward')]

    def __str__(self):
        return str(self.store) + " " + str(self.reward)


class OrderReward(DescriptiveModel):
    description = "Effectively the reward equivalent to OrderLine for transactions."
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, unique=True)
    reward = models.ForeignKey(Reward, on_delete=models.RESTRICT)
    point_cost = models.IntegerField(default=0)
    discount_amount = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    free_product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    owner = Owners.Julia
    load_order = 7

    class Meta:
        db_table = "OrderReward"
        verbose_name = "Customer Reward"
        verbose_name_plural = verbose_name
        managed = False

    def save(self, *args, **kwargs):
        target_reward = Reward.objects.get(pk=self.reward.id)
        self.free_product = target_reward.free_product
        self.discount_amount = target_reward.discount_amount
        self.point_cost = target_reward.point_cost
        super(OrderReward, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order) + " " + str(self.reward)


class PointLog(DescriptiveModel):
    description = "Describes all point transactions for a customer in a single table."
    points_amount = models.IntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    reason = models.ForeignKey(PointReason, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    owner = Owners.Jade
    load_order = 7
    bulk_insert = False
    category = "Core"

    class Meta:
        db_table = "PointLog"
        verbose_name = "Point Log"
        verbose_name_plural = verbose_name
        managed = False

    def __str__(self):
        return str(self.customer) + " " + str(self.reason) + " " + str(self.created_date)

    def save(self, *args, **kwargs):
        customer = self.customer.id
        super(PointLog, self).save(*args, **kwargs)
        module_dir = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(module_dir), "TechspireSite", "SQL",
                            "Brett M", "UpdateCustomerPointsSingle.sql")
        sql = open(path).read()
        with connection.cursor() as cursor:
            cursor.execute(sql, [customer])