from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import *
from .forms import *
from .serializers import *
import requests


# Create your views here.

class DestCreateView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [AllowAny]


class DestDetails(generics.RetrieveAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestDelete(generics.DestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestSearchView(generics.ListAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_queryset(self):
        place_name = self.kwargs.get('place_name')
        return Destination.objects.filter(place_name__icontains=place_name)


def base(request):
    if request.method == 'POST':
        search = request.POST['search']

        api_url = f'http://127.0.0.1:8000/search/{search}/'

        try:
            response = requests.get(api_url)
            print(response.status_code)

            if response.status_code == 200:
                data = response.json()
            else:
                data = None

        except requests.RequestException as e:
            data = None

        return render(request, 'base.html', {'data': data})
    else:
        api_url = 'http://127.0.0.1:8000/create/'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                original_data = data

                paginator = Paginator(original_data, 6)
                page = request.GET.get('page', 1)

                try:
                    destination = paginator.page(page)

                except PageNotAnInteger:
                    destination = paginator.page(1)

                except(EmptyPage, InvalidPage):

                    destination = Paginator.page(paginator.num_pages)

                context = {
                    'original_data': original_data,
                    'destination': destination
                }
                return render(request, 'base.html', context)
            else:
                return render(request, 'base.html', {'error_message': f'Error: {response.status_code}'})

        except requests.RequestException as e:
            return render(request, 'base.html', {'error_message': f'Error:{str(e)}'})

    return render(request, 'base.html')


def create_destination(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/create/'
                data = form.cleaned_data
                print(data)

                response = requests.post(api_url, data=data, files={'image': request.FILES['image']})

                if response.status_code == 400:
                    messages.success(request, 'Destination creation successfull')
                    return redirect('/')
                else:
                    messages.error(request, f'Error{response.status_code}')

            except request.RequestException as e:
                messages.error(request, f'Error during API request {str(e)}')

        else:
            messages.error(request, 'invalid form')

    else:
        form = DestinationForm()

    return render(request, 'create-destination.html', {'form': form})


def update_detail(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        return render(request, 'update-destination.html', {'destination': data})


def update_destination(request, id):

    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        weather = request.POST.get('weather')
        location_state = request.POST.get('location_state')
        location_district = request.POST.get('location_district')
        link = request.POST.get('link')
        description = request.POST.get('description')

        print('Image url', request.FILES.get('image'))

        api_url = f' http://127.0.0.1:8000/update/{id}/'

        data = {
            'place_name': place_name,
            'weather': weather,
            'location_state': location_state,
            'location_district': location_district,
            'link': link,
            'description': description
        }

        files = {'image': request.FILES.get('image')}
        response = requests.put(api_url, data=data, files=files)
        if response.status_code == 200:
            messages.success(request, 'Destination updated successfully')
            return redirect('/')
        else:
            messages.error(request, f'Error submitting data to REST API : {response.status_code}')

    return render(request, 'update-destination.html')


def delete_destination(request, id):
    api_url = f' http://127.0.0.1:8000/delete/{id}'
    response = requests.delete(api_url)

    if response.status_code == 200:
        print(f'Item with id {id} has been deleted')

    else:
        print(f'Failed to delete item. Status code {response.status_code} ')

    return redirect('/')


def delete_page(request,id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return render(request, 'destination-delete.html',{'destination': data})


def fetch_destination(request,id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()

        return render(request, 'fetch-destination.html', {'destination': data})
    return render (request,'fetch-destination.html')
