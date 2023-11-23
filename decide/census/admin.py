from django.contrib import admin
from .models import Census
from import_export.admin import ImportExportModelAdmin

@admin.register(Census)
class CensusAdmin(ImportExportModelAdmin):
    list_display = ('voting_id','voter_id','name','surname',
                    'city', 'region','gender','birth_year',
                    'civil_state','has_job')
    list_filter = ('voting_id',)

    search_fields = ('voter_id',)