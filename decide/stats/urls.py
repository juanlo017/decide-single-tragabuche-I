from django.urls import path
from . import views

urlpatterns = [
    path('general/', views.general_stats),
    #path('<int:voting_id>/', StatsView.as_view()),
]
