from typing import List
from sqlalchemy import Table, Column, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from database import DBModel

# Tabela de relacinamento entre tabelas reservas e seguros (N:N)
reserva_seguro = Table(
    'reservas_seguros',
    DBModel.metadata,
    Column('id_reserva', ForeignKey('reservas.id_reserva')),
    Column('id_seguro', ForeignKey('seguros.id_seguro'))
)

class Cliente(DBModel):
    __tablename__ = 'clientes'
    id_cliente:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_cliente:Mapped[str] = mapped_column(String(100), nullable=False)
    cpf_cliente:Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    cnh_cliente:Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    telefone_cliente:Mapped[str] = mapped_column(String(15), nullable=False)
    email_cliente:Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, **kwargs):
        self.nome_cliente = kwargs['nome_cliente']
        self.cpf_cliente =  kwargs['cpf_cliente']
        self.cnh_cliente = kwargs['cnh_cliente']
        self.telefone_cliente =  kwargs['telefone_cliente']
        self.email_cliente =  kwargs['email_cliente']

class Atendente(DBModel):
    __tablename__ = 'atendentes'
    id_atendente:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_atendente:Mapped[str] = mapped_column(String(20), nullable=False)
    cpf_atendente:Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    telefone_atendente:Mapped[str] = mapped_column(String(15), nullable=False)
    email_atendente:Mapped[str] = mapped_column(String(100), nullable=True)
    salario:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    def __init__(self, **kwargs):
        self.nome_atendente = kwargs['nome_atendente']
        self.cpf_atendente = kwargs['cpf_atendente']
        self.telefone_atendente = kwargs['telefone_atendente']
        self.email_atendente = kwargs['email_atendente']
        self.salario = kwargs['salario']

class Veiculo(DBModel):
    __tablename__ = 'veiculos'
    id_veiculo:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    placa:Mapped[str] = mapped_column(String(10), nullable=False)
    modelo:Mapped[str] = mapped_column(String(100), nullable=False)
    ano:Mapped[int] = mapped_column(nullable=False)
    cor:Mapped[str] = mapped_column(String(30), nullable=False)
    disponibilidade:Mapped[bool] = mapped_column(nullable=False)

    # Chaves estrangeiras:
    categoria_veiculo:Mapped[int] = mapped_column(ForeignKey('categorias.id_categoria'))

    def __init__(self, **kwargs):
        self.placa = kwargs['placa']
        self.modelo = kwargs['modelo']
        self.ano = kwargs['ano']
        self.cor = kwargs['cor']
        self.disponibilidade = kwargs['disponibilidade']
        self.categoria_veiculo = kwargs['categoria_veiculo']

class Categoria(DBModel):
    __tablename__ = 'categorias'
    id_categoria:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_categoria:Mapped[str] = mapped_column(String(50), nullable=False)
    valor_diaria_categoria:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    def __init__(self, **kwargs):
        self.nome_categoria = kwargs['nome_categoria']
        self.valor_diaria_categoria = kwargs['valor_diaria_categoria']

class Seguro(DBModel):
    __tablename__ = 'seguros'
    id_seguro:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome_seguro:Mapped[str] = mapped_column(String(100), nullable=False)
    valor_diaria_seguro:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    def __init__(self, **kwargs):
        self.nome_seguro = kwargs['nome_seguro']
        self.valor_diaria_seguro = kwargs['valor_diaria_seguro']

class Reserva(DBModel):
    __tablename__ = 'reservas'
    id_reserva:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_inicio:Mapped[date] = mapped_column(nullable=False)
    data_fim_prevista:Mapped[date] = mapped_column(nullable=False)
    status_reserva:Mapped[str] = mapped_column(String(30), nullable=False)

    # Chaves estrangeiras:
    cliente:Mapped[int] = mapped_column(ForeignKey('clientes.id_cliente'))
    veiculo:Mapped[int] = mapped_column(ForeignKey('veiculos.id_veiculo'))
    atendente:Mapped[int] = mapped_column(ForeignKey('atendentes.id_atendente'))

    seguro:Mapped[List[Seguro]] = relationship(secondary=reserva_seguro)

    def __init__(self, **kwargs):
        self.data_inicio = kwargs['data_inicio']
        self.data_fim_prevista = kwargs['data_fim_prevista']
        self.status_reserva = kwargs['status_reserva']
        self.cliente = kwargs['cliente']
        self.veiculo = kwargs['veiculo']
        self.atendente = kwargs['atendente']

class Pagamento(DBModel):
    __tablename__ = 'pagamentos'
    id_pagamento:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_pagamento:Mapped[date] = mapped_column(nullable=True)
    valor_devido:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    valor_pago:Mapped[float] = mapped_column(Numeric(10,2), nullable=False, default=0)
    metodo_pagamento = mapped_column(String(50), nullable=False)
    status_pagamento = mapped_column(String(30), nullable=False)

    # Chaves estrangeiras:
    reserva:Mapped[int] = mapped_column(ForeignKey('reservas.id_reserva'))

    def __init__(self, **kwargs):
        self.data_pagamento = kwargs['data_pagamento']
        self.valor_devido = kwargs['valor_devido']
        self.valor_pago = kwargs['valor_pago']
        self.metodo_pagamento = kwargs['metodo_pagamento']
        self.status_pagamento = kwargs['status_pagamento']
        self.reserva = kwargs['reserva']

class Manutencao(DBModel):
    __tablename__ = 'manutencao'
    id_manutencao:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_manutencao:Mapped[date] = mapped_column(nullable=False)
    tipo_manutencao:Mapped[str] = mapped_column(String(50), nullable=False)
    custo_manutencao:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)

    # Chaves estrangeiras:
    veiculo:Mapped[int] = mapped_column(ForeignKey('veiculos.id_veiculo'))

    def __init__(self, **kwargs):
        self.data_manutencao = kwargs['data_manutencao']
        self.tipo_manutencao = kwargs['tipo_manutencao']
        self.custo_manutencao = kwargs['custo_manutencao']
    
class Multa(DBModel):
    __tablename__ = 'multas'
    id_multa:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_multa:Mapped[date] = mapped_column(nullable=False)
    valor_multa:Mapped[float] = mapped_column(Numeric(10,2,), nullable=False)
    status_pagamento:Mapped[str] = mapped_column(String(30), nullable=False)

    # Chaves estrangeiras:
    reserva:Mapped[int] = mapped_column(ForeignKey('reservas.id_reserva'))

    def __init__(self, **kwargs):
        self.data_multa = kwargs['data_multa']
        self.valor_multa = kwargs['valor_multa']
        self.status_pagamento = kwargs['status_pagamento']
        self.reserva = kwargs['reserva']
