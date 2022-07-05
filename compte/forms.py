from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import *
from django import forms
from django.contrib.auth.models import User


class DwsrCreationForm(forms.ModelForm):
    class Meta:
        model = Dwsr
        fields = ['name', 'wilaya']


class DwsrUpdateForm(forms.ModelForm):
    class Meta:
        model = Dwsr
        fields = ['name', 'wilaya']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}),
        }


class CreateUserForm(UserCreationForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class DateInput(forms.DateInput):
    input_type = 'date'

class CreateCandidatForm(forms.ModelForm):

    class Meta:
        model = Candidat
        fields = ['nin', 'nom', 'prenom', 'adresse', 'auto_école', 'categorie_du_permis', 'date_de_naissance', 'Group_sanguin', 'date_reussite', 'code_postal', 'wilaya', 'commune', 'age']

        widgets = {
            'nin': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Entrer le numéro de la carte nationale'}),
            'nom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer le nom du candidat'}),
            'prenom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer le prénom du candidat'}),
            'adresse':  forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer l\'adresse de résidence du candidat'}),
            'auto_école': forms.Select(attrs={'class': 'input', 'placeholder': 'Entrer le nom du auto-école'}),
            'categorie_du_permis': forms.Select(attrs={'class': 'input'}),
            'date_de_naissance': DateInput(attrs={'class': 'input', 'id': 'birthDate'}),
            'Group_sanguin': forms.Select(attrs={'class': 'input'}),
            'date_reussite': DateInput(attrs={'class': 'input'}),
            'age': forms.NumberInput(attrs={'class': 'input', 'id': 'calculateAge'}),
            }
        


class EpreuveResultForm(forms.ModelForm):

    class Meta:
        model = Epreuve
        fields = ['résultat', 'Examinateur']

        widgets = {
            'résultat': forms.Select(attrs={'class': 'form-control'}),
            'Examinateur': forms.Select(attrs={'class': 'form-control'}),
        }


class UpdateCandidatForm(forms.ModelForm):
    class Meta:

        model = Candidat
        fields = ['nin', 'nom', 'prenom', 'adresse', 'auto_école', 'categorie_du_permis', 'date_de_naissance', 'Group_sanguin', 'date_reussite', 'code_postal', 'wilaya', 'commune', 'age', 'réussit']

        widgets = {
            'nin': forms.NumberInput(attrs={'class': 'input', 'placeholder': 'Entrer le numéro de la carte nationale'}),
            'nom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer le nom du candidat'}),
            'prenom': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer le prénom du candidat'}),
            'adresse':  forms.TextInput(attrs={'class': 'input', 'placeholder': 'Entrer l\'adresse de résidence du candidat'}),
            'auto_école': forms.Select(attrs={'class': 'input', 'placeholder': 'Entrer le nom du auto-école'}),
            'categorie_du_permis': forms.Select(attrs={'class': 'input'}),
            'date_de_naissance': DateInput(attrs={'class': 'input', 'id': 'birthDate'}),
            'Group_sanguin': forms.Select(attrs={'class': 'input'}),
            'date_reussite': DateInput(attrs={'class': 'input'}),
            'age': forms.NumberInput(attrs={'class': 'input', 'id': 'calculateAge'}),
        }



class UpdateUserForm(forms.ModelForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']




class CentreExamenForm(forms.ModelForm):
    class Meta:
        model = CentreExamen
        fields = '__all__'
        exclude = ['user']


        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer le nom du centre'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer l\'adresse du centre'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}),
            'commune': forms.Select(attrs={'class': 'form-control', 'id': 'commune'}),
            'nbrPlace': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrer le nombre de place dans ce centre'}),
            'statut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer le statut du centre'}),
            'Numéro_agrément': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrer le numéro d\'agrément'}),
        }


class UpdateCentreExamenForm(forms.ModelForm):

    class Meta:

        model = CentreExamen
        fields = '__all__'
        exclude = ['user']


        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}),
            'commune': forms.Select(attrs={'class': 'form-control', 'id': 'commune'}),
            'nbrPlace': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.TextInput(attrs={'class': 'form-control'}),
            'Numéro_agrément': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AutoEcoleForm(forms.ModelForm):
    class Meta:

        model = AutoEcole
        fields = ['gérant', 'wilaya', 'adresse']

        widgets = {
            'gérant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer le nom du gérant'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrer l\'adresse de l\'auto école'}),
        }


class UpdateAutoEcoleForm(forms.ModelForm):
    class Meta:
        model = AutoEcole
        fields = '__all__'


        widgets = {
            'gérant': forms.TextInput(attrs={'class': 'form-control'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'dwsr': forms.Select(attrs={'class': 'form-control'}),
        }



class ExaminateurForm(forms.ModelForm):

    class Meta:

        model = Examinateur
        fields = '__all__'

        widgets = {
            'centre_examen': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}), 
        }



class UpdateExaminateurForm(forms.ModelForm):
    class Meta:
        model = Examinateur
        fields = '__all__'
        widgets = {
            'centre_examen': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'wilaya': forms.Select(attrs={'class': 'form-control', 'id': 'wilaya'}), 
        }



class PasswordChangingForm(PasswordChangeForm):

    old_password = forms.CharField(label='Ancien mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(label='le nouveau mot de passe',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(label='Confirmer le nouveau mot de passe',max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))


    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']



class TimeInput(forms.TimeInput):
    input_type = 'time'



class SessionForm(forms.ModelForm):
    class Meta:

        model = Session
        fields = '__all__'

        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'nom': forms.Select(attrs={'class': 'form-control'}),
            'heureDebut': TimeInput(attrs={'class': 'form-control'}),
            'heureFin': TimeInput(attrs={'class': 'form-control'}),
            # 'centre_examen': forms.Select(attrs={'class': 'form-control'}),
        }
        