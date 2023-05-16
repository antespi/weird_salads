from database import Base, engine, get_db, Session

# Create database schema
Base.metadata.create_all(bind=engine)
