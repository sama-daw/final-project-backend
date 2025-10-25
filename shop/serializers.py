from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    # ✅ جعل حقول الصور اختيارية عند التحديث
    image_thumbnail = serializers.ImageField(required=False, allow_null=True)
    image_mobile = serializers.ImageField(required=False, allow_null=True)
    image_tablet = serializers.ImageField(required=False, allow_null=True)
    image_desktop = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'is_active',
            'created_at',
            'image_thumbnail',
            'image_mobile',
            'image_tablet',
            'image_desktop',
        ]
        read_only_fields = ['id', 'created_at']
    
    def update(self, instance, validated_data):
        """
        ✅ عند التحديث، إذا لم تُرسل صورة جديدة، احتفظ بالصورة القديمة
        """
        # إزالة الصور الفارغة من البيانات المُراد تحديثها
        for field in ['image_thumbnail', 'image_mobile', 'image_tablet', 'image_desktop']:
            if field in validated_data and validated_data[field] is None:
                validated_data.pop(field)
        
        return super().update(instance, validated_data)


class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemInputSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'phone', 'address', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Items list cannot be empty.")
        
        seen = set()
        for it in items:
            pid = it.get('product_id')
            qty = it.get('quantity', 0)
            
            if pid in seen:
                raise serializers.ValidationError(f"Duplicate product_id {pid} in items.")
            seen.add(pid)
            
            if qty <= 0:
                raise serializers.ValidationError("Quantity must be a positive integer.")
        
        return items
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            
            for it in items_data:
                product = Product.objects.select_for_update().get(pk=it['product_id'])
                qty = it['quantity']
                
                if product.stock < qty:
                    raise serializers.ValidationError({
                        "items": f"Insufficient stock for product {product.id}"
                    })
                
                Product.objects.filter(pk=product.pk).update(stock=F('stock') - qty)
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=product.price
                )
        
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'phone', 'address', 'status', 'created_at', 'items']
