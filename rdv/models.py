from django.db import models

from rdv.random_primary import RandomPrimaryIdModel



class Answer(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class Yes(Answer):
    None


class No(Answer):
    None


class Other(Answer):
    None


class RDV(RandomPrimaryIdModel):
    creation = models.DateTimeField(auto_now_add=True)
    proposed_date = models.DateTimeField(auto_now_add=False, blank=False, null=False)
    initial_rdv = models.ForeignKey('rdv.RDV', related_name='counter_proposition', blank=True, null=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    email_creator = models.EmailField(blank=True, null=True)
    place = models.CharField(max_length=256, blank=True, null=True)
