import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *


class CandidatFilter(django_filters.FilterSet):
    release_year = NumberFilter(field_name='date_de_dossier', lookup_expr='year')
    nom = CharFilter(field_name='nom', lookup_expr='icontains')
    prenom = CharFilter(field_name='prenom', lookup_expr='icontains')
    class Meta:
        model = Candidat
        fields = ['id', 'nom', 'prenom', 'wilaya', 'date_de_dossier']
        exclude = ['date_de_dossier']


class UserFilter(django_filters.FilterSet):

    email = CharFilter(field_name='email', lookup_expr='icontains')
    username = CharFilter(field_name='username', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class CentreExamenFilter(django_filters.FilterSet):



    nom = CharFilter(field_name='nom', lookup_expr='icontains')
    class Meta:
        model = CentreExamen
        fields = ['id', 'nom', 'wilaya']



class AutoEcoleFilter(django_filters.FilterSet):



    gérant = CharFilter(field_name='gérant', lookup_expr='icontains')

    class Meta:
        model = AutoEcole
        fields = ['id', 'gérant', 'wilaya']


class ExaminateurFilter(django_filters.FilterSet):
    nom = CharFilter(field_name='nom', lookup_expr='icontains')
    class Meta:

        model = Examinateur
        fields = ['id', 'nom', 'wilaya']





