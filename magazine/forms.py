# -*- coding: utf-8 -*-

from django.forms import ModelForm
from magazine.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'subject', 'email', 'phone', 'text']
