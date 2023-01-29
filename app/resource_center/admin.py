from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from . import models

class BlogPostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget(config_name='blog-post'))
    class Meta:
        model = models.BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title','blog_category','slug']
    prepopulated_fields = {"slug": ("title",)}

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','slug']
    prepopulated_fields = {"slug": ("category_name",)}

admin.site.register(models.BlogPost,BlogPostAdmin)
admin.site.register(models.BlogCategory,BlogCategoryAdmin)
