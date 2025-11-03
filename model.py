from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, Table, text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


DB_URL = "mysql+pymysql://USUARIO:SENHA@HOST:PORTA/locadora_db"
engine = create_engine(DB_URL, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


# Tabela Relacionamento N:M veiculos-acessorios
veiculo_acessorio = Table('veiculo_acessorio', Base.metadata,
    Column('veiculo_id', Integer, ForeignKey('veiculos.id'), primary_key=True),
    Column('acessorio_id', Integer, ForeignKey('acessorios.id'), primary_key=True)
)


# Classes
class Agencia(Base):
    __tablename__ = 'agencias'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(255))
    
    # Relacionamento 1:N
    locacoes_retirada = relationship("Locacao", foreign_keys="[Locacao.agencia_retirada_id]")
    locacoes_devolucao = relationship("Locacao", foreign_keys="[Locacao.agencia_devolucao_id]")


class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    valor_multiplicador = Column(Numeric(5, 2), default=1.0)
    
    # Relacionamento 1:N com veiculo
    veiculos = relationship("Veiculo", backref="categoria")

class Veiculo(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True)
    placa = Column(String(10), unique=True, nullable=False)
    modelo = Column(String(100))
    preco_diaria_base = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default='Disponível')
    
    # Chave estrangeira 1:N
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    # Relacionamento N:M
    acessorios = relationship(
        "Acessorio", 
        secondary=veiculo_acessorio, 
        backref="veiculos"
    )

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cnh = Column(String(12), unique=True)
    
    # Relacionamento 1:N
    locacoes = relationship("Locacao", backref="cliente")

class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    cargo = Column(String(50))
    salario = Column(Numeric(10, 2))

class Locacao(Base):
    __tablename__ = 'locacoes'
    id = Column(Integer, primary_key=True)
    data_inicio = Column(Date, nullable=False)
    data_fim_prevista = Column(Date, nullable=False)
    data_fim_real = Column(Date)
    valor_total = Column(Numeric(10, 2), default=0.0)
    status = Column(String(20), default='PENDENTE')
    
    # Chaves estrangeiras N:1
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'))
    agencia_retirada_id = Column(Integer, ForeignKey('agencias.id'), nullable=False)
    agencia_devolucao_id = Column(Integer, ForeignKey('agencias.id'), nullable=False)


class Acessorio(Base):
    __tablename__ = 'acessorios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    estoque = Column(Integer, default=0) # Campo que vai ser gerenciado por trigger
    preco_extra_diaria = Column(Numeric(10, 2), default=0.0)

class Manutencao(Base):
    __tablename__ = 'manutencoes'
    id = Column(Integer, primary_key=True)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    custo = Column(Numeric(10, 2), default=0.0)
    
    # Chave estrangeira N:1
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'), nullable=False)
    veiculo = relationship("Veiculo", backref="manutencoes")

class TipoServico(Base):
    __tablename__ = 'tipos_servico'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)


class LogPrecos(Base):
    __tablename__ = 'log_precos'
    id = Column(Integer, primary_key=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    preco_antigo = Column(Numeric(10, 2))
    preco_novo = Column(Numeric(10, 2))
    data_alteracao = Column(Date)
    usuario = Column(String(50))
