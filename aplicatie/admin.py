
from django.contrib import admin
from .models import (
    Persoana,
    Client,
    Angajat,
    Marca,
    Tip,
    Clasa,
    Masina,
    MasinaCombustibil,
    MasinaElectrica,
    MasinaHibrida,
    Inchiriere,
    AngajatInchiriere,
    Plata,
    Asigurare,
    Revizie,
    AreRevizii
)


admin.site.register(Persoana)
admin.site.register(Client)
admin.site.register(Angajat)

admin.site.register(Marca)
admin.site.register(Tip)
admin.site.register(Clasa)


@admin.register(Masina)
class MasinaAdmin(admin.ModelAdmin):
    list_display = (
        'id_masina',
        'nr_inmatriculare',
        'marca',
        'tip',
        'clasa',
        'pret_ora',
        'status',
    )

    list_filter = ('status', 'marca', 'tip', 'clasa')

    search_fields = ('nr_inmatriculare', 'marca__marca')


admin.site.register(MasinaCombustibil)
admin.site.register(MasinaElectrica)
admin.site.register(MasinaHibrida)

admin.site.register(Inchiriere)
admin.site.register(AngajatInchiriere)
admin.site.register(Plata)
admin.site.register(Asigurare)
admin.site.register(Revizie)
admin.site.register(AreRevizii)
