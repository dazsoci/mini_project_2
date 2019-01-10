from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse_lazy, reverse
from django.views import generic
from australian_weather_app.models import Observation
from australian_weather_app.forms import ObservationForm

from joblib import load
import pandas as pd
import datetime
import pickle
import os

# User management


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Home


def home(request):
    return render(request, 'home.html')

# Observation management


@login_required(login_url=reverse_lazy('login'))
def add_observation(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.observer = request.user
            observation.save()

            return HttpResponseRedirect(reverse('list_observations'))
    elif request.method == "GET":
        form = ObservationForm()

    context = {
        'form': form
    }
    return render(request, 'observations/add_observation.html', context)


@login_required(login_url=reverse_lazy('login'))
@ensure_csrf_cookie
def list_observations(request):
    observations = Observation.objects.order_by('-id')

    context = {
        'observations': observations
    }
    return render(request, 'observations/list_observations.html', context)


@login_required(login_url=reverse_lazy('login'))
def edit_observation(request, observation_id):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation_to_be_updated = Observation.objects.get(
                id=observation_id)
            new_observation = form.save(commit=False)

            for attr, value in new_observation.__dict__.items():
                if attr is not 'id' and attr is not 'observer_id':
                    setattr(observation_to_be_updated, attr, value)

            observation_to_be_updated.save()

            return HttpResponseRedirect('/weather/list_observations/')
    elif request.method == 'GET':
        observation = get_object_or_404(Observation, id=observation_id)

        form = ObservationForm(instance=observation)
        context = {
            'form': form
        }
        return render(request, 'observations/edit_observation.html', context)


@login_required(login_url=reverse_lazy('login'))
def delete_observation(request):
    observation_id = request.POST["observation_id"]
    Observation.objects.filter(id=observation_id).delete()

    return HttpResponseRedirect(reverse('list_observations'))


def get_season(d):
    if d.month >= 12 and d.month < 3:
        return 0
    elif d.month >= 3 and d.month < 6:
        return 1
    elif d.month >= 6 and d.month < 9:
        return 2
    else:
        return 3

# Prediction


@login_required(login_url=reverse_lazy('login'))
def predict_rainfall(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.observer = request.user
            
            file_path_base = os.path.join(
                os.path.dirname(__file__), 'ml_files')
            ml_model = load(os.path.join(file_path_base, 'ml_model.joblib'))

            transformed_observation = {
                'Date': observation.date,
                'Location': observation.location,
                'MinTemp': observation.min_temp,
                'MaxTemp': observation.max_temp,
                'Rainfall': observation.rainfall,
                'WindGustDir': observation.wind_gust_dir,
                'WindGustSpeed': observation.wind_gust_speed,
                'WindDir9am': observation.wind_dir_9am,
                'WindDir3pm': observation.wind_dir_3pm,
                'WindSpeed9am': observation.wind_speed_9am,
                'WindSpeed3pm': observation.wind_speed_3pm,
                'Humidity9am': observation.humidity_9am,
                'Humidity3pm': observation.humidity_3pm,
                'Temp9am': observation.temp_9am,
                'Temp3pm': observation.temp_3pm,
                'RainToday': observation.rain_today
            }

            transformed_observation['Season'] = get_season(transformed_observation['Date'])
            df = pd.DataFrame(data=transformed_observation, index=[0])
            df['RainToday'].replace({False: 0, True: 1}, inplace=True)

            ordered_df = df[['Season', 'Location', 'WindGustDir',
                             'WindDir9am', 'WindDir3pm', 'RainToday',
                             'Humidity3pm', 'Humidity9am', 'MaxTemp',
                             'MinTemp', 'Rainfall', 'Temp3pm',
                             'Temp9am', 'WindGustSpeed', 'WindSpeed3pm',
                             'WindSpeed9am']].values

            prediction = ml_model.predict(ordered_df)

            context = {
                'observation': observation,
                'result': prediction
            }
            return render(request, "prediction/result.html", context)
    elif request.method == "GET":
        form = ObservationForm()

        context = {
            'form': form
        }
        return render(request, 'prediction/predict_rainfall.html', context)