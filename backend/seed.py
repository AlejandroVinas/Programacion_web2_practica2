from app.database import init_db

if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada. Usuarios: admin/admin123 y user/user123")
