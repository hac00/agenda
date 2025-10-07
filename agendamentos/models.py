from django.db import models

from funcionarios.models import Funcionario


class Agendamento(models.Model):
    horario = models.DateTimeField('Horario', help_text='Data e hora do atendimento')
    cliente = models.ForeignKey('clientes.Cliente', verbose_name='Clientes', help_text='Nome do cliente', on_delete=models.PROTECT)
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionário', help_text='Nome do funcionário', on_delete=models.PROTECT)
    servico = models.ManyToManyField('servicos.Servico', verbose_name='Serviço', through='agendamentos.OrdemServicos')
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2, default=0.00)
    status = models.CharField('Status', max_length=1, help_text='Status do agendamento', default='A')

    @property
    def servicos(self):
        return OrdemServicos.objects.filter(agendamento=self)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['-horario']

    def __str__(self):
        return f'Cliente: {self.cliente}'

class OrdemServicos(models.Model):
    SITUACAO_OPCOES = (
        ('A', 'Agendado'),
        ('R', 'Realizado'),
        ('C', 'Cancelado'),
    )
    agendamento = models.ForeignKey('agendamentos.Agendamento', verbose_name='Agendamento', on_delete=models.CASCADE, related_name='agendamento')
    servico = models.ForeignKey('servicos.Servico', verbose_name='Serviço', on_delete=models.CASCADE, related_name='ordem_servico')
    funcionario = models.ForeignKey('funcionarios.Funcionario', verbose_name='Funcionario', on_delete=models.CASCADE, related_name='funcionario')
    situacao = models.CharField('Situação', max_length=1, choices=SITUACAO_OPCOES, default='A')
    observacoes = models.TextField('Observações', max_length=300, blank=True, null=True)
    preco = models.DecimalField('Preço', max_digits=6, decimal_places=2, help_text='Preço do serviço', default=0.00)

    def calcula_valor_ordem(self):
        valor_total = 0
        qs = OrdemServicos.objects.filter(agendamento=self.agendamento)
        for item in qs:
            if item.situacao != 'C':
                valor_total += item.preco
        self.agendamento.valor = valor_total
        self.agendamento.save()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.preco = self.servico.preco
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
        self.calcula_valor_ordem()

    def delete(self, using=None, keep_parents=False):
        super().delete(using=None, keep_parents=False)
        self.calcula_valor_ordem()

    class Meta:
        verbose_name = 'Serviço realizado'
        verbose_name_plural = 'Serviço realizados'

        constraints = [models.UniqueConstraint(fields=['agendamento', 'servico'], name='constraint_agendamento')]

    def __str__(self):
        return self.servico.nome


