from django.db import models

from funcionarios.models import Funcionario


class Agendamento(models.Model):
    horario = models.DateTimeField('Horario', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey('clientes.Cliente', verbose_name='Clientes', help_text='Nome do cliente', on_delete=models.PROTECT)
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionário', help_text='Nome do funcionário', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'Cliente: {self.cliente}'


