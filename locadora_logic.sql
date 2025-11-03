USE locadora_db; -- NOME DO BANCO DE DADOS!!! Se mudar, a gente tem que mudar aqui

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


-- 1. Trigger: Garantir que a data de devolução seja posterior à retirada
CREATE TRIGGER TRG_ValidarDataReserva
BEFORE INSERT ON reservas
FOR EACH ROW
BEGIN
    IF NEW.data_fim_prevista <= NEW.data_inicio THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A data de devolução prevista deve ser posterior à data de início da reserva.';
    END IF;
END //

-- 2. Trigger: Atualizar status de pagamento de reserva
CREATE TRIGGER TRG_AtualizarStatusReservaPagamento
AFTER INSERT ON pagamentos
FOR EACH ROW
BEGIN
    IF NEW.status_pagamento = 'PAGO' THEN
        UPDATE reservas
        SET status_reserva = 'PAGA'
        WHERE id_reserva = NEW.reserva_id;
    END IF;
END //

-- 3. Trigger: Impede a exclusão de clientes com reservas ativas
CREATE TRIGGER TRG_ImpedirExclusaoCliente
BEFORE DELETE ON clientes
FOR EACH ROW
BEGIN
    DECLARE v_reservas_ativas INT;
    
    SELECT COUNT(*) INTO v_reservas_ativas
    FROM reservas
    WHERE cliente_id = OLD.id_cliente
      AND status_reserva <> 'FINALIZADA';

    IF v_reservas_ativas > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Não é possível excluir o cliente. Ele possui reservas ativas ou pendentes.';
    END IF;
END //

DELIMITER ;