
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
        'model',
        'nr_inmatriculare',
        'marca',
        'tip',
        'clasa',
        'pret_ora_ron',
        'status',
    )

    list_filter = ('status', 'marca', 'tip', 'clasa')

    search_fields = (
        'model',
        'nr_inmatriculare',
        'marca__marca',
    )

    @admin.display(description='Pret pe ora (RON)')
    def pret_ora_ron(self, obj):
        return f"{obj.pret_ora} RON/oră"



admin.site.register(MasinaCombustibil)
admin.site.register(MasinaElectrica)
admin.site.register(MasinaHibrida)

admin.site.register(Inchiriere)
admin.site.register(AngajatInchiriere)
admin.site.register(Plata)
admin.site.register(Asigurare)
admin.site.register(Revizie)
admin.site.register(AreRevizii)
