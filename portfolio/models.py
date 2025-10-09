from django.db import models
from django.utils.text import slugify

# --- General Site Information (Singleton Model) ---
class GeneralInfo(models.Model):
    name = models.CharField(max_length=100, help_text="Your name for the navbar logo and footer.")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, help_text="Upload your resume PDF file.")
    hero_title = models.TextField(default="Building digital<br><span class='gradient-text'>experiences</span> that matter")
    hero_subtitle = models.TextField(default="Full-stack developer crafting beautiful, accessible, and performant web applications with modern technologies.")
    about_section_tag = models.CharField(max_length=50, default="About Me")
    about_title = models.CharField(max_length=200, default="Crafting Digital Solutions")
    about_subtitle = models.TextField(default="Passionate about creating innovative web experiences that combine beautiful design with powerful functionality")
    about_image = models.ImageField(upload_to='profile_images/', help_text="Upload your professional headshot.")
    about_content_title = models.CharField(max_length=200, default="Hello! I'm a developer who loves building things for the web.")
    about_content_p1 = models.TextField(default="My journey in web development started years ago...")
    about_content_p2 = models.TextField(default="Currently, I'm focused on building innovative products...")
    projects_completed = models.CharField(max_length=10, default="50+")
    happy_clients = models.CharField(max_length=10, default="30+")
    years_experience = models.CharField(max_length=10, default="3+")
    skills_section_tag = models.CharField(max_length=50, default="Skills")
    skills_title = models.CharField(max_length=200, default="My Capabilities")
    skills_subtitle = models.TextField(default="A blend of modern technologies and core software engineering expertise.")
    projects_section_tag = models.CharField(max_length=50, default="Projects")
    projects_title = models.CharField(max_length=200, default="My Projects")
    projects_subtitle = models.TextField(default="A collection of my work. Use the filters to explore different categories.")
    contact_section_tag = models.CharField(max_length=50, default="Contact")
    contact_title = models.CharField(max_length=200, default="Let's Build Something Amazing")
    contact_text_title = models.CharField(max_length=200, default="Have a project in mind or just want to connect? My inbox is always open.")
    contact_text_subtitle = models.TextField(default="I'm currently available for freelance opportunities...")
    contact_email = models.EmailField(default="youremail@example.com")
    footer_text = models.CharField(max_length=100, default="Designed & Built by Your Name")

    def __str__(self):
        return "General Site Information"

    class Meta:
        verbose_name_plural = "General Info"


# --- Skills Section ---
class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="URL-friendly version of the name. Auto-generated if left blank.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # CHANGED
    svg_icon_code = models.TextField(blank=True, null=True, help_text="Paste the full SVG code for the icon.")

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Expertise(models.Model):
    # CHANGED
    svg_icon_code = models.TextField(blank=True, null=True, help_text="Paste the full SVG code for the icon.")
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

# --- Projects Section ---
class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, help_text="URL-friendly version of the name. Auto-generated if left blank.")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Project Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/')
    github_link = models.URLField(blank=True, null=True)
    live_demo_link = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Check if this project should appear in the 'Featured' tab.")
    categories = models.ManyToManyField(ProjectCategory, related_name='projects')
    tags = models.ManyToManyField(Tag, related_name='projects')

    def __str__(self):
        return self.title


# --- Contact Section ---
class SocialLink(models.Model):
    platform_name = models.CharField(max_length=50, help_text="e.g., GitHub, LinkedIn")
    # CHANGED
    svg_icon_code = models.TextField(blank=True, null=True, help_text="Paste the SVG code from Simple Icons.")
    link = models.URLField()

    def __str__(self):
        return self.platform_name


class ClickEvent(models.Model):
    ACTION_CHOICES = [
        ('RESUME_DOWNLOAD', 'Resume Download'),
        ('PROJECT_LIVE_DEMO', 'Project Live Demo'),
        ('PROJECT_GITHUB', 'Project GitHub'),
        ('EMAIL_CLICK', 'Email Click'),
    ]

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="click_events")
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    details = models.CharField(max_length=255, null=True, blank=True, help_text="e.g., Project ID or other info")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.get_action_type_display()} at {self.timestamp.strftime("%Y-%m-%d %H:%M")}'
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.name} ({self.email})'