from django.db import models
from decimal import Decimal
import random


def generate_random_color():
    return f"#{random.randint(0, 0xFFFFFF):06x}"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default=generate_random_color)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class UnitOfMeasure(models.Model):
    """Units like: ml, L, g, kg, units, etc."""
    name = models.CharField(max_length=50, unique=True)  # e.g., "milliliter", "liter"
    abbreviation = models.CharField(max_length=10, unique=True)  # e.g., "ml", "L"
    
    class Meta:
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class Presentation(models.Model):
    """
    Presentation types for products.
    Examples: Plastic Bottle, Glass Bottle, Vidon, Tetra Pak, Can, etc.
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Base product representing the core item (e.g., "Water", "Coca Cola").
    The actual purchasable items are ProductVariants.
    """
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    category = models.ManyToManyField(Category, related_name='products')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images', blank=True)
    
    class Meta:
        unique_together = ['name', 'brand']
    
    def __str__(self):
        return f"{self.brand} - {self.name}" if self.brand else self.name


class ProductVariant(models.Model):
    """
    A specific variant of a product with a particular presentation and size.
    Example: "San Luis Water" in "Plastic Bottle" of "500ml"
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    presentation = models.ForeignKey(Presentation, on_delete=models.PROTECT, related_name='variants')
    size = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 500, 1, 2
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, related_name='variants')
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Stock Keeping Unit
    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='variant_images', blank=True)  # Override product image if needed
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['product', 'presentation', 'size', 'unit']
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
    
    def __str__(self):
        return f"{self.product} - {self.presentation} {self.size}{self.unit.abbreviation}"
    
    def get_display_name(self):
        """Returns a user-friendly display name."""
        return f"{self.product.name} {self.size}{self.unit.abbreviation} ({self.presentation})"


class ProductEquivalent(models.Model):
    """
    Defines equivalency relationships between product variants.
    Example: 1x "1L Water Bottle" = 2x "500ml Water Bottle"
    
    Usage:
        - source_variant: The reference variant (e.g., 1L bottle)
        - source_quantity: How many of the source (e.g., 1)
        - equivalent_variant: The equivalent variant (e.g., 500ml bottle)  
        - equivalent_quantity: How many of the equivalent (e.g., 2)
    
    This means: 1 unit of source = equivalent_quantity units of equivalent
    """
    source_variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE, 
        related_name='equivalents_as_source'
    )
    source_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('1.00')
    )
    equivalent_variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.CASCADE, 
        related_name='equivalents_as_target'
    )
    equivalent_quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    
    class Meta:
        unique_together = ['source_variant', 'equivalent_variant']
        verbose_name = "Product Equivalent"
        verbose_name_plural = "Product Equivalents"
    
    def __str__(self):
        return (
            f"{self.source_quantity}x {self.source_variant.get_display_name()} = "
            f"{self.equivalent_quantity}x {self.equivalent_variant.get_display_name()}"
        )
    
    def get_ratio(self):
        """Returns how many equivalent_variant units equal one source_variant."""
        return self.equivalent_quantity / self.source_quantity
    
    def convert(self, source_qty):
        """
        Convert a quantity of source_variant to equivalent_variant.
        Example: If 1L = 2x500ml, convert(3) returns 6 (3 liters = 6 x 500ml)
        """
        return (Decimal(str(source_qty)) / self.source_quantity) * self.equivalent_quantity