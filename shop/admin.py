from django.contrib import admin
from .models import Product, Order, OrderItem


admin.site.site_header = "🍰 Dessert Shop Admin Panel"
admin.site.site_title = "Admin"
admin.site.index_title = "Welcome to Dessert Shop Management"



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "is_active", "created_at", "product_status")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "is_active")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    
    fieldsets = (
        ("📦 Basic Information", {
            "fields": ("name", "price", "stock")
        }),
        ("📝 Details", {
            "fields": ("description",)
        }),
        ("🖼️ Images", {
            "fields": ("image", "image_mobile", "image_tablet", "image_desktop"),
            "classes": ("collapse",)
        }),
        ("⚙️ Settings", {
            "fields": ("is_active", "created_at")
        }),
    )
    
    def product_status(self, obj):
        if obj.stock > 10:
            return "✅ In Stock"
        elif obj.stock > 0:
            return "⚠️ Low Stock"
        else:
            return "❌ Out of Stock"
    product_status.short_description = "Status"



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "get_product_price")
    can_delete = False
    fields = ("product", "quantity", "get_product_price")
    
    def get_product_price(self, obj):
        """عرض سعر المنتج"""
        return f"${obj.product.price:.2f}"
    get_product_price.short_description = "Unit Price"



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
   
    list_display = ("id", "customer_name", "phone", "get_short_address", "get_order_items", "get_total", "status", "created_at", "order_badge")
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "phone", "address")
    readonly_fields = ("created_at", "get_order_summary")
    list_per_page = 20
    ordering = ("-created_at",)
    inlines = [OrderItemInline]
    
    fieldsets = (
        ("👤 Customer Information", {
            "fields": ("customer_name", "phone", "address")
        }),
        ("💰 Order Details", {
            "fields": ("status", "created_at", "get_order_summary")
        }),
    )
    
  
    def get_short_address(self, obj):
        """عرض العنوان مختصر (أول 30 حرف)"""
        if obj.address:
            if len(obj.address) > 30:
                return obj.address[:30] + "..."
            return obj.address
        return "No address"
    get_short_address.short_description = "Address"
    
    def get_order_items(self, obj):
        """عرض المنتجات في القائمة"""
        items = obj.items.all()
        if not items:
            return "No items"
        
        items_list = [f"{item.product.name} x{item.quantity}" for item in items[:3]]
        result = ", ".join(items_list)
        
        if items.count() > 3:
            result += f" (+{items.count() - 3} more)"
        
        return result
    get_order_items.short_description = "Order Items"
    
    def get_total(self, obj):
        """حساب المجموع الكلي"""
        total = sum(item.quantity * item.product.price for item in obj.items.all())
        return f"${total:.2f}"
    get_total.short_description = "Total"
    
    def get_order_summary(self, obj):
        """ملخص الطلب الكامل (في صفحة التفاصيل)"""
        items = obj.items.all()
        if not items:
            return "No items in this order"
        
        summary = []
        total = 0
        
        for item in items:
            item_total = item.quantity * item.product.price
            total += item_total
            summary.append(
                f"• {item.product.name} - Qty: {item.quantity} - "
                f"Unit Price: ${item.product.price:.2f} - "
                f"Subtotal: ${item_total:.2f}"
            )
        
        summary.append(f"\n💰 Total: ${total:.2f}")
        
        return "\n".join(summary)
    get_order_summary.short_description = "Order Summary"
    
    def order_badge(self, obj):
        status_map = {
            "pending": "🟡 Pending",
            "confirmed": "🟢 Confirmed",
            "completed": "✅ Completed",
            "cancelled": "🔴 Cancelled"
        }
        return status_map.get(obj.status, obj.status)
    order_badge.short_description = "Status Badge"
    
    actions = ["mark_as_completed", "mark_as_cancelled"]
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status="completed")
        self.message_user(request, f"{updated} order(s) marked as completed.")
    mark_as_completed.short_description = "✅ Mark selected orders as completed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"{updated} order(s) marked as cancelled.")
    mark_as_cancelled.short_description = "🔴 Mark selected orders as cancelled"
