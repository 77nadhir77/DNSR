from django.db import models


from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime



 

class Dnsr(models.Model):

    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name


class Dwsr(models.Model):

    dnsr = models.ForeignKey(Dnsr, null=True, blank=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
   

    def __str__(self):
        return self.name


class AutoEcole(models.Model):
    gérant = models.CharField(max_length=100, null=True, blank=True,)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)   
    dwsr = models.ForeignKey(Dwsr, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.gérant


class CategoriePermi(models.Model):

    nom = models.CharField(null=True, blank=True, max_length=3)
    discription = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nom


class Candidat(models.Model):

    x = [
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('AB-', 'AB-'),
        ('AB+', 'AB+'),
    ]


    dwsr = models.ForeignKey(Dwsr, null=True, blank=True, on_delete=models.CASCADE)
    user=models.OneToOneField(User,blank=True, null=True, on_delete=models.SET_NULL)
    nin = models.IntegerField(verbose_name=("Numéro de carte d'Identitée Nationale"))
    nom = models.CharField(verbose_name=("Nom"), max_length=100)
    prenom = models.CharField(verbose_name=("Prénom"), max_length=100)
    adresse = models.CharField(verbose_name=("Adresse"), max_length=200, null=True, blank=True)  
    auto_école = models.ForeignKey(AutoEcole, null=True, blank=True, on_delete=models.CASCADE) 
    categorie_du_permis = models.ForeignKey(CategoriePermi, null=True, blank=True, on_delete=models.PROTECT)
    code_postal = models.IntegerField(null=True, blank=True)
    wilaya = models.CharField(max_length=50, default='Alger')
    commune = models.CharField(max_length=100, default='Sidi Mhamed')
    date_de_naissance = models.DateField(null=True, blank=True)
    date_de_dossier = models.DateTimeField(default=datetime.now())
    Group_sanguin = models.CharField(max_length=3, default='A+', choices=x)
    date_reussite = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    réussit = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.nom + ' ' + self.prenom



class CentreExamen(models.Model):

    
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    nom = models.CharField(max_length=200, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)  
    wilaya = models.CharField(max_length=50, default='Alger')
    commune = models.CharField(max_length=100, default='Sidi Mhamed')
    nbrPlace = models.IntegerField(null=True, blank=True)
    statut = models.CharField(max_length=50, null=True, blank=True)
    Numéro_agrément = models.IntegerField(null=True, blank=True)


    def __str__(self):

        return self.nom + '(' + self.wilaya + ')'
    

class Session(models.Model):
    x = [
        ('Code','Code'),
        ('Manoeuvre','Manoeuvre'),
        ('Conduite','Conduite')
    ]
    date = models.DateField(null=True, blank=True)
    nom = models.CharField(max_length=100, default='session de epreuve', choices=x)
    heureDebut = models.TimeField(null=True, blank=True)
    heureFin = models.TimeField(null=True, blank=True)
    candidat = models.ForeignKey(Candidat,null=True,blank=True, on_delete=models.SET_NULL)
    centre_examen = models.ForeignKey(CentreExamen, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + " " + str(self.heureDebut) + '-' + str(self.heureFin) + self.nom


class Examinateur(models.Model):
    centre_examen = models.ForeignKey(CentreExamen, null=True, blank=True, on_delete=models.PROTECT)
    nom = models.CharField(max_length=200, null=True, blank=True)
    wilaya = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):

        return self.nom





class Epreuve(models.Model):
    x = [
        ('Code','Code'),
        ('Manoeuvre','Manoeuvre'),
        ('Conduite','Conduite')
    ]
    y = [
        ('Reçu','Reçu'),
        ('Echoué','Echoué'),
    ]
    nom = models.CharField(max_length=100, default='Code', choices=x)
    résultat = models.CharField(max_length=100,null=True, blank=True, choices=y)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    candidat = models.ManyToManyField(Candidat)
    Examinateur = models.ForeignKey(Examinateur,null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.session.date)+ ' ' +  str(self.session.heureDebut) +' , Epreuve: '+ self.nom 




    