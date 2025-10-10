# portfolio/views.py

import logging  # 1. Import the logging library
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
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

# 2. Get an instance of the logger for this file
logger = logging.getLogger(__name__)


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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # 3. Add success logging
            logger.info(f"New contact form submission from {form.cleaned_data.get('email')}")
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('portfolio')
        else:
            # 4. Add error logging for form validation failures
            logger.error(f"Contact form submission failed. Errors: {form.errors.as_json()}")
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = ContactForm()

    general_info = GeneralInfo.objects.first()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    expertises = Expertise.objects.all()
    project_categories = ProjectCategory.objects.all()
    projects = Project.objects.prefetch_related('categories', 'tags').all()
    social_links = SocialLink.objects.all()

    context = {
        'form': form,
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
    details_param = request.GET.get('details')

    project_instance = None
    if action in ['PROJECT_LIVE_DEMO', 'PROJECT_GITHUB'] and details_param:
        try:
            project_instance = Project.objects.get(pk=int(details_param))
        except (Project.DoesNotExist, ValueError):
            # 5. Add warning log for non-critical errors
            logger.warning(f"Could not find project with ID '{details_param}' for click tracking.")
            project_instance = None

    if action:
        # 6. Add info logging for tracking events
        logger.info(f"Tracking click event. Action: {action}, Details: {details_param}, IP: {get_ip_address(request)}")
        ClickEvent.objects.create(
            action_type=action,
            ip_address=get_ip_address(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            project=project_instance,
            details=f"Project ID: {details_param}" if project_instance else details_param
        )

    if redirect_url:
        return HttpResponseRedirect(redirect_url)

    return HttpResponse(status=204)