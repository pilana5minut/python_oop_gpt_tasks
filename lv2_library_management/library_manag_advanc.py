class Book:

    def __init__(self, title: str, author: str, status: bool = True) -> None:
        """Инициализирует объект класса книга.
        Args:
            title (str): Строка с названием книги
            author (str): Строка с ФИО автора
            status (bool, optional): Статус отражающий наличие книги. Defaults to True.
        """
        self.title = title
        self.author = author
        self.status = status
        self.borrower = None

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
        print(f'Название: {self.title}')
        print(f'Автор: {self.author}')
        print(f'Статус: {self.get_status()}')
        if (self.borrower):
            print(f'Кем арендована: {self.borrower}')
            print(f'---------------')

#######################################################################


class Reader:

    def __init__(self, name: str, id: int) -> None:
        """Инициализирует объект класса читатель.
        Args:
            name (str): Имя читателя.
            id (int): Уникальный идентификатор читателя.
        """
        self.name = name
        self.id = id
        self.borrowed_books = []

#######################################################################


class Library:

    def __init__(self, limit: int) -> None:
        """Инициализирует объект класса библиотека.
        Args:
            limit (int): Число указывающее лимит книг которые читатель может взять.
        """
        self.lib = []
        self.readers = []
        self.borrow_history = []
        self.rental_limit = limit

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

    def is_register(self, reader_obj: Reader) -> bool:
        """Проверяет регистрацию читателя.
        Args:
            reader_obj (Reader): Экземпляр объекта Reader.
        Returns:
            bool: True или False соответственно.
        """
        for rd in self.readers:
            if (rd.name == reader_obj.name):
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
        count_print = 0
        for b in list_books:
            count_print += 1
            print('')
            print(f'''{count_print}.''')
            b.print_info_book()

    def register_reader(self, reader: Reader) -> None:
        """Регистрирует нового читателя в библиотеке.
        Args:
            reader (Reader): Экземпляр объекта Reader.
        """
        if (isinstance(reader, Reader) and not self.is_register(reader)):
            self.readers.append(reader)
            print(f'Читатель с именем "{
                  reader.name}" был успешно зарегистрирован.')

    def add_book(self, book_obj: Book) -> None:
        """Добавляет книгу в библиотеку.
        Args:
            book_obj (Book): Экземпляр объекта Book.
        """
        if (isinstance(book_obj, Book) and not self.is_stock(book_obj)):
            self.lib.append(book_obj)
            print('Книга была успешно зарегистрирована в библиотеке.')
            print(f'Название: {book_obj.title}')
            print(f'Автор: {book_obj.author}')
            # print(f'Статус: {book_obj.get_status()}')
            print('')

    def borrow_book(self, title: str, reader: str) -> None:
        """Выдает книгу читателю, если она в наличии.
        Args:
            title (str): Называние книги
            reader (str): Имя читателя
        """
        book_obj = None
        reader_obj = None
        book_status = None
        reader_status = None

        for b in self.lib:
            if (b.title == title):
                book_obj = b

        for rd in self.readers:
            if (rd.name == reader.capitalize()):
                reader_obj = rd

        if (book_obj is None):
            print(f'Книга "{title}" НЕ зарегистрирована')
            return
        elif (book_obj.status):
            book_status = True
        else:
            book_status = False

        if (reader_obj is None):
            print(f'Читатель по имени "{reader}" НЕ зарегистрирован')
        elif (len(reader_obj.borrowed_books) < self.rental_limit):
            reader_status = True
        else:
            print(f'У читателя "{reader_obj.name}" достигнут ЛИМИТ выдачи: {
                self.rental_limit} книги.')
            reader_status = False

        if (book_status and reader_status):
            book_obj.status = False
            book_obj.borrower = reader_obj.name
            reader_obj.borrowed_books.append(book_obj)
            self.add_borrow_history(reader_obj)
            print(f'Книга "{book_obj.title}" была ВЫДАНА читателю по имени "{
                reader_obj.name}".')
        elif (not book_status):
            print(f'Книги "{title}" нет в наличии.')
            print(f'Книга "{title}" в данный момент у читателя "{
                  book_obj.borrower}".')

    def return_book(self, title: str, reader: str) -> None:
        """Возвращает книгу в библиотеку.
        Args:
            title (str): Строка с название книги.
            reader (str): Строка с именем читателя.
        """
        book_obj = None
        reader_obj = None
        book_status = None
        reader_status = None

        for b in self.lib:
            if (b.title == title):
                book_obj = b

        for rd in self.readers:
            if (rd.name == reader.capitalize()):
                reader_obj = rd

        if (book_obj is None):
            print(f'Книга "{title}" НЕ зарегистрирована')
            return
        else:
            book_status = True

        if (reader_obj is None):
            print(f'Читатель по имени "{reader}" НЕ зарегистрирован')
        elif (book_obj in reader_obj.borrowed_books):
            reader_status = True
        else:
            reader_status = False
            print(f'Книга "{book_obj.title}" НЕ числится в списке читателя {
                reader_obj.name}')

        if (book_status and reader_status):
            book_obj.status = True
            book_obj.borrower = None
            reader_obj.borrowed_books.remove(book_obj)
            print(f'Книга "{book_obj.title}" была ВОЗВРАЩЕНА читателем {
                reader_obj.name}.')

    def get_book_status(self, title: str) -> None:
        """Выводит информацию о статусе книги и у какого читателя она находится.
        Args:
            title (str): Строка с название книги.
        """
        for b in self.lib:
            if (b.title == title):
                b.print_info_book()

    def list_reader_books(self, reader: str) -> None:
        """Распечатывает список книг конкретного читателя.
        Args:
            reader (str): Строка с именем читателя.
        """
        reader_obj = None

        for rd in self.readers:
            if (rd.name == reader.capitalize()):
                reader_obj = rd

        print(f'У читателя "{reader_obj.name}" в данный момент {
              len(reader_obj.borrowed_books)} книг на руках.')
        self.print_list_book(reader_obj.borrowed_books)

    def search_book(self, prompt: str) -> None:
        """Ищет книгу среди всех зарегистрированных по названию или автору.\n
        Не чувствителен к регистру.\n
        Args:
            prompt (str): Строка содержащая название книги или автора.
        """
        count_match = 0
        match_list = []
        borrower_list = set()

        for b in self.lib:
            current_book = f'{b.title} {b.author}'
            if (prompt.lower() in current_book.lower()):
                count_match += 1
                match_list.append(b)

        for b in match_list:
            if (not b.status):
                borrower_list.add(b.borrower)

        print(f'По запросу "{prompt}" найдено {count_match} книг:')
        self.print_list_book(match_list)

        if (len(borrower_list) > 0):
            print(f'Одна или несколько книг в данный момент у читателей')
            for rd in borrower_list:
                print(f'{rd}')
            current_reader = input('Для показа списка введите имя читателя:')
            self.list_reader_books(current_reader.capitalize())

    def show_status_library(self) -> None:
        """Отображает текущее состояние всех книг в библиотеке."""
        in_stock = 0
        out_stock = 0
        for b in self.lib:
            if (b.status):
                in_stock += 1
            else:
                out_stock += 1
        print(f'Книг всего зарегистрировано: {len(self.lib)}')
        print(f'Книг в наличии: {in_stock}')
        print(f'Книг выдано читателю: {out_stock}')

    def add_borrow_history(self, reader_obj: Reader) -> None:
        """Добавляет читателя в историю библиотеки.
        Args:
            reader_obj (Reader): Экземпляр объекта читатель.
        """
        if (reader_obj not in self.borrow_history):
            self.borrow_history.append(reader_obj)

    def show_borrow_history(self):
        """Распечатывает список читателей которые брали книги."""
        for rd in self.borrow_history:
            print(f'{rd.name}')

    def show_nomenclature(self, status: bool = None) -> None:
        """Распечатывает тот или иной список книг в зависимости от аргумента.\n
        Без аргумента: Список всех зарегистрированных в библиотеке книг.\n
        True: Список книг имеющихся в наличии библиотеки.\n
        False: Список книг выданных читателю на данный момент\n
        Args:
            status (bool, optional): Флаг обозначающий тот или иной список.
        """
        in_stock = []
        out_stock = []
        for b in self.lib:
            if (b.status):
                in_stock.append(b)
            else:
                out_stock.append(b)
        if (status):
            print(f'Книги в наличии: {len(in_stock)}')
            self.print_list_book(in_stock)
        elif (status is False):
            print(f'Книги выданные читателям: {len(out_stock)}')
            self.print_list_book(out_stock)
        else:
            print(f'Книг всего зарегистрировано: {len(self.lib)}')
            self.print_list_book(self.lib)


