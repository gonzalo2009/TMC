from django.shortcuts import render
from django.http import HttpResponse   
import requests
from django.utils import timezone
from datetime import timedelta, date, datetime

def index(request):
    date_now = timezone.now()
    max_date = datetime(year = date_now.year, month = date_now.month, day = date_now.day).strftime("%Y-%m-%d")
    if request.method == 'POST':

        if request.POST['UF']!='' and request.POST['dias']!='' and request.POST['UF']!='fecha':
            year=request.POST['fecha'][:4]
            month=request.POST['fecha'][5:7]
            response = requests.get( 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/' + year +'/'+ month +'?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json')
            n=None
            
            dias = int(request.POST['dias'])
            UF = int(request.POST['UF'])
            if dias < 90 and UF <= 5000:
                n=26
            elif  dias < 90 and UF > 5000:
                n=25
            elif  dias >= 90 and UF <= 50:
                n=45
            elif  dias >= 90 and UF <= 200 and UF > 50:
                n=44
            elif  dias >= 90 and UF <= 5000 and UF > 200:
                n=35

            
            j=None

            for i in range(len(response.json()['TMCs'])):
                if int(response.json()['TMCs'][i]['Tipo'])==n:
                    j=i
                    i+=1
        

            context={'max_date': max_date,  'TMC': response.json()['TMCs'][j]['Valor']}
            return render(request, "TMC/index.html", context)
        else:
            context={'max_date': max_date,'message': 'Faltan campos por completar'}
            return render(request, "TMC/index.html", context)
    else:
        response = requests.get( 'https://api.sbif.cl/api-sbifv3/recursos_api/tmc/2011/11?apikey=9c84db4d447c80c74961a72245371245cb7ac15f&formato=json')

        context={'max_date': max_date}
        return render(request, "TMC/index.html", context)
       