from app.database import init_db
from app.service import ProductService
from app.ui.mainWindow import MainWindow

def main() -> None:
    init_db()
    service = ProductService()
    app = MainWindow(service)
    app.mainloop()

if __name__ == "__main__":
    main()