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

from datetime import datetime

from rdv.models import RDV, Answer
from rdv.forms import RDVForm


class IndexView(CreateView):
    template_name = "rdv/index.html"
    model = RDV
    form_class = RDVForm
    fields = ['proposed_date', 'proposer', 'place']

    def post(self, request, *args, **kwargs):
        return super(IndexView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        self.success_url = "/" + str(self.object.id)
        return redirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["rdv_list"] = RDV.objects.all()
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

        # Get the name of the proposer
        if "answerer" in request.GET.keys():
            nickname = request.GET["answerer"]
        else:
            nickname = ""

        # Check if the answer is in the parameters
        if "ynanswer" not in request.GET.keys():
            # Manage error here 
            # TODO
            print "No ynanswer given."
            return self.render_to_response(context)

        if request.GET["ynanswer"] == 'y':
            # Create a yes answer object
            ans = Answer(value='y', answerer=nickname)
        elif request.GET["ynanswer"] == 'n':
            # Create a no answer object
            ans = Answer(value='n', answerer=nickname)
        else: 
            # idem
            # TODO
            print "Answer not y nor no."
            return self.render_to_response(context)


        ans.save()
        rdv.answer = ans
        rdv.save()

        # Get initial rdv
        initial_rdv = rdv
        while initial_rdv.initial_rdv != None:
            initial_rdv = initial_rdv.initial_rdv

        return redirect("/" + str(initial_rdv.id))


class ReproposeView(TemplateView):

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        new_rdv_form = RDVForm(request.GET)
        if new_rdv_form.is_valid():
            print "form valid"


        # Check if the rendez-vous id is in the parameters
        if "rdvid" not in request.GET.keys():
            # Manage error here 
            # TODO
            print "No rdvid given."
            return self.render_to_response(context)

        # Get initial proposition
        rdv = RDV.objects.get(id=request.GET['rdvid'])

        # Then we try to reach the last proposition
        curr_prop = rdv
        # While there is a previous proposition
        while len(curr_prop.counter_proposition.all()) > 0:
            # We take one step back
            curr_prop = curr_prop.counter_proposition.all()[0]
        
        # At this point, rdv is the initial proposition and curr_prop is the current one

        # Get the name of the proposer
        if "nickname" in request.GET.keys():
            nickname = request.GET["nickname"]
        else:
            nickname = ""

        # Creation of an answer for the current proposition
        ans = Answer(answerer=nickname, value='o')
        # Saving the answer
        ans.save()
        # Linking answer to the proposition
        curr_prop.answer = ans
        curr_prop.save()

        # NExt, we create the new proposition

        # Get the date string
#        date_str = request.GET["proposed_date"]
        # Create the date object
#        date = datetime.strptime(date_str, "%m/%d/%Y") 
        # Get the date
#        place = request.GET["place"]
        # Create the new rdv object linked to the previous proposition
        new_rdv = new_rdv_form.save(commit=False)
        print "Form: "
        print new_rdv_form
        print "place: "
        print new_rdv.place
        print "date: "
        print new_rdv.proposed_date
        print new_rdv.proposed_date
        new_rdv.initial_rdv = curr_prop
        new_rdv.save()
        
        # Redirect to the page of the initial proposition
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
        context["rdv"] = rdv 
        context["form"] = RDVForm() #notitle=True) #, instance=rdv)
        return self.render_to_response(context)

#    def get_context_data(self, *args, **kwargs):
#        context = super(RDVView, self).get_context_data(*args, **kwargs)
#        context.update({
#            'form': RDVForm(),
#        })
#        return context

    model = RDV
    slug_field = 'pk'
    slug_url_kwarg = 'rdvid'
    context_object_name = "rdv"


class CreatedView(TemplateView):
    template_name = "rdv/created.html"
