from django.urls import path, include
from . import views


urlpatterns = [
    path('create/', views.createCensus, name='create_census'),
    path('deatils<int:voting_id>', views.CensusDetail.as_view(), name='census_detail'),
    path('import/', views.import_xslx, name='import_xslx'),
]
