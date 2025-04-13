from rest_framework import serializers
from .models import Item, PurchaseHeader, PurchaseDetail, SellHeader, SellDetail, SellAllocation

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['code', 'name', 'unit', 'description', 'stock', 'balance']

class PurchaseDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)

    class Meta:
        model = PurchaseDetail
        fields = ['id', 'item_code', 'quantity', 'unit_price']
    
    def to_representation(self, instance):
        """Include item_code in the response"""
        representation = super().to_representation(instance)
        representation['item_code'] = instance.item.code
        return representation
    
    def create(self, validated_data):
        """Create a purchase detail and update item stock/balance"""
        item_code = validated_data.pop('item_code')
        item = Item.objects.get(code=item_code, is_deleted=False)
        header = self.context['header']
        purchase_detail = PurchaseDetail.objects.create(
            header=header,
            item=item,
            **validated_data
        )
        purchase_detail.remaining_quantity = purchase_detail.quantity
        purchase_detail.save()

        # Update item stock and balance
        item.stock += purchase_detail.quantity
        item.balance += purchase_detail.quantity * purchase_detail.unit_price
        item.save()
        return purchase_detail
    
class PurchaseHeaderSerializer(serializers.ModelSerializer):
    details = PurchaseDetailSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseHeader
        fields = ['code', 'date', 'description', 'details']

class SellDetailSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(write_only=True)

    class Meta:
        model = SellDetail
        fields = ['id', 'item_code', 'quantity']
    
    def to_representation(self, instance):
        """Include item_code in the response"""
        representation = super().to_representation(instance)
        representation['item_code'] = instance.item.code
        return representation
    
    def create(self, validated_data):
        """Create a sell detail and update item stock/balance"""
        item_code = validated_data.pop('item_code')
        item = Item.objects.get(code=item_code, is_deleted=False)
        header = self.context['header']
        sell_detail = SellDetail.objects.create(
            header=header,
            item=item,
            **validated_data
        )

        # Deplete stock using FIFO
        remaining_quantity = sell_detail.quantity
        purchase_details = PurchaseDetail.objects.filter(
            item=item,
            remaining_quantity__gt=0,
            header__is_deleted=False
        ).order_by('header__date')
        total_cost = 0

        for pd in purchase_details:
            if remaining_quantity <= 0:
                break
            deplete_qty = min(pd.remaining_quantity, remaining_quantity)
            SellAllocation.objects.create(
                sell_detail=sell_detail,
                purchase_detail=pd,
                quantity=deplete_qty
            )
            pd.remaining_quantity -= deplete_qty
            pd.save()
            total_cost += deplete_qty * pd.unit_price
            remaining_quantity -= deplete_qty
        
        if remaining_quantity > 0:
            raise serializers.ValidationError("Not enough stock to fulfill the sale.")
        
        # Update item stock and balance
        item.stock -= sell_detail.quantity
        item.balance -= total_cost
        item.save()
        return sell_detail

class SellHeaderSerializer(serializers.ModelSerializer):
    details = SellDetailSerializer(many=True, read_only=True)

    class Meta:
        model = SellHeader
        fields = ['code', 'date', 'description', 'details']
