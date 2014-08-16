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

from datetime import datetime

from rdv.models import RDV, Answer
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


class AnswerView(TemplateView):
    template_name = "rdv/answer.html"
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # Check if the rendez-vous id is in the parameters
        if "rdvid" not in request.GET.keys():
            # Manage error here 
            # TODO
            print "No rdvid given."
            return self.render_to_response(context)

        # Get rendez-vous object
        rdv = RDV.objects.get(id=request.GET["rdvid"])

        # Check if the answer is in the parameters
        if "ynanswer" not in request.GET.keys():
            # Manage error here 
            # TODO
            print "No ynanswer given."
            return self.render_to_response(context)

        if request.GET["ynanswer"] == 'y':
            # Create a yes answer object
            ans = Answer(value='y')
        elif request.GET["ynanswer"] == 'n':
            # Create a no answer object
            ans = Answer(value='n')
        else: 
            # idem
            # TODO
            print "Answer not y nor no."
            return self.render_to_response(context)


        print "OK"
        ans.save()
        rdv.answer = ans
        rdv.save()
        print rdv.answer

        return redirect("/" + str(rdv.id))


class ReproposeView(TemplateView):

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        # Check if the rendez-vous id is in the parameters
        if "rdvid" not in request.GET.keys():
            # Manage error here 
            # TODO
            print "No rdvid given."
            return self.render_to_response(context)

        print "RID"
        print request.GET['rdvid']
        rdv = RDV.objects.get(id=request.GET['rdvid'])
        prev_prop = rdv
        print "plop"
        print rdv.proposed_date
        print prev_prop.counter_proposition.all()
        while len(prev_prop.counter_proposition.all()) > 0:
            print "New prop"
            prev_prop = prev_prop.counter_proposition.all()[0]
        
        if "nickname" in request.GET.keys():
            nickname = request.GET["nickname"]
        else:
            nickname = ""
        ans = Answer(answerer=nickname, value='o')
        ans.save()
        prev_prop.answer = ans
        prev_prop.save()

        date_str = request.GET["proposed_date"]
        date = datetime.strptime(date_str, "%m/%d/%Y") 
        place = request.GET["place"]
        new_rdv = RDV(initial_rdv=prev_prop, 
                proposer=nickname, 
                proposed_date=date, place=place)
        new_rdv.save()
        
        return redirect("/" + str(rdv.id))


class RDVView(TemplateView):
    template_name = "rdv/rdv_page.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rdvid = self.kwargs['rdvid']
        context["rdvid"] = rdvid
        rdv = RDV.objects.get(id=rdvid)
        context["previous_rdv"] = list()
        while len(rdv.counter_proposition.all()) > 0:
            context["previous_rdv"].append(rdv)
            rdv = rdv.counter_proposition.all()[0]
            print rdv
        context["rdv"] = rdv 
        return self.render_to_response(context)

    model = RDV
    slug_field = 'pk'
    slug_url_kwarg = 'rdvid'
    context_object_name = "rdv"


class CreatedView(TemplateView):
    template_name = "rdv/created.html"
