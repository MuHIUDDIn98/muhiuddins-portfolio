from django.contrib import admin
from .models import ClickEvent 
from .models import (
    GeneralInfo, SkillCategory, Skill, Expertise,
    ProjectCategory, Tag, Project, SocialLink,
    LicenseCategory, License 
)

# Use inline for a better editing experience when inside a Category
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    inlines = [SkillInline]
    prepopulated_fields = {'slug': ('name',)}

# --- [NEW] Register the Skill model directly ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # This shows the skill name and its category in the list
    list_display = ('name', 'category')
    # This adds a filter sidebar to filter skills by their category
    list_filter = ('category',)
    # This adds a search bar to search by skill name
    search_fields = ('name',)


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured')
    list_filter = ('is_featured', 'categories')
    filter_horizontal = ('categories', 'tags')

@admin.register(LicenseCategory)
class LicenseCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Find and replace your old CertificationAdmin with this LicenseAdmin
@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'date_issued', 'display_order')
    list_editable = ('display_order',)
    list_filter = ('categories',)
    filter_horizontal = ('categories',) # Better UI for ManyToMany fields
 

@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action_type', 'ip_address', 'details')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('ip_address', 'user_agent', 'details')
    readonly_fields = ('timestamp', 'action_type', 'ip_address', 'user_agent', 'details')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    
# Register the rest of the models
admin.site.register(GeneralInfo)
admin.site.register(Expertise)
admin.site.register(Tag)
admin.site.register(SocialLink)
