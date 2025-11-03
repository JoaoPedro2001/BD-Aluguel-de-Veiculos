from datetime import date, timedelta
from database import engine, DBModel, DBSession, get_session
from models import (
    Cliente, Atendente, Veiculo, Categoria, 
    Seguro, Reserva, Pagamento, Manutencao, 
    Multa, Agencia # Adicionando a nova tabela Agencia
)

def populate_initial_data():
    with get_session() as session:
    
        agencia_centro = Agencia(nome_agencia='Agência Central', endereco='Rua A, 100')
        agencia_aeroporto = Agencia(nome_agencia='Agência Aeroporto', endereco='Terminal 2')
        session.add_all([agencia_centro, agencia_aeroporto])
        session.commit() 

       
        cat_economico = Categoria(nome_categoria='Econômico', valor_diaria_categoria=80.00)
        cat_suv = Categoria(nome_categoria='SUV', valor_diaria_categoria=150.00)
        cat_luxo = Categoria(nome_categoria='Luxo', valor_diaria_categoria=300.00)
        session.add_all([cat_economico, cat_suv, cat_luxo])
        session.commit()

       
        atendente_1 = Atendente(nome_atendente='Alice Silva', cpf_atendente='11122233344', telefone_atendente='987654321', email_atendente='alice@locadora.com', salario=3000.00)
        atendente_2 = Atendente(nome_atendente='Bob Souza', cpf_atendente='55566677788', telefone_atendente='912345678', email_atendente='bob@locadora.com', salario=3200.00)
        session.add_all([atendente_1, atendente_2])
        session.commit()
        

        veiculo_1 = Veiculo(placa='ABC1A23', modelo='Onix', ano=2024, cor='Branco', disponibilidade=True, categoria_veiculo=cat_economico.id_categoria)
        veiculo_2 = Veiculo(placa='XYZ9B87', modelo='Jeep Compass', ano=2023, cor='Preto', disponibilidade=False, categoria_veiculo=cat_suv.id_categoria) 
        veiculo_3 = Veiculo(placa='DEF4C56', modelo='BMW X5', ano=2025, cor='Prata', disponibilidade=True, categoria_veiculo=cat_luxo.id_categoria)
        
        session.add_all([veiculo_1, veiculo_2, veiculo_3])
        session.commit()
        
    
        cliente_ativo = Cliente(nome_cliente='Carlos Ferreira', cpf_cliente='12345678900', cnh_cliente='12345678901', telefone_cliente='998877665', email_cliente='carlos@teste.com')
        cliente_limpo = Cliente(nome_cliente='Maria Teste', cpf_cliente='00987654321', cnh_cliente='00987654322', telefone_cliente='955443322', email_cliente='maria@teste.com')
        session.add_all([cliente_ativo, cliente_limpo])
        session.commit()
        
        seguro_basico = Seguro(nome_seguro='Básico', valor_diaria_seguro=10.00)
        seguro_completo = Seguro(nome_seguro='Completo', valor_diaria_seguro=30.00)
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

        print("\n--- População de Dados Concluída! ---")
        print(f"Cientes inseridos: 2. Veículos: 3. Reservas ativas: 1.")
        print("Você pode testar a lógica do servidor agora.")

if __name__ == '__main__':
    from models import * 
    DBModel.metadata.create_all(engine)
    
    populate_initial_data()