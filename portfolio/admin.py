from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import ClickEvent 
from .models import (
    GeneralInfo, SkillCategory, Skill, Expertise,
    ProjectCategory, Tag, Project, SocialLink,ContactSubmission
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


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action_type', 'get_project_link', 'ip_address')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('ip_address', 'user_agent', 'details', 'project__title')
    readonly_fields = ('timestamp', 'action_type', 'ip_address', 'user_agent', 'details', 'get_project_link')

    @admin.display(description='Project Title')
    def get_project_link(self, obj):
        if obj.project:
            # Create a link to the project's own admin page
            url = reverse('admin:portfolio_project_change', args=[obj.project.pk])
            return format_html('<a href="{}">{}</a>', url, obj.project.title)
        # For non-project clicks, show the details if they exist
        return obj.details or "N/A"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'timestamp')

    def has_add_permission(self, request):
        return False # Disable adding submissions from the admin

    def has_change_permission(self, request, obj=None):
        return False # Disable editing submissions
   
# Register the rest of the models
admin.site.register(GeneralInfo)
admin.site.register(Expertise)
admin.site.register(Tag)
admin.site.register(SocialLink)