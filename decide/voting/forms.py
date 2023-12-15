from django import forms
from .models import QuestionOption

class QuestionOptionAdminForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = '__all__'

    def clean_option(self):
        option = self.cleaned_data['option']
        question = self.cleaned_data['question']
        number = self.cleaned_data['number']

        if self.instance and self.instance.pk:
            if question.yes_no and option not in ['', 'Yes', 'No']:
                raise forms.ValidationError("Option must be empty. Don't write")
            
        else: 
            if question.yes_no and option not in ['']:
                raise forms.ValidationError("Option must be empty. Don't write")
        return option