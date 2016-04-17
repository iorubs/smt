from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
import ast
import commands
import re 
from django.http import JsonResponse

class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


def eval(l1 , l2):
    return any(map(lambda v: v in l2, l1))


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


def bleuScoreView(request):
    """
    Calculate and return bleu score for input in request.
    """
    data = json.loads(request.body)
    user_input = data['input']
    user_output = data['output']

    #claculate score here
    #For input sentence
    tmpIn = []
    tmpIn.append(user_input.encode('ascii'))
    for i in tmpIn:
        i.split()

    inSen = []
    inSen = i.split()

    #For output sentence
    tmpOut = []
    tmpOut.append(user_output.encode('ascii'))
    for o in tmpOut:
        o.split()

    outSen = []
    outSen = o.split()
    
    if len(inSen) < 4: # return if we can't compute up to 4 n-grams
        return HttpResponse("Not enough input data to compute score")

    # N-grams for inputed sentance
    oneG   = find_ngrams(inSen, 1)
    twoG   = find_ngrams(inSen, 2)
    threeG = find_ngrams(inSen, 3)
    fourG  = find_ngrams(inSen, 4)

    # N-grams of the output sentance
    PerfoneG   = find_ngrams(outSen, 1)
    PerftwoG   = find_ngrams(outSen, 2)
    PerfthreeG = find_ngrams(outSen, 3)
    PerffourG  = find_ngrams(outSen, 4)

    count = 0
    for i in outSen:
        if(i in inSen):
            count += 1

    print "count : {}".format(count)
    if count == 0:
        if eval(fourG, PerffourG):
            return HttpResponse ("Perfect score: 100%")
        elif eval(threeG, PerfthreeG):
            return HttpResponse ("The score is: 95%")
        else:
            return HttpResponse ("The score is: 85%")

    if count == 1:
        if eval(fourG, PerffourG):
            return HttpResponse ("The score is approximately: 95%")
        elif eval(threeG, PerfthreeG):
            return HttpResponse ("The score is approximately: 85%")
        else:
            return HttpResponse ("The score is approximately: 80%")

    if count > 1 and count <= 4:
        if eval(fourG, PerffourG):
            return HttpResponse ("The score is approximately: 75%")
        elif eval(threeG, PerfthreeG):
            return HttpResponse ("The score is approximately: 55%")
        elif eval(twoG, PerftwoG):
            return HttpResponse ("The score is approximately: 45%")
        elif eval(oneG, PerfoneG):
            return HttpResponse ("The score is approximately: 25%")
        else:
            return HttpResponse ("The score is less than 20%")

    if count > 4 and len(inSen) < 15:   
        if eval(fourG, PerffourG):
            return HttpResponse ("The score is approximately: 35%")
        elif eval(threeG, PerfthreeG):
            return HttpResponse ("The score is approximately: 25%")
        elif eval(twoG, PerftwoG):
            return HttpResponse ("The score is approximately: 15%")
        elif eval(oneG, PerfoneG):
            return HttpResponse ("The score is approximately: 5%")
        else:
            return HttpResponse ("The score is less than 5%")

    if count > 4 and len(inSen) > 15:
        if eval(fourG, PerffourG):
            return HttpResponse ("Perfect score: 100%")
        elif eval(threeG, PerfthreeG):
            return HttpResponse ("The score is approximately: 75%")
        elif eval(twoG, PerftwoG):
            return HttpResponse ("The score is approximately: 50%")
        elif eval(oneG, PerfoneG):
            return HttpResponse ("The score is approximately: 25%")
        else:
            return HttpResponse ("The score is less than 25%")
    
    # Not needed but incase ;)
    return HttpResponse("System could not compute the score: Unknow reason")

def meteorScoreView(request):
    """
    Calculate and return meteor score for input in request.
    """
    data = json.loads(request.body)
    user_input = data['input']
    user_output = data['output']

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

