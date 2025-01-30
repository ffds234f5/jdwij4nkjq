from django import forms
from .models import Question, Choice
from django.utils import timezone

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = kwargs.pop('choices', [])
        for i in range(len(self.choices)):
            field_name = f'choice_{i}'
            self.fields[field_name] = forms.CharField(
                label=f'Choice {i + 1}',
                initial=self.choices[i],
                required=False
            )
        if not self.instance.pk:
            self.initial['pub_date'] = timezone.now()

