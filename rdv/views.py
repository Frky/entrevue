# from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# 
# from django.template import RequestContext
# from django.core import serializers
# from django.utils import simplejson
# from django.core.exceptions import ObjectDoesNotExist
# 
# from django.contrib import messages
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# from django.contrib.auth import login, logout

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from rdv.models import RDV
from rdv.forms import RDVForm



class IndexView(CreateView):
    template_name = "rdv/index.html"
    model = RDV
    fields = ['proposed_date', 'email_creator', 'place']

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        self.success_url = "/" + str(self.object.id)
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["rdv_list"] = RDV.objects.all()
        print context
        if self.object != None:
            context['new_rdv'] = self.object
            context['rdv_created'] = True
        return context


class RDVView(DetailView):
    template_name = "rdv/rdv_page.html"
    model = RDV
    slug_field = 'pk'
    slug_url_kwarg = 'rdvid'
    context_object_name = "rdv"

class CreatedView(TemplateView):
    template_name = "rdv/created.html"
