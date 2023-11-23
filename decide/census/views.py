from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .forms import CreationCensusForm
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .resources import CensusResource
from django.views.generic import ListView
from tablib import Dataset

def votingIdSet():
    lista=[]
    for census in Census.objects.all():
        lista.append(census.voting_id)
    conjunto=set(lista)
    return conjunto

def filter(request):
    censo = Census.objects.all()
    votingIds = votingIdSet()
    return render(request, 'filterCensus.html',{'census' : censo, 'votingsIds': votingsIds})

class FilterVotingID(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(voting_id__icontains=query).order_by('-voting_id')

class FilterVoterID(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(voting_id__icontains=query).order_by('-voter_id')

class FilterName(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Census.objects.filter(name__icontains=query).order_by('-name')

class FilterSurname(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('i')
        return Census.objects.filter(surname__icontains=query).order_by('-surname')

class FilterCity(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(city__icontains=query).order_by('-city')

class FilterRrgion(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(region__icontains=query).order_by('-region')

class FilterGender(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(gender__icontains=query).order_by('-gender')

class FilterBirthYear(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(birth_year__icontains=query).order_by('-birth_year')

class FilterCivilState(ListView):
    model = Census
    template_name = 'filterCensus.html'
    context_object_name = 'census'

    def get_queryset(self):
        query = self.request.GET.get('j')
        return Census.objects.filter(civil_state__icontains=query).order_by('-civil_state')

def import_xslx(request):

    if request.method == 'POST':
        census_resource = CensusResource()
        dataset = Dataset()
        new_census = request.FILES['myfile']

        if not new_census.name.endswith('xlsx'):
            messages.info(request, 'Error en el formato, debe ser .xslx')
            return render(request, 'import.html')

        data = dataset.load(new_census.read(),format='xlsx')

        for d in data:
            value = Census(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[8],
                    data[9],
                    data[10],
                    data[11]
                    )
            value.save()

    return render(request, 'import.html')

class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})



class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

def createCensus(request): 
    if request.method == 'GET':
        return render(request, 'census_create.html',{'form': CreationCensusForm})
    else: 
        if request.method == 'POST':
            try: 
                census = Census.objects.create(voting_id = request.POST['voting_id'],voter_id = request.POST['voter_id'],
                name = request.POST['name'],surname= request.POST['surname'],city = request.POST['city'],region = request.POST['region'],
                gender = request.POST['gender'],birth_year = request.POST['birth_year'],civil_state = request.POST['civil_state'],has_job = request.POST['has_job'])
                census.save()
                return render(request,'census_succeed.html',{'census':census})
                
            except: 
                return render(request,'census_create.html',{'form': CreationCensusForm, "error": 'Census already exist'})
        return  render(request,'census_create.html',{'form': CreationCensusForm})
