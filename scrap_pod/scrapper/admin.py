from django.contrib import admin
from django.apps import apps
from .models import Categories, Store, SubCategories, Product

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')
admin.site.register(Categories, CategoriesAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'store')
    list_filter = ('category', 'sub_category', 'store')
admin.site.register(Product, ProductsAdmin)

# Get the app config for the 'scrapper' app
app_config = apps.get_app_config('scrapper')

# Get all models from the 'scrapper' app
models = app_config.get_models()

# Register all models with the admin site
for model in models:
    # Check if the model is already registered
    if not admin.site.is_registered(model):
        admin.site.register(model)
