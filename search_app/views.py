from django.shortcuts import render
import requests
from django.conf import settings
from .forms import SearchForm

# Create your views here.



def doc_search(request):

    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            results = search_query(query)
    
    else:
        form = SearchForm()
    
    context = {
        'form':form,
        'results':results
    }
    return render(request, 'main.html',context=context)

def search_query(query, document_types=None):


    
    if document_types is None:
        document_types = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt']






    
    '''
      Building file type filter string using the list comprehension

      which makes list like for example = ['filetype:pdf', 'filetype:doc'] 

     and joining to create a single string for example : 'filetype:pdf OR filetype:doc OR filetype:docx'
      
        '''
    
    filetype_filter = ' OR '.join([f'filetype:{doc_type}' for doc_type in document_types])









    
    '''
    Combining the original query with the filetype_filter.

    Suppose the query is 'AI research paper' and the filetype_filter is 'filetype:pdf OR filetype:doc OR filetype:docx'. 

    The resulting filtered_query would be: 

    'AI research paper (filetype:pdf OR filetype:doc OR filetype:docx)'
    
    '''
    filtered_query = f"{query} ({filetype_filter})"



    
    api_url = f"https://www.googleapis.com/customsearch/v1?q={filtered_query}&key={settings.GOOGLE_API_KEY}&cx={settings.GOOGLE_CSE_ID}"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        search_results = response.json()
        return search_results.get('items', [])
    else:
        return []

    

