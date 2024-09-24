class Book:

    def __init__(self, title: str, author: str, year: int) -> None:
        self.title = title
        self.author = author
        self.year = year

    def get_info_book(self):
        """Метод для вывода информации о книге в удобочитаемом формате."""
        return f"Название:{self.title} - Автор:{self.author} - Год издания:{self.year}"

#######################################################################


class Library:
    def __init__(self) -> None:
        self.lib = []

    def add_book(self, book: Book) -> None:
        """Метод для добавления книги в библиотеку."""
        if (isinstance(book, Book)):
            self.lib.append(book)
        else:
            print('Не является книгой')

    def show_all_books(self) -> None:
        """Метод для отображения всех книг в библиотеке."""
        for b in self.lib:
            print(b.get_info_book())

    def search_book(self, prompt: str) -> None:
        """Метод для поиска книги по названию или автору."""
        answer = []
        for b in self.lib:
            if (prompt.lower() in f'{b.title} {b.author}'.lower()):
                answer.append(b)

        if (len(answer) != 0):
            print(f'Найдено совпадений {len(answer)}')
            for b in answer:
                print(b.get_info_book())
        else:
            print(f'Найдено совпадений {len(answer)}')

#######################################################################


b1 = Book("Простой Python", "Билл Любанович", 2021)
b2 = Book("FastAPI", "Билл Любанович", 2024)
b3 = Book("Внутреннее устройство Linux", "Дмитрий Кетов", 2021)
b4 = Book("Linux Книга рецептов", "Карла Шрёдер", 2022)
b5 = Book("Чистый код", "Роберт Мартин", 2024)
b6 = Book("Идеальная работа", "Роберт Мартин", 2022)
b7 = Book("Идеальный программист", "Роберт Мартин", 2015)

library = Library()

library.add_book(b1)
library.add_book(b2)
library.add_book(b3)
library.add_book(b4)
library.add_book(b5)
library.add_book(b6)
library.add_book(b7)
