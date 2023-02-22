from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import models
from django.urls import reverse

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):

    objects = models.Manager() # default Manager
    published = PublishedManager() # custom model manager

    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published')
    )

    title   = models.CharField(max_length=200)
    slug    = models.SlugField(max_length=100)
    author  = models.ForeignKey(User, related_name="blog_posts",   on_delete = models.DO_NOTHING,)
    body    = models.TextField()
    likes   = models.ManyToManyField(User ,related_name='likes' ,blank=True)
    created = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created.
    updated = models.DateTimeField(auto_now=True) #Automatically set the field to now every time the object is saved.
    status  = models.CharField(max_length=100 ,choices=STATUS_CHOICES, default='draft')
    restrict_comment = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
            ordering = ['-id']

    def _str_(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id,self.slug])

#this method create the slug
@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug=slugify(kwargs['instance'].title)
    kwargs['instance'].slug=slug



class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    dob=models.DateField(null=True)
    photo = models.ImageField(null=True,blank=True,upload_to='media/')


    def __str__(self):
        return "Profile of user {}".format(self.user.username)


class Images(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


    def __str__(self):
        return str(self.post.id)


class Comments(models.Model):

    # by making ForeignKey ‘self’ you make recursive relationships.
    # They work similar to how One to #Many relationships. But as the name suggests, the model references itself.

    post = models.ForeignKey(Post ,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(max_length=160)
    reply=models.ForeignKey('self',null=True,related_name='replies',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))
