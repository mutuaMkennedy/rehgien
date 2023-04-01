from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

class BlogCategory(models.Model):
    category_name = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField( blank=False,null=True)
    slug = models.SlugField(blank=False,null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural ='Blog Categories'

class BlogPost(models.Model):
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL,
                    default = None, related_name='blog_post_category', blank=False, null=True)
    title = models.CharField(max_length=125, blank=False)
    slug = models.SlugField(blank=False,null=True)
    text = RichTextField(config_name='blog-post', blank=False)
    thumbnail = CloudinaryField('thumbnail', blank=False, null=True, overwrite=True, resource_type='image',
	 						folder='blog_post_thumb')
    reads = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_post_reads', blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_post_likes', blank=True)
    featured = models.BooleanField(default=False)
    publishdate = models.DateTimeField(auto_now=False, auto_now_add=True)
    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( 'rehgien_pro:blog_detail', kwargs={'slug':self.slug})
