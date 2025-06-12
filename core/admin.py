from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Item, ItemImage, Message

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'department', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'department')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'department', 'profile_photo')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)



class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'item_status', 'category', 'location', 'posted_by', 'created_at', 'is_approved')
    list_filter = ('status', 'item_status', 'category', 'location', 'is_approved', 'created_at')
    search_fields = ('title', 'description', 'posted_by__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [ItemImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status', 'item_status')
        }),
        ('Details', {
            'fields': ('category', 'location', 'date_lost_found', 'time_lost_found')
        }),
        ('Contact & Posting', {
            'fields': ('contact_info', 'posted_by', 'is_approved')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('item__title', 'caption')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('item', 'sender', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('item__title', 'sender__username', 'content')
    readonly_fields = ('created_at',)