#######################################################################

library = Library(4)

b1 = Book("FastAPI", "Билл Любанович")
b2 = Book("Простой Python", "Билл Любанович")
b3 = Book("Чистый код", "Роберт Мартин")
b4 = Book("Идеальная работа", "Роберт Мартин")
b5 = Book("Идеальный программист", "Роберт Мартин")
b6 = Book("Изучаем Python", "Марк Лутц")
b7 = Book("Python Карманный справочник", "Марк Лутц")
b8 = Book("ES6 и не только", "Кайл Симпсон")
b9 = Book("Замыкания и объекты", "Кайл Симпсон")
b10 = Book("Познакомьтесь, JavaScript", "Кайл Симпсон")
b11 = Book("Изучаем SQL", "Алан Бьюли")
b12 = Book("Django 4 в примерах", "Антонио Меле")
b13 = Book("Linux Книга рецептов", "Карла Шрёдер")
b14 = Book("jQuery в действии", "Аурелио де Роза")
b15 = Book("Внутреннее устройство Linux", "Дмитрий Кетов")
b16 = Book("Внутреннее устройство Linux", "Дмитрий Кетов")

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
library.add_book(b12)
library.add_book(b13)
library.add_book(b14)
library.add_book(b15)
library.add_book(b16)

r1 = Reader('Alice', 123)
r2 = Reader('Bob', 456)
r3 = Reader('Eve', 789)

library.register_reader(r1)
library.register_reader(r2)
library.register_reader(r3)

# library.show_status_library()

# library.borrow_book('Изучаем Python', 'Alice')
# library.borrow_book('Изучаем SQL', 'Alice')
# library.borrow_book('Чистый код', 'Alice')
# library.borrow_book('Идеальный программист', 'Alice')

# library.borrow_book('Идеальная работа', 'Bob')
# library.borrow_book('ES6 и не только', 'Bob')
# library.borrow_book('Замыкания и объекты', 'Bob')

# library.borrow_book('Простой Python', 'Eve')
# library.borrow_book('Внутреннее устройство Linux', 'Eve')
