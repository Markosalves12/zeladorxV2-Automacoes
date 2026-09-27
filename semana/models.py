from django.db import models

# Create your models here.
class DiasDaSemana(models.Model):
    diasdasemana = [
        ('Segunda-Feira', 'Segunda-Feira'),
        ('Terça-Feira', 'Terça-Feira'),
        ('Quarta-Feira', 'Quarta-Feira'),
        ('Quinta-Feira', 'Quinta-Feira'),
        ('Sexta-Feira', 'Sexta-Feira'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]


    diasdasemana = models.CharField(
        choices=diasdasemana,
        max_length=60,
        blank=False,
        null=False,
        unique=True
    )

    def __str__(self):
        return self.diasdasemana