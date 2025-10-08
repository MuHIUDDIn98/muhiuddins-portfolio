from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import (
    GeneralInfo,
    SkillCategory,
    Expertise,
    ProjectCategory,
    Project,
    SocialLink,  
    ClickEvent  
)

# --- Helper function to get the real IP address ---
def get_ip_address(request):
    """Returns the real IP address of the user."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# --- Main view for displaying the portfolio page ---
def portfolio_view(request):
    general_info = GeneralInfo.objects.first()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    expertises = Expertise.objects.all()
    project_categories = ProjectCategory.objects.all()
    projects = Project.objects.prefetch_related('categories', 'tags').all()
    social_links = SocialLink.objects.all()

    context = {
        'info': general_info,
        'skill_categories': skill_categories,
        'expertises': expertises,
        'project_categories': project_categories,
        'projects': projects,
        'social_links': social_links,
    }
    return render(request, 'index.html', context)


# --- View for tracking user clicks ---
def track_click(request):
    action = request.GET.get('action')
    redirect_url = request.GET.get('redirect_url')
    details_param = request.GET.get('details') # Use a different name to avoid confusion

    project_instance = None
    # If the click is project-related, try to find the project object
    if action in ['PROJECT_LIVE_DEMO', 'PROJECT_GITHUB'] and details_param:
        try:
            # We expect 'details_param' to be the project's ID
            project_instance = Project.objects.get(pk=int(details_param))
        except (Project.DoesNotExist, ValueError):
            # If the ID is invalid or project doesn't exist, we just ignore it
            project_instance = None

    if action:
        ClickEvent.objects.create(
            action_type=action,
            ip_address=get_ip_address(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            project=project_instance,  # Save the linked project object here
            details=f"Project ID: {details_param}" if project_instance else details_param
        )
    
    if redirect_url:
        return HttpResponseRedirect(redirect_url)
    
    return HttpResponse(status=204)