'''
Script con lista de instrucciones denominda 'instructions' con la cual se genera la base de datos MYSQL en donde primar para este programa 
la tabla usuario y pedido. Las lineas previas a la creación de tablas se aseguran de que no existan previamente borrando adecuadamente las
llaves foraneas y las tablas en si.
'''

instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS Usuario;',
    'DROP TABLE IF EXISTS Pedido;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE Usuario(
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            address VARCHAR(100) NOT NULL,
            phone VARCHAR(10) NOT NULL
        );
    """,
    """
        CREATE TABLE Pedido(
            id INT PRIMARY KEY AUTO_INCREMENT,
            ordered_by INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            amount INT NOT NULL,
            delivered BOOLEAN NOT NULL,
            pay_method TEXT,
            FOREIGN KEY (ordered_by) REFERENCES Usuario (id)
        );
    """
]