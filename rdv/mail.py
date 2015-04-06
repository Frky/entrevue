#-*- coding: utf-8 -*-

from django.core.mail import send_mail
from smtplib import SMTPRecipientsRefused

EMAIL_FROM = 'rdv@udtq.fr'
RDV_URL_PREFIX = 'http://rdv.udtq.fr/'

def mail_rdv_created(rdv, dest):
    try:
        send_mail(
                '[RDV] ' + RDV_URL_PREFIX + rdv.id, 
                u"Votre rendez-vous a été créé. Vous serez informé des réponses par email.", 
                EMAIL_FROM,
                dest, 
                fail_silently=False
            )
    except SMTPRecipientsRefused:
        #TODO notify user that failure
        pass

def mail_rdv_edited(rdv, dest):
    try:
        send_mail(
                '[RDV] ' + RDV_URL_PREFIX + rdv.id, 
                u"Une contre-proposition a été faite à votre rendez-vous: " + RDV_URL_PREFIX + str(rdv.id),
                EMAIL_FROM,
                dest, 
                fail_silently=False
            )
    except SMTPRecipientsRefused:
        #TODO notify user that failure
        pass

def mail_rdv_answered(rdv, dest):
    try:
        send_mail(
                '[RDV] ' + RDV_URL_PREFIX + rdv.id, 
                u"Une réponse a été fournie à votre rendez-vous: " + RDV_URL_PREFIX + str(rdv.id),
                EMAIL_FROM,
                dest, 
                fail_silently=False
            )
    except SMTPRecipientsRefused:
        #TODO notify user that failure
        pass
