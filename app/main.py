from app.database import init_db
from app.ui.startWindow import StartWindow


def main() -> None:
    init_db()
    app = StartWindow()
    app.mainloop()


if __name__ == "__main__":
    main()