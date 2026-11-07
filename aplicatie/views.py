from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Persoana, Client, Masina, Marca, Tip, Clasa


def login_client(request):
    form = AuthenticationForm(
        request,
        data=request.POST if request.method == 'POST' else None
    )

    if request.method == 'POST' and form.is_valid():
        utilizator = form.get_user()

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
    })
