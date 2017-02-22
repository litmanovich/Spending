from django import forms

from expenses import models


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = models.Expense
        exclude = (
            'user',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = (
            'content',
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = (
            'user',
        )


class FeebackForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    phone = forms.CharField(required=False)

