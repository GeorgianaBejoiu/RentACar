from django.db import models

# Create your models here.

#PERSOANA
class Persoana(models.Model):
    id_persoana = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    adresa = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nume} {self.prenume}"

    class Meta:
        db_table = 'Persoana'

# CLIENT
class Client(models.Model):
    id_persoana = models.OneToOneField(
        Persoana,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persoana'
    )

    class Meta:
        db_table = 'Client'

    def __str__(self):
        return str(self.id_persoana)

# ANGAJAT
class Angajat(models.Model):
    id_persoana = models.OneToOneField(
        Persoana,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_persoana'
    )
    functie = models.CharField(max_length=100)
    salariu = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Angajat'

    def __str__(self):
        return f"{self.id_persoana} - {self.functie}"

# MARCA
class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    marca = models.CharField(max_length=100)
    detalii = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Marca'

    def __str__(self):
        return self.marca

# TIP
class Tip(models.Model):
    id_tip = models.AutoField(primary_key=True)
    tip = models.CharField(max_length=100)
    detalii = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Tip'

    def __str__(self):
        return self.tip
# CLASA
class Clasa(models.Model):
    id_clasa = models.AutoField(primary_key=True)
    clasa = models.CharField(max_length=100)
    descriere = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Clasa'

    def __str__(self):
        return self.clasa

# MASINA
class Masina(models.Model):
    STATUS_CHOICES = [
        ('Disponibila', 'Disponibila'),
        ('Inchiriata', 'Inchiriata'),
    ]

    id_masina = models.AutoField(primary_key=True)
    nr_inmatriculare = models.CharField(max_length=20, unique=True)
    nr_km = models.PositiveIntegerField()
    data_fabricatiei = models.DateField()
    pret_ora = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Disponibila'
    )

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_column='id_marca'
    )
    tip = models.ForeignKey(
        Tip,
        on_delete=models.PROTECT,
        db_column='id_tip'
    )
    clasa = models.ForeignKey(
        Clasa,
        on_delete=models.PROTECT,
        db_column='id_clasa'
    )

    class Meta:
        db_table = 'Masina'

    def __str__(self):
        return self.nr_inmatriculare

# MASINA COMBUSTIBIL
class MasinaCombustibil(models.Model):
    id_masina = models.OneToOneField(
        Masina,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_masina'
    )
    tip_combustibil = models.CharField(max_length=50)
    capacitate_rezervor = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    class Meta:
        db_table = 'MasinaCombustibil'

    def __str__(self):
        return f"{self.id_masina} - {self.tip_combustibil}"

# MASINA ELECTRICA
class MasinaElectrica(models.Model):
    id_masina = models.OneToOneField(
        Masina,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_masina'
    )
    capacitate_baterie = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    autonomie_km = models.PositiveIntegerField()

    class Meta:
        db_table = 'MasinaElectrica'

    def __str__(self):
        return f"{self.id_masina} - {self.autonomie_km} km"

# MASINA HIBRIDA
class MasinaHibrida(models.Model):
    id_masina = models.OneToOneField(
        Masina,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_masina'
    )
    tip_combustibil = models.CharField(max_length=50)
    capacitate_rezervor = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    capacitate_baterie = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    autonomie_electrica_km = models.PositiveIntegerField()

    class Meta:
        db_table = 'MasinaHibrida'

    def __str__(self):
        return f"{self.id_masina} - Hibrida"

# INCHIRIERE
class Inchiriere(models.Model):
    id_inchiriere = models.AutoField(primary_key=True)

    id_client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        db_column='id_client'
    )

    id_masina = models.ForeignKey(
        Masina,
        on_delete=models.PROTECT,
        db_column='id_masina'
    )

    data_inceput = models.DateTimeField()
    data_sfarsit = models.DateTimeField()

    class Meta:
        db_table = 'Inchiriere'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(data_sfarsit__gt=models.F('data_inceput')),
                name='verifica_perioada_inchirierii'
            )
        ]

    def __str__(self):
        return f"Inchiriere {self.id_inchiriere}"

# ANGAJAT INCHIRIERE
class AngajatInchiriere(models.Model):
    id = models.AutoField(primary_key=True)

    id_angajat = models.ForeignKey(
        Angajat,
        on_delete=models.PROTECT,
        db_column='id_angajat'
    )

    id_inchiriere = models.ForeignKey(
        Inchiriere,
        on_delete=models.CASCADE,
        db_column='id_inchiriere'
    )

    class Meta:
        db_table = 'AngajatInchiriere'
        constraints = [
            models.UniqueConstraint(
                fields=['id_angajat', 'id_inchiriere'],
                name='angajat_inchiriere_unic'
            )
        ]

    def __str__(self):
        return f"{self.id_angajat} - {self.id_inchiriere}"

# PLATA
class Plata(models.Model):
    id_plata = models.AutoField(primary_key=True)

    id_inchiriere = models.ForeignKey(
        Inchiriere,
        on_delete=models.PROTECT,
        db_column='id_inchiriere'
    )

    suma = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    data_platii = models.DateTimeField()

    class Meta:
        db_table = 'Plata'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(suma__gt=0),
                name='verifica_suma_platii'
            )
        ]

    def __str__(self):
        return f"Plata {self.id_plata} - {self.suma} lei"

# ASIGURARE
class Asigurare(models.Model):
    id_asigurare = models.AutoField(primary_key=True)

    id_masina = models.ForeignKey(
        Masina,
        on_delete=models.PROTECT,
        db_column='id_masina'
    )

    tip_asigurare = models.CharField(max_length=100)
    data_inceput = models.DateField()
    data_sfarsit = models.DateField()

    class Meta:
        db_table = 'Asigurare'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(data_sfarsit__gt=models.F('data_inceput')),
                name='verifica_perioada_asigurarii'
            )
        ]

    def __str__(self):
        return f"{self.tip_asigurare} - {self.id_masina}"

# REVIZIE
class Revizie(models.Model):
    id_revizie = models.AutoField(primary_key=True)

    data_revizie = models.DateField()
    descriere = models.TextField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'Revizie'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cost__gte=0),
                name='verifica_cost_revizie'
            )
        ]

    def __str__(self):
        return f"Revizie {self.id_revizie}"

# ARE REVIZII
class AreRevizii(models.Model):

    id_angajat = models.ForeignKey(
        Angajat,
        on_delete=models.PROTECT,
        db_column='id_angajat'
    )

    id_masina = models.ForeignKey(
        Masina,
        on_delete=models.PROTECT,
        db_column='id_masina'
    )

    id_revizie = models.ForeignKey(
        Revizie,
        on_delete=models.CASCADE,
        db_column='id_revizie'
    )

    class Meta:
        db_table = 'AreRevizii'
        constraints = [
            models.UniqueConstraint(
                fields=['id_angajat', 'id_masina', 'id_revizie'],
                name='are_revizii_unic'
            )
        ]

    def __str__(self):
        return f"{self.id_angajat} - {self.id_masina} - {self.id_revizie}"