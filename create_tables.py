from database import engine, DBModel

def main():
    from models import (
        Cliente, Atendente, Veiculo,
        Categoria, Seguro, Reserva,
        Pagamento, Manutencao, Multa,
        reserva_seguro
    )

    with engine.connect() as conn:
        DBModel.metadata.drop_all(conn)
        DBModel.metadata.create_all(conn)

if __name__ == '__main__':
    main()