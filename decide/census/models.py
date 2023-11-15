from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    #New stuff
    name = models.CharField(max_length=40, null=True)
    surname = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=40, null=True)
    region = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=10, null=True)
    birth_year = models.PositiveIntegerField(null=True)
    civil_state = models.CharField(max_length=10, null=True)
    has_job = models.BooleanField(default=False)

    class Meta:
        unique_together = (('voting_id','voter_id','name','surname',
                            'city', 'region','gender','birth_year',
                            'civil_state','has_job'),)
