from django.contrib import admin

from .models import FamilyMember, Marriage

# Register your models here.

class DescendantInline(admin.TabularInline):
    model = Marriage
    fk_name = 'in_law'
    verbose_name = 'Spouse Descendant (Bloodline)'
    extra = 0
    
class InLawInline(admin.TabularInline):
    model = Marriage
    fk_name = 'descendant'
    verbose_name = 'Spouse In-Law (Non Bloodline)'
    extra = 0

class FamilyMemberAdmin(admin.ModelAdmin): 

    inlines = [DescendantInline, InLawInline]
    filter_horizontal = ('parents','children')
    search_fields = ['first_name','middle_name','last_name']
    
class MarriageAdmin(admin.ModelAdmin): 
    search_fields = ['descendant__first_name','descendant__middle_name',
    				'descendant__last_name', 'in_law__first_name',
    				'in_law__middle_name', 'in_law__last_name']


admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(Marriage, MarriageAdmin)

