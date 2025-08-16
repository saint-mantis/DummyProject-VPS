from django.contrib import admin
from .models import PropertyType, Location, Agent, PropertyFeature, Property, PropertyImage, Inquiry, Testimonial, Favorite, Contact


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'latitude', 'longitude']
    list_filter = ['parent']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'experience_years', 'rating', 'total_sales', 'is_active']
    list_filter = ['is_active', 'experience_years']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['joined_date']


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'location', 'agent', 'status', 'is_featured', 'created_at']
    list_filter = ['property_type', 'status', 'listing_type', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'address']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [PropertyImageInline]
    filter_horizontal = ['features']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'property_type', 'listing_type', 'status')
        }),
        ('Price & Financial', {
            'fields': ('price', 'price_per_sqft')
        }),
        ('Location', {
            'fields': ('location', 'address', 'latitude', 'longitude')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'area_sqft', 'lot_size', 'year_built', 'parking_spaces')
        }),
        ('Features & Management', {
            'fields': ('features', 'agent')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_published')
        })
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'property', 'inquiry_type', 'status', 'created_at']
    list_filter = ['inquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'property__title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'agent', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['name', 'content']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'property__title']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'subject', 'status', 'created_at']
    list_filter = ['inquiry_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Management', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
