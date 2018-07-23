from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    # We want to keep track of history
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # An "active" field will let us keep model instances that
    # represent relationships that aren't in use anymore
    active = models.BooleanField(default=True)
    # I feel like letting users make notes on anything
    # is a great way to discover new features/fields that need
    # to be added and prevent the user's workflow from being
    # artificially limited by my POV as a dev
    notes = models.TextField()

    class Meta:
        abstract = True


class Furniture(BaseModel):
    # Each piece of furniture is 1 piece in 1 warehouse
    category = models.CharField(max_length=200, blank=True)
    sub_category = models.CharField(max_length=200, blank=True)
    budget_sub_category = models.CharField(max_length=200, blank=True)
    product_name = models.CharField(max_length=200, blank=True)
    product_description = models.CharField(max_length=200, blank=True)
    brand = models.CharField(max_length=200, blank=True)
    # Some pieces of furtinure aren't "whole"
    whole = models.BooleanField(default=True)
    # No weird half-cents, plz
    current_unit_cost = models.DecimalField(max_digits=19, decimal_places=2, default=0)

    def add_to_cart(self, cart):
        """ Convenience method

        Add the piece of furniture to a cart to reserve it,
        only if the furniture is not already reserved/assigned.
        """

        # if not (self.is_assigned() or self.is_reserved()):
            # cf = self.cart_furniture_set.create(cart=cart)
            # cf.save()
        pass

    def warehouse(self):
        """ Convenience method

        Because we have history, we need a way to retrieve only the
        active warehouse relationship.

        """
        # self.warehouse_furniture_set.filter(furtinure=self, active=True)
        pass

    def add_to_warehouse(self, warehouse):
        """ Convenience method

        Add the piece of furniture to a warehouse-- either
        from one warehouse to another or from a property
        to a warehouse. In the latter case, should also unassign
        it from the property.
        """
        # if self.is_assigned():
        #     assignment = self.property_furniture_set.filter(furniture=self, active=True).get()
        #     assignment.active = False
        #     assignment.save()
        # wf = self.warehouse_furniture_set.create(warehouse=warehouse)
        # wf.save()
        pass

    def is_assigned(self):
        """ Convenience method

        True if the furniture is currently assigned to a property,
        otherwise false.
        We cannot assign/reserve furniture that is already assigned/reserved.
        """
        # self.property_furniture_set.filter(active=True)
        pass

    def is_reserved(self):
        """ Convenience method

        True if the furniture is currently in a cart, otherwise false.
        We cannot assign/reserve furniture that is already assigned/reserved.
        """
        # self.cart_furniture_set.filter(active=True)
        pass

    def history(self):
        """ Convenience method

        View a list of current and past assignments/locations,
        ordered by date, most recent first.
        """
        # self.cart_furniture_set.all()
        # self.property_furniture_set.all()
        # self.warehouse_furniture_set.all()
        pass



class Property(BaseModel):
    address = models.CharField(max_length=200, unique=True)
    activation_date = models.CharField(max_length=200)
    deactivation_date = models.CharField(max_length=200)

    def furniture(self):
        """ List furniture currently assigned to property """
        # return self.property_furniture_set.filter(active=True)
        pass


class Warehouse(BaseModel):
    address = models.CharField(max_length=200, unique=True)

    def furniture(self):
        """ List furniture currently at warehouse """
        # return self.warehouse_furniture_set.filter(active=True)
        pass


class Cart(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=200, unique=True)

    def furniture(self):
        """ List furniture currently in cart """
        # return self.cart_furniture_set.filter(active=True)
        pass


class CartFurniture(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)


class PropertyFurniture(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)


class WarehouseFurniture(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)
