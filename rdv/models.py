#-*- coding: utf-8 -*-

from django.db import models

from rdv.random_primary import RandomPrimaryIdModel


class Answer(models.Model):
    YES = 'y'
    NO = 'n'
    OTHER = 'o'

    ANS_CHOICES = ( 
            (YES, "Yes"), 
            (NO, "No"), 
            (OTHER, "Other"),
        )

    date = models.DateTimeField(auto_now_add=True)
    value = models.CharField(max_length=1, 
                            choices=ANS_CHOICES)
    answerer = models.CharField(max_length=256, blank=True, null=True)


class RDV(RandomPrimaryIdModel):
    creation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256, blank=True, null=True, verbose_name='Titre')
    proposer = models.CharField(max_length=256, blank=True, null=True, verbose_name='Nom')
    proposed_date = models.DateTimeField(auto_now_add=False, blank=False, null=False, verbose_name='Date choisie (obligatoire)')
    initial_rdv = models.ForeignKey('rdv.RDV', related_name='counter_proposition', blank=True, null=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    email_creator = models.EmailField(blank=True, null=True, verbose_name='Email pour être averti des réponses (sera masqué)')
    email_share = models.EmailField(blank=True, null=True, verbose_name='Email pour partager le rendez-vous (sera masqué)')
    place = models.CharField(max_length=256, blank=True, null=True, verbose_name='Lieu')
