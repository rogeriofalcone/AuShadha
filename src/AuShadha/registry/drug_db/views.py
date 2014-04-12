#################################################################################
# Project      : AuShadha
# Description  : Views for Drug DB
# Author       : Dr.Easwar T.R 
# Date         : 04-10-2013
# License      : GNU-GPL Version 3, See LICENSE.txt 
################################################################################

import os
import sys
from datetime import datetime, date, time

# General Django Imports----------------------------------

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Application Specific Model Imports-----------------------
import AuShadha.settings as settings
from AuShadha.settings import APP_ROOT_URL
from AuShadha.apps.ui.data.json import ModelInstanceJson
from AuShadha.apps.ui.data.summary import ModelInstanceSummary
from AuShadha.utilities.forms import aumodelformerrorformatter_factory
from AuShadha.apps.ui.ui import ui as UI
from AuShadha.core.serializers.data_grid import generate_json_for_datagrid
from AuShadha.utilities.forms import aumodelformerrorformatter_factory


from .models import FDADrugs
 
# Views start here -----------------------------------------



@login_required
def fda_drug_db_json_all_drugs(request):

  if request.method == 'GET' and request.is_ajax():

     range_to_query = request.META.get('HTTP_X_RANGE', None) 
     print("Received request to get range: ", range_to_query)
     all_drugs = FDADrugs.objects.all()

     if range_to_query is not None:
        query_index = range_to_query.split('=')[1].split('-')
        query_start = int(query_index[0])
        query_end = int(query_index[1])
        print("Querying ", query_start, " to Query end ", query_end)
        drugs = all_drugs[query_start:query_end]

     else:
        drugs = all_drugs[:len(drugs)-1]

     if all_drugs is not None:
        data = []
        for drug in drugs:
           json_data = ModelInstanceJson(drug).return_data()
           data.append(json_data)
     else:
        data = {}
     json_output = simplejson.dumps(data)
     response = HttpResponse(json_output, content_type="application/json")
     response['Content-Range'] = 'items'+str(query_start)+'-'+str(query_end)+'/'+ str( len(all_drugs))
     return response
  else:
    raise Http404("Bad Request Method")

@login_required
def fda_drug_summary(request,drug_id):
  if request.method == 'GET' and request.is_ajax():
    user = request.user
    if drug_id:
        drug_id = int(drug_id)
    else:
        drug_id = int(request.GET.get('drug_id') )
    try:
        drug_obj = FDADrugs.objects.get(pk = drug_id)
        var = ModelInstanceSummary(drug_obj).variable
        var['user'] = user
        variable = RequestContext(request,var)
        return render_to_response('registry/drug_db/fda_drugs/summary.html', variable)
    except(AttributeError, ValueError, TypeError, NameError):
        raise Http404("ERROR ! Bad Request Parameters")
    except(FDADrugs.DoesNotExist):
        raise Http404("ERROR! FDA Drug Does not exist")

  else:
      raise Http404("Bad Request method")


@login_required
def fda_drug_db_json_for_a_drug(request,drug_id):
  pass

@login_required
def fda_drug_db_search(request):
  pass

@login_required
def fda_drug_db_advanced_search(request,search_for):
  pass



