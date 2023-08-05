from django.contrib import admin
from .models import Menu, MenuGroup, MenuCustom
from parler.admin import TranslatableAdmin

# class MenuAdmin(admin.ModelAdmin):    
#     list_filter = ('name', 'parent',) 
#     list_display = ['name', 'parent', 'link', 'order_menu', 'kind', 'updated_at']
#     search_fields = ('name', 'parent')
#     ordering = ('-updated_at',)

admin.site.register(Menu, TranslatableAdmin)

# class MenuGroupAdmin(admin.ModelAdmin):
#     list_filter = ('name',) 
#     list_display = ['name', 'updated_at']
#     search_fields = ('name',)
#     ordering = ('-updated_at',)

admin.site.register(MenuGroup, TranslatableAdmin)

# tidak di update model yg ini
class MenuCustomAdmin(admin.ModelAdmin):
    list_filter = ('menu',) 
    list_display = ['menu', 'menu_group', 'updated_at']
    search_fields = ('menu',)
    ordering = ('-updated_at',)

admin.site.register(MenuCustom, MenuCustomAdmin)