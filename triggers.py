from sqlalchemy import text
from database import engine


def create_triggers():
    sql_script = """
    DELIMITER //

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

    """

    with engine.connect() as conn:
        for statement in sql_script.split("//"):
            stmt = statement.strip()

            if stmt:
                conn.execute(text(stmt))

    conn.commit

if __name__ == "__main__":
    create_triggers()
    print("Triggers criados com sucesso!")