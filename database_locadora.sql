-- Necessário pra o Trigger 1
CREATE TABLE IF NOT EXISTS Log_Precos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    veiculo_id INT,
    preco_antigo DECIMAL(10, 2),
    preco_novo DECIMAL(10, 2),
    data_alteracao DATETIME,
    usuario VARCHAR(50)
);

-- Necessário pra o Trigger 3
CREATE TABLE IF NOT EXISTS Log_Estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    acessorio_id INT,
    quantidade_anterior INT,
    quantidade_nova INT,
    tipo_operacao VARCHAR(10), 
    data_log DATETIME
);


DELIMITER //

-- Stored Procedure 1: Calcula o valor total e registra a locação
CREATE PROCEDURE SP_RegistrarNovaLocacao(
    IN p_cliente_id INT,
    IN p_veiculo_id INT,
    IN p_funcionario_id INT,
    IN p_agencia_retirada_id INT,
    IN p_agencia_devolucao_id INT,
    IN p_data_inicio DATE,
    IN p_data_fim_prevista DATE
)
BEGIN
    DECLARE v_dias INT;
    DECLARE v_diaria_base DECIMAL(10, 2);
    DECLARE v_multiplicador DECIMAL(5, 2);
    DECLARE v_valor_total DECIMAL(10, 2);

    SET v_dias = DATEDIFF(p_data_fim_prevista, p_data_inicio);

    SELECT V.preco_diaria_base, C.valor_multiplicador 
    INTO v_diaria_base, v_multiplicador
    FROM Veiculos V
    JOIN Categorias C ON V.categoria_id = C.id
    WHERE V.id = p_veiculo_id;
    
    SET v_valor_total = v_diaria_base * v_multiplicador * v_dias;

    INSERT INTO Locacoes (
        cliente_id, veiculo_id, funcionario_id, agencia_retirada_id, 
        agencia_devolucao_id, data_inicio, data_fim_prevista, valor_total, status
    )
    VALUES (
        p_cliente_id, p_veiculo_id, p_funcionario_id, p_agencia_retirada_id, 
        p_agencia_devolucao_id, p_data_inicio, p_data_fim_prevista, v_valor_total, 'ATIVA'
    );
    
    UPDATE Veiculos SET status = 'Alugado' WHERE id = p_veiculo_id;
END //

-- Stored Procedure 2: Busca veículos disponíveis em um período
CREATE PROCEDURE SP_BuscarVeiculosDisponiveis(
    IN p_data_inicio DATE,
    IN p_data_fim DATE,
    IN p_categoria_id INT
)
BEGIN
    SELECT V.placa, V.modelo, C.nome AS categoria
    FROM Veiculos V
    JOIN Categorias C ON V.categoria_id = C.id
    WHERE V.status = 'Disponível'
    AND C.id = IFNULL(p_categoria_id, C.id) 
    AND V.id NOT IN (
        SELECT veiculo_id FROM Locacoes
        WHERE status = 'ATIVA' AND 
        (data_inicio <= p_data_fim AND data_fim_prevista >= p_data_inicio)
    )
    AND V.id NOT IN (
        SELECT veiculo_id FROM Manutencoes
        WHERE data_fim IS NULL OR 
        (data_inicio <= p_data_fim AND data_fim >= p_data_inicio)
    );
END //

-- Stored Procedure 3: Gerencia o início de uma manutenção
CREATE PROCEDURE SP_IniciarManutencao(
    IN p_veiculo_id INT,
    IN p_data_inicio DATE
)
BEGIN
    INSERT INTO Manutencoes (veiculo_id, data_inicio, custo)
    VALUES (p_veiculo_id, p_data_inicio, 0.0);

    UPDATE Veiculos SET status = 'Manutenção' WHERE id = p_veiculo_id;
END //

-- Stored Procedure 4: Finaliza uma locação e calcula eventuais multas/custos
CREATE PROCEDURE SP_FinalizarLocacao(
    IN p_locacao_id INT,
    IN p_data_devolucao REAL DATE,
    IN p_custo_adicional DECIMAL(10, 2)
)
BEGIN
    DECLARE v_valor_base DECIMAL(10, 2);
    DECLARE v_data_prevista DATE;
    DECLARE v_dias_atraso INT;
    DECLARE v_multa DECIMAL(10, 2) DEFAULT 0.0;
    DECLARE v_veiculo_id INT;

    SELECT valor_total, data_fim_prevista, veiculo_id 
    INTO v_valor_base, v_data_prevista, v_veiculo_id
    FROM Locacoes 
    WHERE id = p_locacao_id;

    SET v_dias_atraso = DATEDIFF(p_data_devolucao, v_data_prevista);

    IF v_dias_atraso > 0 THEN
        SET v_multa = (v_valor_base / DATEDIFF(v_data_prevista, (SELECT data_inicio FROM Locacoes WHERE id = p_locacao_id))) * 0.5 * v_dias_atraso;
    END IF;

    UPDATE Locacoes SET 
        data_fim_real = p_data_devolucao, 
        valor_total = v_valor_base + v_multa + p_custo_adicional,
        status = 'FINALIZADA'
    WHERE id = p_locacao_id;
    
    UPDATE Veiculos SET status = 'Disponível' WHERE id = v_veiculo_id;
END //

DELIMITER ;


DELIMITER //

-- Trigger 1: Histórico de Preços
CREATE TRIGGER TRG_LogAlteracaoPreco
AFTER UPDATE ON Veiculos
FOR EACH ROW
BEGIN
    IF OLD.preco_diaria_base <> NEW.preco_diaria_base THEN
        INSERT INTO Log_Precos (veiculo_id, preco_antigo, preco_novo, data_alteracao, usuario)
        VALUES (OLD.id, OLD.preco_diaria_base, NEW.preco_diaria_base, NOW(), USER());
    END IF;
END //

-- Trigger 2: Validação de Data 
CREATE TRIGGER TRG_ValidarDataLocacao
BEFORE INSERT ON Locacoes
FOR EACH ROW
BEGIN
    IF NEW.data_fim_prevista <= NEW.data_inicio THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ERRO: A data de devolução deve ser posterior à data de retirada.';
    END IF;
END //

-- Trigger 3: Gerenciamento de Estoque de Acessórios 
CREATE TRIGGER TRG_DecrementoEstoqueAcessorio
AFTER INSERT ON veiculo_acessorio 
FOR EACH ROW
BEGIN
    DECLARE v_estoque_anterior INT;
    
    SELECT estoque INTO v_estoque_anterior FROM Acessorios WHERE id = NEW.acessorio_id;

    UPDATE Acessorios SET estoque = estoque - 1 WHERE id = NEW.acessorio_id;
    
    INSERT INTO Log_Estoque (acessorio_id, quantidade_anterior, quantidade_nova, tipo_operacao, data_log)
    VALUES (NEW.acessorio_id, v_estoque_anterior, v_estoque_anterior - 1, 'DECREMENTO', NOW());
END //

DELIMITER ;