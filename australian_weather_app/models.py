from django.db import models
from django.contrib.auth.models import User

locations = (('0', 'Adelaide'), ('1', 'Albury'), ('2', 'AliceSprings'), ('3', 'BadgerysCreek'), ('4', 'Ballarat'),
             ('5', 'Bendigo'), ('6', 'Brisbane'), ('7', 'Cairns'), ('8', 'Canberra'), ('9', 'Cobar'),
             ('10', 'CoffsHarbour'), ('11', 'Dartmoor'), ('12', 'Darwin'), ('13', 'GoldCoast'), ('14', 'Hobart'),
             ('15', 'Katherine'), ('16', 'Launceston'), ('17', 'Melbourne'), ('18', 'MelbourneAirport'), ('19', 'Mildura'),
             ('20', 'Moree'), ('21', 'MountGambier'), ('22', 'MountGinini'), ('23', 'Nhil'), ('24', 'NorahHead'),
             ('25', 'NorfolkIsland'), ('26', 'Nuriootpa'), ('27', 'PearceRAAF'), ('28', 'Penrith'), ('29', 'Perth'),
             ('30', 'PerthAirport'), ('31', 'Portland'), ('32', 'Richmond'), ('33', 'Sale'), ('34', 'SalmonGums'),
             ('35', 'Sydney'), ('36', 'SydneyAirport'), ('37', 'Townsville'), ('38', 'Tuggeranong'), ('39', 'Uluru'),
             ('40', 'WaggaWagga'), ('41', 'Walpole'), ('42', 'Watsonia'), ('43', 'Williamtown'), ('44', 'Witchcliffe'),
             ('45', 'Wollongong'), ('46', 'Woomera'))


winddirs = (('0', 'E'), ('1', 'ENE'), ('2' ,'ESE'), ('3', 'N'), ('4', 'NE'),
            ('5', 'NNE'), ('6', 'NNW'), ('7', 'NW'), ('8', 'S'), ('9', 'SE'),
            ('10', 'SSE'), ('11', 'SSW'), ('12', 'SW'), ('13', 'W'), ('14', 'WNW'),
            ('15', 'WSW'))

# Create your models here.

class Observation(models.Model):
    observer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=40, choices=locations)
    min_temp = models.FloatField(blank=False)
    max_temp = models.FloatField(blank=False)
    rainfall = models.FloatField(blank=False)
    wind_gust_dir = models.CharField(max_length=10, blank=False, choices=winddirs)
    wind_gust_speed = models.FloatField(blank=False)
    wind_dir_9am = models.CharField(max_length=10, blank=False, choices=winddirs)
    wind_dir_3pm = models.CharField(max_length=10, blank=False, choices=winddirs)
    wind_speed_9am = models.FloatField(blank=False)
    wind_speed_3pm = models.FloatField(blank=False)
    humidity_9am = models.FloatField(blank=False)
    humidity_3pm = models.FloatField(blank=False)
    temp_9am = models.FloatField(blank=False)
    temp_3pm = models.FloatField(blank=False)
    rain_today = models.BooleanField(blank=False)