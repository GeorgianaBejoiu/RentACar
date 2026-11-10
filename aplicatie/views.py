from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.db import transaction
from .forms import InregistrareClientForm
from django.db.models import Q

from .models import Persoana, Client, Masina, Marca, Tip, Clasa



def login_client(request):
    form = AuthenticationForm(
        request,
        data=request.POST if request.method == 'POST' else None
    )

    if request.method == 'POST' and form.is_valid():
        utilizator = form.get_user()

        # Verificăm dacă utilizatorul este administrator
        if utilizator.is_staff:
            login(request, utilizator)
            return redirect('admin:index')

        # Dacă nu este administrator, verificăm dacă este client
        try:
            persoana = utilizator.persoana
            client = persoana.client

        except (Persoana.DoesNotExist, Client.DoesNotExist):
            form.add_error(
                None,
                'Acest cont nu este asociat unui client.'
            )

        else:
            login(request, utilizator)
            return redirect('lista_masini')

    #Afisam pagina de login si ii transmitem formularul.
    return render(
        request,
        'aplicatie/login.html',
        {'form': form}
    )

@login_required(login_url='login_client')
def client_home(request):
    try:
        persoana = request.user.persoana
        client = persoana.client
    except (Persoana.DoesNotExist, Client.DoesNotExist):
        return HttpResponseForbidden(
            'Nu ai permisiunea de a accesa pagina clientului.'
        )

    return render(request, 'aplicatie/client_home.html')

def logout_client(request):
    logout(request)
    return redirect('login_client')


@login_required(login_url='login_client')
def lista_masini(request):
    try:
        persoana = request.user.persoana
        client = persoana.client
    except (Persoana.DoesNotExist, Client.DoesNotExist):
        return HttpResponseForbidden(
            'Nu ai permisiunea de a accesa această pagină.'
        )

    masini = Masina.objects.filter(status='Disponibila')
    cautare = request.GET.get('q', '')

    if cautare:
        masini = masini.filter(
            Q(model__icontains=cautare) |
            Q(marca__marca__icontains=cautare)
        )

    marca_selectata = request.GET.get('marca')
    tip_selectat = request.GET.get('tip')
    clasa_selectata = request.GET.get('clasa')

    if marca_selectata:
        masini = masini.filter(marca__id_marca=marca_selectata)

    if tip_selectat:
        masini = masini.filter(tip__id_tip=tip_selectat)

    if clasa_selectata:
        masini = masini.filter(clasa__id_clasa=clasa_selectata)

    marci = Marca.objects.all()
    tipuri = Tip.objects.all()
    clase = Clasa.objects.all()

    return render(request, 'aplicatie/masini.html', {
        'masini': masini,
        'marci': marci,
        'tipuri': tipuri,
        'clase': clase,
        'marca_selectata': marca_selectata,
        'tip_selectat': tip_selectat,
        'clasa_selectata': clasa_selectata,
        'nume_client': persoana.prenume + ' ' + persoana.nume,
    })
@login_required(login_url='login_client')
def detalii_masina(request, id_masina):
    try:
        persoana = request.user.persoana
        client = persoana.client
    except (Persoana.DoesNotExist, Client.DoesNotExist):
        return HttpResponseForbidden(
            'Nu ai permisiunea de a accesa această pagină.'
        )

    masina = get_object_or_404(
        Masina,
        id_masina=id_masina,
        status='Disponibila'
    )

    return render(request, 'aplicatie/detalii_masina.html', {
        'masina': masina
    })
def inregistrare_client(request):
    form = InregistrareClientForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            utilizator = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            persoana = Persoana.objects.create(
                nume=form.cleaned_data['nume'],
                prenume=form.cleaned_data['prenume'],
                telefon=form.cleaned_data['telefon'],
                email=form.cleaned_data['email'],
                adresa=form.cleaned_data['adresa'],
                tip_persoana='Client',
                utilizator=utilizator
            )

            Client.objects.create(
                id_persoana=persoana
            )

        login(request, utilizator)
        return redirect('lista_masini')

    return render(
        request,
        'aplicatie/inregistrare.html',
        {'form': form}
    )