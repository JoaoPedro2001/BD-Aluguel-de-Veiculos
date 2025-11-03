# BD-Aluguel-de-Veiculos
Banco de dados usado no sistema de aluguel de veículos para uma locadora de automóveis

Instruções de como aplicar o o banco de dados:
1. rode o arquivo database.py para gerar o banco de dados;
2. rode o arquivo create_tables.py para gerar as tabelas;
3. rode o arquivo tabela.py para popular as tabelas com um conjunto de dados pré-criados;
4. Rode os comandos presentes no arquivo locadora_logic.sql para criar os triggers e stored procedures.

OBS.: em database.py, para que o banco de dados seja gerado no MySQL, é necessaria a troca da senha para a do servidor MySQL usado no dispositivo:

MYSQL_PASSWORD = "Adicione senha aqui"
