import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from voting import models as VotingModels
from django.shortcuts import render

def get_all_votings():
    return VotingModels.Voting.objects.all()

def get_voting(voting_id):
    try:
        return VotingModels.Voting.objects.get(pk=voting_id)
    except VotingModels.Voting.DoesNotExist:
        raise Http404("Voting does not exist")

def general_stats(request):
    votings = get_all_votings()

    data = {}

    #quiero desglosar los datos de cada votacion y asignarselos a data para que se los pase a la plantilla con el nombre de la votacion como key
    for voting in votings:
        print(f'{voting.get_votes(token="")}')
        #data[voting.name] = {}

    return render(request, 'stats/general.html', {'votings': data})
