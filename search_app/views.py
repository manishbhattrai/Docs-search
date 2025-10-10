from django.shortcuts import render
from .forms import SearchForm
from .models import GoogleAPIKeys
from .utils import  search_query
import logging

# Create your views here.



logger = logging.getLogger(__name__)

def doc_search(request):

    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            try:
                results = search_query(query)

            except Exception as e:
                logging.error(f"Error: {e}")
                ##print(f"Error: {e}")
    
    else:
        form = SearchForm()
    
    context = {
        'form':form,
        'results':results,
    }
    return render(request, 'main.html',context=context)
