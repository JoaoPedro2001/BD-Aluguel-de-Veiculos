from datetime import date, timedelta
from database import engine, DBModel, get_session
from models import (
    Cliente, Atendente, Veiculo, Categoria, 
    Seguro, Reserva, Pagamento, Manutencao, 
    Multa,
)

def populate_initial_data():
    with get_session() as session:

        cat_economico = Categoria(
            nome_categoria='Econômico',
            valor_diaria_categoria=80.00
        )
        cat_suv = Categoria(
            nome_categoria='SUV',
            valor_diaria_categoria=150.00
        )
        cat_luxo = Categoria(
            nome_categoria='Luxo',
            valor_diaria_categoria=300.00
        )
        cat_van = Categoria(
             nome_categoria='Van',
             valor_diaria_categoria=250.00
        )
        session.add_all([cat_economico, cat_suv, cat_luxo, cat_van])
        session.commit()

        atendente_1 = Atendente(
            nome_atendente='Alice Silva',
            cpf_atendente='11122233344',
            telefone_atendente='987654321',
            email_atendente='alice@locadora.com',
            salario=3000.00
        )
        atendente_2 = Atendente(
            nome_atendente='Bob Souza',
            cpf_atendente='55566677788',
            telefone_atendente='912345678',
            email_atendente='bob@locadora.com',
            salario=3200.00
        )
        atendente_3 = Atendente(
            nome_atendente='Sofia Mendes',
            cpf_atendente='77788899900',
            telefone_atendente='933445566',
            email_atendente='sofia@locadora.com',
            salario=2800.00
        )
        atendente_4 = Atendente(
            nome_atendente='Ricardo Neves',
            cpf_atendente='22211100099',
            telefone_atendente='966778899',
            email_atendente='ricardo@locadora.com',
            salario=3500.00
        )
        session.add_all([atendente_1, atendente_2, atendente_3, atendente_4])
        session.commit()

        veiculo_1 = Veiculo(
            placa='ABC1A23',
            modelo='Onix',
            ano=2024,
            cor='Branco',
            disponibilidade=True,
            categoria_veiculo=cat_economico.id_categoria,
        )
        veiculo_2 = Veiculo(
            placa='XYZ9B87',
            modelo='Jeep Compass',
            ano=2023,
            cor='Preto',
            disponibilidade=False,
            categoria_veiculo=cat_suv.id_categoria,
        )
        veiculo_3 = Veiculo(
            placa='DEF4C56',
            modelo='BMW X5',
            ano=2025,
            cor='Prata',
            disponibilidade=True,
            categoria_veiculo=cat_luxo.id_categoria,
        )
        veiculo_4 = Veiculo(
            placa='VAN7D89',
            modelo='Renault Master',
            ano=2022, cor='Branco',
            disponibilidade=True,
            categoria_veiculo=cat_van.id_categoria
        )
        veiculo_5 = Veiculo(
            placa='GHI2E34',
            modelo='Corsa',
            ano=2018,
            cor='Azul',
            disponibilidade=True,
            categoria_veiculo=cat_economico.id_categoria
        )
        session.add_all([veiculo_1, veiculo_2, veiculo_3, veiculo_4, veiculo_5])
        session.commit()

    
        cliente_ativo = Cliente(
            nome_cliente='Carlos Ferreira',
            cpf_cliente='12345678900',
            cnh_cliente='12345678901',
            telefone_cliente='998877665',
            email_cliente='carlos@teste.com'
        )
        cliente_limpo = Cliente(
            nome_cliente='Maria Teste',
            cpf_cliente='00987654321',
            cnh_cliente='00987654322',
            telefone_cliente='955443322',
            email_cliente='maria@teste.com'
        )
        cliente_historico = Cliente(
            nome_cliente='João Histórico',
            cpf_cliente='33344455566',
            cnh_cliente='33344455567',
            telefone_cliente='944332211',
            email_cliente='joao@teste.com'
        )
        cliente_novo_teste = Cliente(
            nome_cliente='Pedro Almeida',
            cpf_cliente='44455566677',
            cnh_cliente='44455566678',
            telefone_cliente='977889900',
            email_cliente='pedro.almeida@teste.com'
        )
        cliente_vip = Cliente(
            nome_cliente='Ana Torres',
            cpf_cliente='99900011122',
            cnh_cliente='99900011123',
            telefone_cliente='911223344',
            email_cliente='ana.torres@teste.com'
        )
        session.add_all([cliente_ativo, cliente_limpo, cliente_historico, cliente_novo_teste, cliente_vip])
        session.commit()


        seguro_basico = Seguro(
            nome_seguro='Básico',
            valor_diaria_seguro=10.00
        )
        seguro_completo = Seguro(
            nome_seguro='Completo',
            valor_diaria_seguro=30.00
        )
        session.add_all([seguro_basico, seguro_completo])
        session.commit()

    
        reserva_ativa = Reserva(
            data_inicio=date.today(),
            data_fim_prevista=date.today() + timedelta(days=5),
            status_reserva='ATIVA',
            cliente=cliente_ativo.id_cliente,
            veiculo=veiculo_1.id_veiculo,
            atendente=atendente_1.id_atendente
        )
        reserva_ativa.seguro = [seguro_basico, seguro_completo]
        session.add(reserva_ativa)

        reserva_historico = Reserva(
            data_inicio=date.today() - timedelta(days=20),
            data_fim_prevista=date.today() - timedelta(days=15),
            status_reserva='FINALIZADA',
            cliente=cliente_historico.id_cliente,
            veiculo=veiculo_5.id_veiculo,
            atendente=atendente_2.id_atendente
        )
        session.add(reserva_historico)
        session.commit()

        pagamento_pago = Pagamento(
            data_pagamento=date.today(),
            valor_devido=400.00,
            valor_pago=400.00,
            metodo_pagamento='Cartão',
            status_pagamento='PAGO',
            reserva=reserva_ativa.id_reserva
        )
        session.add(pagamento_pago)
        session.commit()

        manutencao_recente = Manutencao(
            data_manutencao=date.today() - timedelta(days=10),
            tipo_manutencao='Troca de óleo',
            custo_manutencao=350.00,
            veiculo=veiculo_3.id_veiculo
        )
        session.add(manutencao_recente)
        session.commit()

        multa_1 = Multa(
            data_multa=date.today() - timedelta(days=2),
            valor_multa=150.00,
            status_pagamento='PENDENTE',
            reserva=reserva_ativa.id_reserva
        )
        session.add(multa_1)
        session.commit()

        print("\n--- População de Dados Concluída! ---")
        print(f"Categorias: 4 | Atendentes: 4 | Veículos: 5 | Clientes: 5 | Reservas: 1 | Pagamentos: 1 | Manutenções: 1 | Multas: 1")
        print("Banco populado com sucesso!")

if __name__ == '__main__':
    DBModel.metadata.create_all(engine)
    populate_initial_data()
