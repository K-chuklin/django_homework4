from django.core.management import BaseCommand
from blog.models import Post


class Command(BaseCommand):

    def handle(self, *args, **options):
        posts_list = [
            {
                "name": "statia_#",
                "slug": "statia_#",
                "content": "content_of_statia_#",

            },
            {
                "name": "statia_#",
                "slug": "statia_#",
                "content": "content_of_statia_#",

            },
            {
                "name": "statia_#",
                "slug": "statia_#",
                "content": "content_of_statia_#",

            },
        ]

        posts_objects = []
        for item in posts_list:
            posts_objects.append(Post(**item))

        Post.objects.bulk_create(posts_objects)
