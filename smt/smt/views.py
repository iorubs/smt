from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
import ast
import commands
from django.http import JsonResponse

class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

def bleuScoreView(request):
    """
    Calculate and return bleu score for input in request.
    """
    data = json.loads(request.body)
    user_input = data['input']
    user_output = data['output']

    #claculate score here

    return HttpResponse("some score like 2.555")

def meteorScoreView(request):
    """
    Calculate and return meteor score for input in request.
    """
    data = json.loads(request.body)
    user_input = data['input']
    user_output = data['output']

    #claculate score here

    return HttpResponse("some score like 5.222")

def nistScoreView(request):
    """
    Calculate and return nist score for input in request.
    """
    data = json.loads(request.body)
    user_input = data['input']
    user_output = data['output']

    #claculate score here

    return HttpResponse("some score like 1.111")

def translateView(request):
    """
    curl result
    """
    data = json.loads(request.body)
    status, output = commands.getstatusoutput('echo "' + data['input'] + '" > tmp.txt')
    request = 'curl -XPUT -F name=@tmp.txt localhost:5000/upload | python -m json.tool'
    status, output = commands.getstatusoutput(request)
    data = output.split('{')
    status, output = commands.getstatusoutput('rm -rf tmp.txt')

    return JsonResponse(json.loads('{' + data[1]))

