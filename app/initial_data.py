from app.database import engine, create_db_and_tables
from app.models.author import Author
from app.models.book import Book
from app.models.publisher import Publisher
from app.models.user import User
from app.models.loan import Loan
from sqlmodel import Session
from datetime import date, timedelta

def seed_database():
    # Crear tablas si no existen
    create_db_and_tables()
    
    with Session(engine) as session:
        # Crear autores
        author1 = Author(name="J.R.R. Tolkien", birth_date=date(1892, 1, 3), nationality="British")
        author2 = Author(name="George Orwell", birth_date=date(1903, 6, 25), nationality="British")
        
        # Crear editoriales
        publisher1 = Publisher(name="Allen & Unwin", founding_year=1936)
        publisher2 = Publisher(name="Secker & Warburg", founding_year=1936)
        
        # Crear libros
        book1 = Book(
            title="The Hobbit",
            isbn="978-0547928227",
            publication_year=1937,
            author=author1,
            publisher=publisher1
        )
        book2 = Book(
            title="1984",
            isbn="978-0451524935",
            publication_year=1949,
            author=author2,
            publisher=publisher2
        )
        
        # Crear usuarios
        user1 = User(name="John Doe", email="john@example.com")
        user2 = User(name="Jane Smith", email="jane@example.com")
        
        # Crear préstamos
        loan1 = Loan(
            book=book1,
            user=user1,
            loan_date=date.today() - timedelta(days=10),
            due_date=date.today() + timedelta(days=20)
        )
        loan2 = Loan(
            book=book2,
            user=user2,
            loan_date=date.today() - timedelta(days=5),
            due_date=date.today() + timedelta(days=15),
            return_date=date.today()  # Libro ya devuelto
        )
        
        # Añadir todos los objetos a la sesión
        session.add_all([author1, author2, publisher1, publisher2, book1, book2, user1, user2, loan1, loan2])
        session.commit()

if __name__ == "__main__":
    seed_database()
    print("✅ Base de datos inicializada con datos de prueba!")