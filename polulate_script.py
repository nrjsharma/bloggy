import os,django,random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialMedia.settings")
django.setup()


from django.contrib.auth.models import User
from faker import Faker
from blog.models import Post
from django.utils import timezone


def create_post(N):
    fake = Faker()

    for i in range(N):
        id=random.randint(1,3)
        title=fake.name()
        status=random.choice(['published','draft'])
        Post.objects.create(

            title=title,
            author=User.objects.get(id=id),
            slug="-".join(title.lower().split()),
            body=fake.text(),
            status=status,
            created=timezone.now(),
            updated=timezone.now(),

        )

create_post(5)
print('post created')