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