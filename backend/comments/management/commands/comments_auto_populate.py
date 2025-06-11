from django.core.management.base import BaseCommand

from ._comment_generator import CommentGenerator


class Command(BaseCommand):

    help = "Populate db with data"

    def add_arguments(self, parser):
        parser.add_argument(
            '-l',
            '--language',
            default='en_US',
            type=str,
            help='Language for generated data',
            metavar='language',
        )
        parser.add_argument(
            '-a',
            '--amount',
            default=1,
            type=int,
            help='Number to objects to create',
            metavar='amount',
        )
        parser.add_argument(
            '-f',
            '--frequency',
            default=1,
            type=int,
            help='Frequency of new TopComments',
            metavar='frequency',
        )

    def handle(self, *args, **options):
        cg_args = {
            'language': options['language'],
            'amount': options['amount'],
            'frequency': options['frequency'],
        }
        cg = CommentGenerator(**cg_args)
        cg.run()
