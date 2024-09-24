class Book:

    def __init__(self, title: str, author: str, status: bool = True) -> None:
        self.title = title
        self.author = author
        self.status = status

    def get_status(self):
        """Возвращает статус книги в удобочитаемом формате.
        Returns:
            str: Строка описывающая статус книги в удобочитаемом формате.
        """
        if (self.status):
            return 'В наличии'
        else:
            return 'У читателя'

    def print_info_book(self):
        """Распечатывает сводную информация о книге."""
        print(f'''
            Название: {self.title}
            Автор: {self.author}
            Статус: {self.get_status()}''')


#######################################################################


class Library:
    def __init__(self) -> None:
        self.lib = []

    def is_stock(self, book_obj: Book) -> bool:
        """Проверяет регистрацию книги.
        Args:
            book_obj (Book): Экземпляр объекта Book.
        Returns:
            bool: True или False соответственно.
        """
        for b in self.lib:
            if (b.title == book_obj.title):
                return True
        return False

    def print_list_book(self, list_books: list) -> None:
        """Распечатывает список книг в формате:\n
        Название: ...\n
        Автор: ...\n
        Статус: ...\n
        Args:
            list_books (list): Список экземпляров класса Book.
        """
        for b in list_books:
            b.print_info_book()

    def add_book(self, book_obj: Book) -> None:
        """Добавляет книгу в библиотеку.
        Args:
            book_obj (Book): Экземпляр объекта Book.
        """
        if (isinstance(book_obj, Book) and not self.is_stock(book_obj)):
            self.lib.append(book_obj)
            print('Книга была успешно зарегистрирована в библиотеке.')
            self.print_list_book([book_obj])

    def out_book(self, title_book: str) -> None:
        """Выдает книгу пользователю.
        Args:
            title_book (str): Строка с название книги.
        """
        for b in self.lib:
            if (b.title == title_book and b.status == True):
                b.status = False
                print('Книга была выдана читателю.')
                self.print_list_book([b])
                return
            elif (b.title == title_book and b.status == False):
                print('Книга в данный момент у читателя.')
                self.print_list_book([b])
                return
        print('Книга с таким название не зарегистрирована в библиотеке.')

    def return_book(self, title_book: str) -> None:
        """Возвращает книгу в библиотеку.
        Args:
            title_book (str): Строка с название книги.
        """
        for b in self.lib:
            if (b.title == title_book):
                b.status = True
                print('Книга была возвращена в библиотеку.')
                self.print_list_book([b])
        print('Книга с таким название не зарегистрирована в библиотеке.')

    def search_book(self, prompt: str) -> None:
        """Ищет книгу среди всех зарегистрированных по названию или автору.\n
        Не чувствителен к регистру.\n
        Args:
            prompt (str): Строка содержащая название книги или автора.
        """
        match_count = 0
        match_list = []
        for b in self.lib:
            current_book = f'{b.title} {b.author}'
            if (prompt.lower() in current_book.lower()):
                match_count += 1
                match_list.append(b)
        print(f"Найдено {match_count} совпадений")
        self.print_list_book(match_list)

    def show_status_library(self) -> None:
        """Отображает текущее состояние всех книг в библиотеке."""
        all_stock = len(self.lib)
        in_stock = 0
        out_stock = 0
        for b in self.lib:
            if (b.status):
                in_stock += 1
            else:
                out_stock += 1
        print(f'Книг всего зарегистрировано: {all_stock}')
        print(f'Книг в наличии: {in_stock}')
        print(f'Книг выдано читателю: {out_stock}')

    def show_nomenclature(self, status: bool = None) -> None:
        """Распечатывает тот или иной список книг в зависимости от аргумента.\n
        Без аргумента: Список всех зарегистрированных в библиотеке книг.\n
        True: Список книг имеющихся в наличии библиотеки.\n
        False: Список книг выданных читателю на данный момент\n
        Args:
            status (bool, optional): Флаг обозначающий тот или иной список.
        """
        status
        all_stock = []
        in_stock = []
        out_stock = []
        for b in self.lib:
            all_stock.append(b)
            if (b.status == True):
                in_stock.append(b)
            else:
                out_stock.append(b)
        if (status == True):
            print(f'Книги в наличии: {len(in_stock)}')
            self.print_list_book(in_stock)
        elif (status == False):
            print(f'Книги выданные читателю: {len(out_stock)}')
            self.print_list_book(out_stock)
        elif (status == None):
            print(f'Книг всего зарегистрировано: {len(all_stock)}')
            self.print_list_book(all_stock)


#######################################################################

b1 = Book("FastAPI", "Билл Любанович")
b2 = Book("Простой Python", "Билл Любанович")
b3 = Book("Чистый код", "Роберт Мартин")
b4 = Book("Идеальная работа", "Роберт Мартин")
b5 = Book("Идеальный программист", "Роберт Мартин")
b6 = Book("Изучаем Python", "Марк Лутц")
b7 = Book("Python Карманный справочник", "Марк Лутц")
b8 = Book("Linux Книга рецептов", "Карла Шрёдер")
b9 = Book("Внутреннее устройство Linux", "Дмитрий Кетов")
b10 = Book("Django 4 в примерах", "Антонио Меле")
b11 = Book("Django 4 в примерах", "Антонио Меле")

library = Library()

library.add_book(b1)
library.add_book(b2)
library.add_book(b3)
library.add_book(b4)
library.add_book(b5)
library.add_book(b6)
library.add_book(b7)
library.add_book(b8)
library.add_book(b9)
library.add_book(b10)
library.add_book(b11)

library.show_status_library()
