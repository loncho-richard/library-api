# library-api
Technical challenge for the PWC recruitment process, using the FastAPI framework


# Mermaid of DB
erDiagram
    AUTHORS ||--o{ BOOKS : "escribe"
    PUBLISHERS ||--o{ BOOKS : "publica"
    BOOKS ||--o{ LOANS : "tiene"
    USERS ||--o{ LOANS : "realiza"
    
    AUTHORS {
        int id PK
        string name
        date birth_date
        string nationality
    }
    
    PUBLISHERS {
        int id PK
        string name
        int founding_year
    }
    
    BOOKS {
        int id PK
        string title
        string isbn
        int author_id FK
        int publisher_id FK
        int publication_year
    }
    
    USERS {
        int id PK
        string name
        string email
        date join_date
    }
    
    LOANS {
        int id PK
        int book_id FK
        int user_id FK
        date loan_date
        date due_date
        date return_date
    }