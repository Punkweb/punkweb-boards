import argparse

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Renames app. Usage rename_app [old_name] [new_name] [classes ...]'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('old_name', nargs=1, type=str)
        parser.add_argument('new_name', nargs=1, type=str)
        parser.add_argument('models', nargs=argparse.REMAINDER, type=str)

    def handle(self, old_name, new_name, models, *args, **options):
        with connection.cursor() as cursor:
            # Rename model
            old_name = old_name[0]
            new_name = new_name[0]
            cursor.execute("UPDATE django_content_type SET app_label='{}' WHERE app_label='{}'".format(new_name, old_name))
            cursor.execute("UPDATE django_migrations SET app='{}' WHERE app='{}'".format(new_name, old_name))

            for model in models:
                cursor.execute("ALTER TABLE {old_name}_{model_name} RENAME TO {new_name}_{model_name}".format(
                    old_name=old_name, new_name=new_name, model_name=model))
