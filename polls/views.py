from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
from .dataService import *
# Create your views here.

def result(request,pk):
    """
    :param request:
    :param pk:
    :return:
    """
    if request.method == "POST":
        query_model = Inter.objects.filter(id=pk)[0]
        print(query_model)
        params_card = request.POST.get('identityCard')
        params_mobile = request.POST.get('mobile')
        params_channel = request.POST.get('productChannel')
        ds = DataService(query_model.supplier,query_model.interface,params_card,phone=params_mobile,productChannel=params_channel)
        model_result = ds.get_data()
        rely_list = query_model.rely.all()
        result = {query_model.interface:model_result}
        for i in rely_list:
            ds = DataService(i.supplier, i.interface, params_card, phone=params_mobile,
                             productChannel=params_channel)
            result[i.interface]=ds.get_data()
        return JsonResponse(result)


def select(request):
    model_set = Inter.objects.filter(is_model=1)
    return render(request,'index.html',{'models':model_set})

def params(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('interface')
        model = Inter.objects.filter(interface=name)[0]
        param = model.inter.all()
        print(param)
    return render(request, 'param.html',{'params':param,'id':model.id})