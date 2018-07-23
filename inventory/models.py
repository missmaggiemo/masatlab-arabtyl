from django.db import models
from django.core.exceptions import ObjectDoesNotExist
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
    notes = models.TextField(blank=True)

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

    @classmethod
    def available_pieces(cls):
        """ List all peices that aren't assigned or reserved """
        all_furniture = cls.objects.filter(active=True)  # Exclude retired peices
        return [f for f in all_furniture if not (f.is_assigned() or f.is_reserved())]

    def add_to_cart(self, cart):
        """ Convenience method

        Add the piece of furniture to a cart to reserve it,
        only if the furniture is not already reserved/assigned.
        """
        if (self.is_assigned() or self.is_reserved()):
            raise Exception('Furniture peice assigned or reserved')
        cf = self.cartfurniture_set.create(cart=cart)
        cf.save()
        return self

    def add_to_property(self, property):
        """ Convenience method

        Add the piece of furniture to a property, only if the
        furniture is reserved.
        """
        if self.is_assigned():
            raise Exception('Furniture peice already assigned')
        if not self.is_reserved():
            raise Exception('Furniture peice must be reserved before assigning')
        # Remove from current cart (but keep history)
        cf = self.cartfurniture_set.get(active=True)
        cf.active = False
        cf.save()
        # Add to property
        pf = self.propertyfurniture_set.create(property=property)
        pf.save()
        # Remove from warehouse (but keep history)
        wf = self.warehousefurniture_set.get(active=True)
        wf.active = False
        wf.save()
        return self

    def current_warehouse(self):
        """ Convenience method

        Because we have history, we need a way to retrieve only the
        active warehouse relationship.

        """
        try:
            return self.warehousefurniture_set.get(active=True)
        except ObjectDoesNotExist:
            return None

    def current_property(self):
        """ Convenience method

        Because we have history, we need a way to retrieve only the
        active warehouse relationship.

        """
        try:
            return self.propertyfurniture_set.get(active=True)
        except ObjectDoesNotExist:
            return None

    def current_cart(self):
        """ Convenience method

        Because we have history, we need a way to retrieve only the
        active warehouse relationship.

        """
        try:
            return self.cartfurniture_set.get(active=True)
        except ObjectDoesNotExist:
            return None

    def add_to_warehouse(self, warehouse):
        """ Convenience method

        Add the piece of furniture to a warehouse-- either
        from one warehouse to another or from a property
        to a warehouse. In the latter case, should also unassign
        it from the property.
        """
        if self.is_assigned():
            assignment = self.current_property()
            assignment.active = False
            assignment.save()
        wf = self.warehousefurniture_set.create(warehouse=warehouse)
        wf.save()
        return wf

    def is_assigned(self):
        """ Convenience method

        True if the furniture is currently assigned to a property,
        otherwise false.
        We cannot assign/reserve furniture that is already assigned/reserved.
        """
        return bool(self.current_property())

    def is_reserved(self):
        """ Convenience method

        True if the furniture is currently in a cart, otherwise false.
        We cannot assign/reserve furniture that is already assigned/reserved.
        """
        return bool(self.current_cart())

    def history(self):
        """ Convenience method

        View a list of current and past assignments/locations,
        ordered by date, most recent first.
        """
        history = list(self.cartfurniture_set.all()) + \
            list(self.propertyfurniture_set.all()) + \
            list(self.warehousefurniture_set.all())
        return sorted(history, reverse=True, key=lambda obj: obj.updated)


class Property(BaseModel):
    address = models.CharField(max_length=200, unique=True)
    activation_date = models.DateTimeField(null=True, blank=True)
    deactivation_date = models.DateTimeField(null=True, blank=True)

    def furniture(self):
        """ List furniture currently assigned to property """
        return list(self.propertyfurniture_set.filter(active=True))


class Warehouse(BaseModel):
    address = models.CharField(max_length=200, unique=True)

    def furniture(self):
        """ List furniture currently at warehouse """
        return list(self.warehousefurniture_set.filter(active=True))


class Cart(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    property = models.ForeignKey(Property, on_delete=models.PROTECT, null=True)

    def furniture(self):
        """ List furniture currently in cart """
        return [cf.furniture for cf in self.cartfurniture_set.filter(active=True)]

    def check_out(self):
        for cf in self.cartfurniture_set.filter(active=True):
            cf.furniture.add_to_property(self.property)
        self.active = False
        self.save()
        return self

    def clear(self):
        # The one time where we want to remove the CartFurniture models
        # is when we're clearing an active cart-- if the cart is inactive,
        # that means it has been checked out, and we want to save the
        # history
        if not self.active:
            raise Exception('Cannot delete items from an inactive cart')
        self.cartfurniture_set.all().delete()
        return self

class CartFurniture(BaseModel):
    """ Basic join model, important for keeping history """
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)


class PropertyFurniture(BaseModel):
    """ Basic join model, important for keeping history """
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)


class WarehouseFurniture(BaseModel):
    """ Basic join model, important for keeping history """
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)
