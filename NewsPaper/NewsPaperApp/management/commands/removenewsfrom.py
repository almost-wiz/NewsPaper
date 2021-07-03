from django.core.management.base import BaseCommand
from NewsPaperApp.models import Post, Category


class Command(BaseCommand):
    help = '''In order to run the command, you must enter 1 required argument - the category from which you want to delete all posts: python3 manage.py removenewsfrom <your category>'''
    missing_args_message = '''You must enter 1 required argument - the category from which you want to delete all posts: python3 manage.py removenewsfrom <your category>'''

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Do you really want to delete all posts in the category {options["category"]}? y/n\n')

        if answer != 'y':
            self.stdout.write(self.style.ERROR('Denied'))
            return False

        try:
            category = Category.objects.get(position=options['category'])
            Post.objects.filter(categories=category).all().delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted all news from category {category.position}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
