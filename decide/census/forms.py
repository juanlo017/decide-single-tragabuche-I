

from django import forms
from .models import Census


class CreationCensusForm(forms.Form):
    voting_id = forms.IntegerField()
    voter_id = forms.IntegerField()
    name = forms.CharField()
    surname = forms.CharField()
    city = forms.CharField()
    region = forms.CharField()
    gender = forms.CharField()
    birth_year = forms.IntegerField()
    civil_state = forms.CharField()
    has_job = forms.BooleanField()


    class Meta: 
        model = Census
        fields = (
            'voting_id',
            'voter_id',
            'name',
            'surname',
            'city',
            'region',
            'gender',
            'birth_year',
            'civil_state',
            'has_job'
        )

    def save (self, commit = True):
        census = super(CreationCensusForm, self).save(commit = False)
        census.voting_id = self.cleaned_data['voting_id']
        census.voter_id = self.cleaned_data['voter_id']
        census.name = self.cleaned_data['name']
        census.surname= self.cleaned_data['surname']
        census.city = self.cleaned_data['city']
        census.region = self.cleaned_data['region']
        census.gender = self.cleaned_data['gender']
        census.birth_year = self.cleaned_data['birth_year']
        census.civil_state = self.cleaned_data['civil_state']
        census.has_job = self.cleaned_data['has_job']

        if commit : 
            census.save()
        return census