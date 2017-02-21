from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='category',
                             on_delete=models.CASCADE)
    name = models.TextField(max_length=30)

    class Meta:
        unique_together = (
            ('user', 'name'),
        )

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='expenses',
                             on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="expenses/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='expenses',
                                 null=True, blank=True)

    def __str__(self):
        return "[#{}] ${} @{} {}".format(
            self.id,
            self.amount,
            self.date,
            self.title or "---"
        )

    def get_absolute_url(self):
        return reverse("expenses:detail", args=(self.id,))


class Comment(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE,
                                related_name="comments")
    added_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
