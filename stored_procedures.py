from sqlalchemy import text
from database import engine


def create_stored_procedures():
    sql_script = """
    DELIMITER //

    -- Stored Procedure 1: Registrar pagamento da reserva e atualizar status
    CREATE PROCEDURE SP_RegistrarPagamento(
        IN p_reserva_id INT,
        IN p_metodo_pagamento VARCHAR(50),
        IN p_valor_pago DECIMAL(10, 2)
    )
    BEGIN
        DECLARE v_valor_devido DECIMAL(10, 2);
        DECLARE v_status_pagamento VARCHAR(30);

        SELECT valor_devido INTO v_valor_devido FROM pagamentos WHERE reserva_id = p_reserva_id LIMIT 1;

        IF p_valor_pago >= v_valor_devido THEN
            SET v_status_pagamento = 'PAGO';
        ELSE
            SET v_status_pagamento = 'PARCIAL';
        END IF;

        INSERT INTO pagamentos (reserva_id, data_pagamento, valor_devido, valor_pago, metodo_pagamento, status_pagamento)
        VALUES (p_reserva_id, CURDATE(), v_valor_devido, p_valor_pago, p_metodo_pagamento, v_status_pagamento);
    
    END //

    -- Stored Procedure 2: Atualizar disponibilidade do veículo (após reserva)
    CREATE PROCEDURE SP_AtualizarDisponibilidadeVeiculo(
        IN p_veiculo_id INT,
        IN p_disponivel BOOLEAN
    )
    BEGIN
        UPDATE veiculos
        SET disponibilidade = p_disponivel
        WHERE id_veiculo = p_veiculo_id;
    END //


    -- Stored Procedure 3: Buscar veículos por categoria e disponibilidade
    CREATE PROCEDURE SP_BuscarVeiculosPorCategoria(
        IN p_categoria_id INT
    )
    BEGIN
        SELECT 
            V.placa, 
            V.modelo, 
            C.nome_categoria, 
            C.valor_diaria_categoria
        FROM veiculos V
        JOIN categorias C ON V.categoria_veiculo = C.id_categoria
        WHERE V.disponibilidade = TRUE
        AND V.categoria_veiculo = p_categoria_id
        ORDER BY C.valor_diaria_categoria ASC;
    END //

    -- Stored Procedure 4: Gerar relatório de manutenções por período
    CREATE PROCEDURE SP_RelatorioManutencoesPorPeriodo(
        IN p_data_inicio DATE,
        IN p_data_fim DATE
    )
    BEGIN
        SELECT 
            M.data_manutencao, 
            M.tipo_manutencao, 
            M.custo_manutencao, 
            V.placa, 
            V.modelo
        FROM manutencao M
        JOIN veiculos V ON M.veiculo = V.id_veiculo
        WHERE M.data_manutencao BETWEEN p_data_inicio AND p_data_fim
        ORDER BY M.data_manutencao DESC;
    END //

    DELIMITER ;

    """

    with engine.connect() as conn:
        for statement in sql_script.split("//"):
            stmt = statement.strip()

            if stmt:
                conn.execute(text(stmt))

    conn.commit

if __name__ == "__main__":
    create_stored_procedures()
    print("Stored procedures criados com sucesso!")