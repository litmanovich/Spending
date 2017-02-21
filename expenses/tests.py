from django.contrib.auth.models import User
from django.test import TestCase
from . import models
import calendar
import silly
import random


class ExpensesTests(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create(username='user{}'.format(i))
            for i in range(1, 5)
            ]

    def create_expense(self):
        o = models.Expense(
            user = self.users[0],
            date="2012-04-22",
            amount="15.23",
            title="Pizza",
            description="For My birthday\nOlive + Mushroom.",
        )
        o.full_clean()
        o.save()

        return o

    def test_basic_expense(self):
        n = models.Expense.objects.count()
        o = self.create_expense()
        self.assertEquals(n + 1, models.Expense.objects.count())
        o.delete()

    def test_comments(self):
        o = self.create_expense()

        c1 = models.Comment(
            expense=o,
            content="Hello!!!!",
        )
        c1.full_clean()
        c1.save()

        c2 = models.Comment.objects.create(
            expense=o,
            content="Hello 222222!!!!",
        )

        # qs = models.Comment.objects.filter(expense=o)
        # - euqals to -
        # qs = o.comment_set.all()
        qs = o.comments.all()

        self.assertEquals(qs.count(), 2)

        c3 = o.comments.create(
            content="Hello 22123213212222!!!!",
        )

        self.assertEquals(qs.count(), 3)

    def test_categories(self):
        n = User.objects.count()
        user1, created = User.objects.get_or_create(username='Danny')
        user1.save()
        self.assertEquals(User.objects.all().count(), n + 1)

        cat_food = models.Category(user=user1, name='Food')
        cat_food.save()
        cat_rent = models.Category(user=user1, name='Rent')
        cat_rent.save()
        cat_utilities = models.Category(user=user1, name='Utilities')
        cat_utilities.save()
        self.assertEquals(models.Category.objects.filter(user=user1).count(), 3)

        o = models.Expense(
            user=user1,
            date="2017-02-20",
            amount="10.19",
            title="Pizza",
            description="Pepperoni",
            category=cat_food,
        )
        o.save()

        for i in range(1, 13):
            o = models.Expense(
                user=user1,
                date="2017-{:02}-20".format(i),
                amount="30.55",
                title="Electricity bill for {}".format(calendar.month_name[i]),
                description="Electricity bill",
                category=cat_utilities,
            )
            o.save()

        self.assertEquals(models.Expense.objects.filter(user=user1, category=cat_food).count(), 1)
        self.assertEquals(models.Expense.objects.filter(user=user1, category=cat_utilities).count(), 12)
        e = models.Expense.objects.get(user=user1, date="2017-06-20")
        self.assertEquals(e.title, "Electricity bill for June")

        user2, created = User.objects.get_or_create(username='Sarah')
        cats = []
        for cname in 'Car', 'Parking', 'Food':
            c = models.Category(user=user2, name=cname)
            c.save()
            cats.append(c)
        for i in range(100):
            o = models.Expense(
                user=user2,
                date="2017-01-01",
                amount="10.01",
                title=silly.noun().title(),
                description=silly.sentence(),
                category=cats[random.randint(0, 2)],
            )
            o.save()
        self.assertEquals(models.Expense.objects.filter(user=user2).count(), 100)
        self.assertGreaterEqual(models.Expense.objects.filter(user=user2, category=cats[1]).count(), 0)
        self.assertLessEqual(models.Expense.objects.filter(user=user2, category=cats[1]).count(), 100)
