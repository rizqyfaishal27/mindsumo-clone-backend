from django.contrib import admin
from django.forms import ModelForm
from .models import CustomUser, Skill, Challenge, Submission

class CustomAdminSite(admin.AdminSite):
    site_header = "Suara.in"
    site_title = "Suara.in Admin Portal"
    index_title = "Welcome to Suara.in CMS"

admin_site = CustomAdminSite(name='suara_in_admin')

class ChallengeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super (ChallengeForm, self ).__init__(*args, **kwargs) 
        self.fields['author'].queryset = CustomUser.objects.filter(is_staff=True)

    class Meta:
        exclude = []
        model = Challenge


# Register your models here.    

class SubmissionTableInline(admin.TabularInline):
    model = Submission
    exclude = ['submission_text', ]
    readonly_fields = ['submission_user', 'submission_title', 'submission_file', ]
    extra = 0
    max_num = 0
    show_change_link = True
    can_delete = False
    can_add = False
    can_edit = False

    

class SkillAdmin(admin.ModelAdmin):
    list_display = ['skill_name', 'created_at']
    ordering = ['skill_name']

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    ordering = ['id']

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'status']
    search_fields = ['skills']
    filter_horizontal = ['skills']
    form = ChallengeForm
    inlines = [
        SubmissionTableInline
    ]

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['submission_user', 'challenge', 'submission_title', 'created_at']
    ordering = ['created_at']



admin_site.register(Challenge, ChallengeAdmin)
admin.site.register(Skill, SkillAdmin)
admin_site.register(Submission, SubmissionAdmin)
admin_site.register(CustomUser, CustomUserAdmin)