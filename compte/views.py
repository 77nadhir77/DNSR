from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import * 
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from .filters import *
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView


# Create your views here.



@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def create_dwsr(request):

    if request.method == 'POST':
        name = request.POST.get('nom')
        wilaya = request.POST.get('wilaya')

        data = Dwsr(name=name, wilaya=wilaya)
        dwsr = data.save()

        return redirect('liste_des_dwsr')

    return render(request, 'create_dwsr.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_candidat(request):

    form = CreateCandidatForm()

    if request.method == 'POST':
        form = CreateCandidatForm(request.POST)
        wilaya = request.POST.get('wilaya')
        commune = request.POST.get('commune')
        code_postal = request.POST.get('code_postal')



        if form.is_valid():
            candidat = form.save()
            candidat.wilaya = wilaya
            candidat.commune = commune
            candidat.code_postal = code_postal
            return redirect('liste_des_candidat')




    context = {
        'form': form,
    }
    return render(request, 'create_candidat.html', context)

@allowed_users(allowed_roles=['DWSR'])
@login_required(login_url='login')
def update_candidat(request, id):
    candidat = Candidat.objects.get(id=id)
    form = None
    if request.method == 'POST':
        form = UpdateCandidatForm(request.POST, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('liste_des_candidat')
    else:
        form = UpdateCandidatForm(instance=candidat)
    
    context = {
        'form': form
    }
    
    return render(request, 'update_candidat.html', context)

@allowed_users(allowed_roles=['DWSR'])
@login_required(login_url='login')
def delete_candidat(request, id):
    candidat = Candidat.objects.get(id=id)
    if request.method == 'POST':
        candidat.delete()
        redirect('liste_des_candidat')
    
    context = {
        'candidat': candidat
    }
    return render(request, 'delete_candidat.html', context)



@allowed_users(allowed_roles=['DWSR', 'DNSR'])
@login_required(login_url='login')
def liste_des_candidat(request):

    candidats = Candidat.objects.all()
    myFilter = CandidatFilter(request.GET, queryset = candidats)
    candidats =  myFilter.qs

    context = {
        'candidats': candidats,
        'myFilter': myFilter,
    }
    return render(request, 'liste_des_candidat.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_candidat_user(request, id):


    form = CreateUserForm()
    if request.method == 'POST':
        form =  CreateUserForm(request.POST) 
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='CANDIDAT')
            user.groups.add(group)
            candidat = Candidat.objects.all().filter(id=id).update(user=user, dwsr=request.user.dwsr)
            return redirect('liste_des_candidat')

    context = {
        'form': form
    }

    return render(request, 'create_candidat_user.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def liste_des_dwsr(request):
    context = {
        'dwsrs': Dwsr.objects.all()
    }

    return render(request, 'liste_des_dwsr.html', context)



@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')




@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.success(request, 'Utilisateur ou mot de passe incorrect')
                return redirect('login')
            else:
                login(request, user)
                return redirect('index')
               

    else:
        return render(request, 'login.html')



def logoutPage(request):

    logout(request)
    return redirect('login')




@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def create_dwsr_user(request, id):
    
    
    form = CreateUserForm()
    if request.method == 'POST':
        form =  CreateUserForm(request.POST) 
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='DWSR')
            user.groups.add(group)
            dwsr = Dwsr.objects.all().filter(id=id).update(user=user, dnsr=request.user.dnsr)
            return redirect('liste_des_dwsr')

    
    context = {
        'form': form

    }


    
    return render(request, 'create_dwsr_user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def liste_des_user_dnsr(request):
    groups = Group.objects.get(name='DNSR')
    users = User.objects.all().filter(groups = groups)

    Filter = UserFilter(request.GET, queryset=users)
    users = Filter.qs
    context = {'users': users, 'Filter': Filter}

    return render(request, 'liste_des_user_dnsr.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def liste_des_user_dwsr(request):
    groups = Group.objects.get(name='DWSR')
    users = User.objects.all().filter(groups = groups)

    Filter = UserFilter(request.GET, queryset=users)
    users = Filter.qs
    context = {'users': users, 'Filter': Filter}

    return render(request, 'liste_des_user_dwsr.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def liste_des_user_centre(request):
    groups = Group.objects.get(name='CENTRE')
    users = User.objects.all().filter(groups = groups)

    Filter = UserFilter(request.GET, queryset=users)
    users = Filter.qs
    context = {'users': users, 'Filter': Filter}

    return render(request, 'liste_des_user_centre.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def liste_des_user_candidat(request):
    groups = Group.objects.get(name='CANDIDAT')
    users = User.objects.all().filter(groups = groups)

    Filter = UserFilter(request.GET, queryset=users)
    users = Filter.qs
    context = {'users': users, 'Filter': Filter}

    return render(request, 'liste_des_user_candidat.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def delete_user_dnsr(request, id):

    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_des_user_dnsr')
    
    context = {
        'user': user

    }
    return render(request, 'delete_user_dnsr.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def update_user_dnsr(request, id):

    form = None
    user = User.objects.get(id=id)


    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('liste_des_user_dnsr')
    else:

        form = UpdateUserForm(instance=user)



    context = {
        'form': form
    }


    return render(request, 'update_user_dnsr.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def delete_user_dwsr(request, id):

    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_des_user_dwsr')
    
    context = {
        'user': user

    }
    return render(request, 'delete_user_dwsr.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def update_user_dwsr(request, id):

    form = None
    user = User.objects.get(id=id)


    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('liste_des_user_dwsr')
    else:

        form = UpdateUserForm(instance=user)



    context = {
        'form': form
    }


    return render(request, 'update_user_dwsr.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def delete_user_centre(request, id):

    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_des_user_centre')
    
    context = {
        'user': user

    }
    return render(request, 'delete_user_centre.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def update_user_centre(request, id):

    form = None
    user = User.objects.get(id=id)


    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('liste_des_user_centre')
    else:

        form = UpdateUserForm(instance=user)



    context = {
        'form': form
    }


    return render(request, 'update_user_centre.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def delete_user_candidat(request, id):

    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('liste_des_user_candidat')
    
    context = {
        'user': user

    }
    return render(request, 'delete_user_candidat.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def update_user_candidat(request, id):

    form = None
    user = User.objects.get(id=id)


    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('liste_des_user_candidat')
    else:

        form = UpdateUserForm(instance=user)



    context = {
        'form': form
    }


    return render(request, 'update_user_candidat.html', context)









@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def update_dwsr(request, id):
    form = None
    dwsr_id = Dwsr.objects.get(id=id)
    if request.method == 'POST':
        form = DwsrUpdateForm(request.POST, instance=dwsr_id)
        if form.is_valid():

            form.save()
            return redirect('liste_des_dwsr')

    else:
        form = DwsrUpdateForm(instance=dwsr_id)

    context = {
        'form': form
    }



    return render(request, 'update_dwsr.html', context)









@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def delete_dwsr(request, id):
    dwsr = Dwsr.objects.get(id=id)

    if request.method == 'POST':
        dwsr.delete()
        return redirect('liste_des_dwsr')
    
    context = {
        'dwsr': dwsr
    }
    
    return render(request, 'delete_dwsr.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['CANDIDAT'])
def liste_des_centre(request):
    centres = CentreExamen.objects.all().order_by('wilaya')

    Filter = CentreExamenFilter(request.GET, queryset=centres)
    centres = Filter.qs 
    context = {
        'centres': centres,
        'Filter': Filter,
    } 
    return render(request, 'listedescentres.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['CANDIDAT'])
def liste_session(request, id):
    exists = False
    centre = CentreExamen.objects.get(id=id)
    candidat = Candidat.objects.get(id=request.user.candidat.id)
    sessions_code = Session.objects.all().filter(centre_examen = centre, nom = 'Code').order_by('date')
    sessions_nocode = Session.objects.all().filter(centre_examen = centre).exclude(nom='Code').order_by('date')

    sessions_candidat = Session.objects.all().filter(candidat = candidat).order_by('date')

    for session_candidat in sessions_candidat:
        if session_candidat.nom == 'Code':
            if session_candidat.epreuve.résultat == 'Reçu':
                exists = True
                break

    context = {
        'centre': centre,
        'sessions_code': sessions_code,
        'sessions_nocode': sessions_nocode,
        'exists': exists,
    }
    return render(request, 'listedessession.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['CANDIDAT'])
def inscrir_dans_session(request, id):

    centre = Session.objects.get(id=id).centre_examen

    if request.method == 'POST':
        candidat = Candidat.objects.get(id=request.user.candidat.id)
        Session.objects.all().filter(id=id).update(candidat=candidat)
        session = Session.objects.get(id=id)
        epreuve = Epreuve.objects.create(
            date = session.date,
            session= session,
            nom = session.nom
            )
        
        epreuve.candidat.add(candidat)
            
        return redirect('liste_session', centre.id)
    
    context = {
        'centre': centre
    }

    return render(request, 'inscrir_dans_session.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR', 'DWSR'])
def profile_candidat(request, id):

    candidat = Candidat.objects.get(id=id)
    sessions = Session.objects.all().filter(candidat=candidat).order_by('date')
    epreuve_liste = []
    for session in sessions:
        epreuve = Epreuve.objects.get(session=session)
        epreuve_liste.append(epreuve)



    context = {
        'candidat': candidat, 
        'epreuves': epreuve_liste,
        'sessions': sessions,
    }

    return render(request, 'profile_candidat.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def saisir_résultat(request, id):
    epreuve = Epreuve.objects.get(id=id)
    candidat = epreuve.session.candidat
    form = None
    if request.method == 'POST':
        form = EpreuveResultForm(request.POST, instance=epreuve)
        if form.is_valid():
            form.save()
            return redirect('profile_candidat', candidat.id)

    else:

        form = EpreuveResultForm(instance=epreuve)

    context = {
        'form': form,
        'candidat': candidat
    }
    return render(request, 'saisir_résultat.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_centre(request):


    form = CentreExamenForm()
    if request.method == 'POST':
        form = CentreExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_centre_examens')

    context = {
        'form': form
    }
    return render(request, 'create_centre.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR', 'DNSR'])
def liste_centre_examens(request):

    centres = CentreExamen.objects.all()

    CentreFilter = CentreExamenFilter(request.GET, queryset=centres)
    centres = CentreFilter.qs

    context = {
        'centres': centres,
        'CentreFilter': CentreFilter
    }

    return render(request, 'liste_centre_examens.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_centre_user(request, id):

    form = CreateUserForm()
    if request.method == 'POST':
        form =  CreateUserForm(request.POST) 
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='CENTRE')
            user.groups.add(group)
            centre = CentreExamen.objects.all().filter(id=id).update(user=user)
            return redirect('liste_centre_examens')

    
    context = {
        'form': form

    }
    return render(request, 'create_centre_user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def update_centre(request, id):
    form = None
    centre = CentreExamen.objects.get(id=id)
    if request.method == 'POST':

        form = UpdateCentreExamenForm(request.POST, instance=centre)
        if form.is_valid():
            form.save()
            return redirect('liste_centre_examens')
    else:
        form = UpdateCentreExamenForm(instance=centre)

    

    context = {
        'form': form
    }



    return render(request, 'update_centre.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def delete_centre(request, id):
    centre = CentreExamen.objects.get(id=id)

    if request.method == 'POST':
        centre.delete()
        return redirect('liste_centre_examens')
    
    context = {
        'centre': centre
    }
    
    return render(request, 'delete_centre.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_auto_ecole(request):

    form = AutoEcoleForm()

    if request.method == 'POST':

        form = AutoEcoleForm(request.POST)

        if form.is_valid():

            form.save()
            
            return redirect('liste_auto_ecole')
    context = {
        'form': form
    } 
    return render(request, 'create_auto_ecole.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR', 'DNSR'])
def liste_auto_ecole(request):

    autoEcoles = AutoEcole.objects.all()

    Filter = AutoEcoleFilter(request.GET, queryset=autoEcoles)
    autoEcoles = Filter.qs

    context = {
        'AutoEcoles': autoEcoles,
        'Filter': Filter
    }
    return render(request, 'liste_auto_ecole.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def update_auto_ecole(request, id):
    form = None
    autoEcoles = AutoEcole.objects.get(id=id)

    if request.method == 'POST':

        form = UpdateAutoEcoleForm(request.POST, instance=autoEcoles)
        if form.is_valid():
            form.save()
            return redirect('liste_auto_ecole')
    else:
        form = UpdateAutoEcoleForm(instance=autoEcoles)
    
    context = {
        'form': form
    }

    return render(request, 'update_auto_ecole.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def delete_auto_ecole(request, id):

    autoEcole = AutoEcole.objects.get(id=id)

    if request.method == 'POST':
        autoEcole.delete()
        return redirect('liste_auto_ecole')
    
    context = {
        'AutoEcole': autoEcole
    }
    
    return render(request, 'delete_auto_ecole.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def create_examinateur(request):

    form = ExaminateurForm()

    if request.method == 'POST':

        form = ExaminateurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_examinateur')


    context = {
        'form': form
    }

    return render(request, 'create_examinateur.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR', 'DNSR'])
def liste_examinateur(request):

    examinateures = Examinateur.objects.all()

    Filter = ExaminateurFilter(request.GET, queryset=examinateures)
    examinateures = Filter.qs



    context = {
        'examinateures': examinateures,
        'Filter': Filter
    }

    return render(request, 'liste_examinateur.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def update_examinateur(request, id):

    form = None
    examinateur = Examinateur.objects.get(id=id)

    if request.method == 'POST':
        
        form = UpdateExaminateurForm(request.POST, instance=examinateur)

        if form.is_valid():
            form.save()
            return redirect('liste_examinateur')
        
    else:
        
        form = UpdateExaminateurForm(instance=examinateur)
    
    context = {
        'form': form
    }

    return render(request, 'update_examinateur.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DWSR'])
def delete_examinateur(request, id):

    examinateur = Examinateur.objects.get(id=id)

    if request.method == 'POST':
        examinateur.delete()
        return redirect('liste_examinateur')
    
    context = {
        'examinateur': examinateur
    }
    
    return render(request, 'delete_examinateur.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['CENTRE'])
def session_calendar(request):

    centre_examen = CentreExamen.objects.get(id=request.user.centreexamen.id)
    sessions = Session.objects.all().filter(centre_examen=centre_examen)
    session_list = []

    for session in sessions:
        session_list.append(
            {
                "title": session.nom,
                "start": str(session.date) + 'T' + str(session.heureDebut),
                "end": str(session.date)+'T'+str(session.heureFin),
                "color": '#gtbbf'
            }
        )
    

    context = {
        'sessions': session_list
    }
    return render(request, 'calendrier_des_session.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['CENTRE'])
def add_session(request):
    form = SessionForm()
    centre = CentreExamen.objects.get(id=request.user.centreexamen.id)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            nom = form.cleaned_data['nom']
            heureDebut = form.cleaned_data['heureDebut']
            heureFin = form.cleaned_data['heureFin']

            Session.objects.create(
                date = date,
                nom = nom,
                heureDebut = heureDebut,
                heureFin = heureFin,
                centre_examen = centre,
            )
            
            return redirect('session_calendar')
    context = {
        'form': form
    }
    return render(request, 'create_session.html', context)


# class SessionListView(ListView):
#     model = Session
#     template_name = ''












@login_required(login_url='login')
@allowed_users(allowed_roles=['CENTRE'])
def render_pdf_view(request):

    centre = CentreExamen.objects.get(id=request.user.centreexamen.id)
    sessions = Session.objects.all().filter(
        date = datetime.now().date(),
        centre_examen = centre
        ).order_by('heureDebut')
    template_path = 'pdf/liste_session.html'
    context = {
        'centre': centre,
        'sessions': sessions
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachement: filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '<pre>')
    return response




@login_required(login_url='login')
@allowed_users(allowed_roles=['CANDIDAT'])
def profile_candidat_candidat(request):

    candidat = Candidat.objects.get(id=request.user.candidat.id)

    sessions = Session.objects.all().filter(candidat=candidat).order_by('date')
    epreuve_liste = []
    for session in sessions:
        epreuve = Epreuve.objects.get(session=session)
        epreuve_liste.append(epreuve)



    context = {
        'candidat': candidat, 
        'epreuves': epreuve_liste,
        'sessions': sessions,
    }

    return render(request, 'profile_du_candidat.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['CANDIDAT'])
def render_pdf_convocation(request):

    candidat = Candidat.objects.get(id=request.user.candidat.id)
    sessions = Session.objects.all().filter(
        candidat = candidat,
        ).order_by('date')
    template_path = 'pdf/convocation.html'
    context = {
        'candidat': candidat,
        'sessions': sessions
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachement: filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '<pre>')
    return response



@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def consulter_stat_dwsr(request, id):

    dwsr = Dwsr.objects.get(id=id)

    
    context = {
        'allcandidats': str(Candidat.objects.all().filter(dwsr=dwsr).count()),
        'candidatpending': Candidat.objects.all().filter(dwsr=dwsr, date_reussite=None).count(),
        'candidatfailed': Candidat.objects.all().filter(dwsr=dwsr, réussit=False).count(),
        'candidatsuccess': Candidat.objects.all().filter(dwsr=dwsr, réussit=True).count(),
    }


    return render(request, 'statistiques_dwsr.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['DNSR'])
def consulter_stat_auto_ecole(request, id):
    autoEcole = AutoEcole.objects.get(id=id)

    context = {
        'candidats': str(Candidat.objects.all().filter(auto_école=autoEcole).count()),
        'candidatspending': Candidat.objects.all().filter(auto_école=autoEcole, date_reussite=None).count(),
        'candidatsfailed': Candidat.objects.all().filter(auto_école=autoEcole, réussit=False).count(),
        'candidatssuccess': Candidat.objects.all().filter(auto_école=autoEcole, réussit=True).count(),
    }

    return render(request, 'statistiques_auto_ecole.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['CENTRE'])
def liste_des_sessions_pour_centre(request):

    sessions = Session.objects.all().filter(centre_examen = request.user.centreexamen, candidat=None).order_by('date')

    context = {
        'sessions': sessions,
    }

    return render(request, 'liste_des_sessions_pour_centre.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['CENTRE'])
def delete_this_session(request, id):

    session = Session.objects.get(id=id)

    if request.method == 'POST':
        session.delete()
        return redirect('liste_des_sessions_pour_centre')


    context = {
        'session': session,
    }
    return render(request, 'dlt_session.html', context)
