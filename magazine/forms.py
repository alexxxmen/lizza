# -*- coding: utf-8 -*-

from django.forms import ModelForm
from magazine.models import Feedback, Order
from django import forms


class CartAddProductForm(forms.Form):
    count = forms.IntegerField(max_value=1000, min_value=1)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'text']


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = ['name', 'subject', 'email', 'phone', 'text']
