
from django.core.management.base import BaseCommand
from django.db import transaction

from mockapi.models import MockAnswer

import yaml

class Command(BaseCommand):
    help = 'Loads a list of MockAnswer records from a YAML file into the database'

    def add_arguments(self, parser):
        parser.add_argument('yaml', nargs='+')

    def handle(self, *args, **options):
        yamls = options.get('yaml',[])
        for yaml_file in yamls:
            self.load_yaml(yaml_file)
        print "------\nDone.\n"
    
    def load_yaml(self, yaml_file):
        with open(yaml_file) as f:
            content = yaml.load(f)
        print "\nLoading {}:".format(yaml_file)
        with transaction.atomic():
            for record in content:
                ma = MockAnswer.objects.create(**record)
                print "  ", ma.req_method, ma.url

