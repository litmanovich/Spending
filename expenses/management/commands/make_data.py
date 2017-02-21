import datetime
import random

import silly
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from expenses import models


def get_random_date():
    while True:
        try:
            return datetime.date(
                random.randint(2010, 2019),
                random.randint(1, 12),
                random.randint(1, 30)
            )
        except ValueError:
            # non existent date
            pass


def get_paragraph(a, b):
    """
    Produces a paragraph of text with between a and b sentences.
    """
    return "\n".join([silly.sentence() for x in range(random.randint(a, b))])


class Command(BaseCommand):
    help = "Adds demo data to database."

    def add_arguments(self, parser):
        parser.add_argument('-n', '--number', type=int)
        parser.add_argument('--clear', action='store_true', help='Remove all data', default=False)

    def handle(self, *args, **options):
        if not options['clear'] and not options['number']:
            self.print_help('make_data', 'help')
            return

        if options['clear']:
            User.objects.all().delete()
            print("Removed all data")

        if options['number']:
            n = options['number']
            users = []
            added = 0
            for i in range(1, 6):
                user, created = User.objects.get_or_create(
                    username='user{}'.format(i),
                )
                user.set_password("secret1234")
                user.save()
                users.append(user)
                if created:
                    added += 1
                    for j in range(random.randint(1, 5)):
                        c, created = models.Category.objects.get_or_create(user=user, name=silly.noun().title())
                        c.save()
            print("Added {} users".format(added))

            for i in range(n):
                o = models.Expense(
                    user=random.choice(users),
                    date=get_random_date(),
                    amount="{:.2f}".format(random.uniform(1, 100)),
                    title="{} {}".format(silly.adjective(), silly.noun()).title(),
                    description=get_paragraph(1, 3),
                )
                o.full_clean()
                o.save()
                for i in range(random.randint(0, 5)):
                    o.comments.create(
                        content=get_paragraph(1, 4),
                    )

            print("Added {} expenses".format(n))
