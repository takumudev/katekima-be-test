from django.db import models

class BaseModel(models.Model):
    """
    Abstract base model for common fields and soft delete functionality.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
    def delete(self, *args, **kwargs):
        """Override delete method to perform soft delete."""
        self.is_deleted = True
        self.save()

class Item(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    description = models.TextField()
    stock = models.IntegerField(default=0) # Current stock quantity
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0) # Current balance value

    def __str__(self):
        return self.code

class PurchaseHeader(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.code
    
    def delete(self, *args, **kwargs):
        """Soft delete the header and its details."""
        self.is_deleted = True
        self.save()
        self.details.update(is_deleted=True)

class PurchaseDetail(BaseModel):
    header = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchase_details')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_quantity = models.IntegerField(default=0) # Tracks unsold quantity for FIFO

    def __str__(self):
        return f"{self.header.code} - {self.item.code} - {self.quantity}"

class SellHeader(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.code
    
    def delete(self, *args, **kwargs):
        """Soft delete the header and its details."""
        self.is_deleted = True
        self.save()
        self.details.update(is_deleted=True)

class SellDetail(BaseModel):
    header = models.ForeignKey(SellHeader, on_delete=models.CASCADE, related_name='details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='sell_details')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.header.code} - {self.item.code} - {self.quantity}"

class SellAllocation(BaseModel):
    """
    Tracks which purchase batches are depleted by sales.
    """
    sell_detail = models.ForeignKey(SellDetail, on_delete=models.CASCADE, related_name='allocations')
    purchase_detail = models.ForeignKey(PurchaseDetail, on_delete=models.CASCADE, related_name='allocations')
    quantity = models.IntegerField()

    class Meta:
        unique_together = ('sell_detail', 'purchase_detail')
