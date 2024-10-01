class Book:

    def __init__(self, title: str, author: str,  id: int, status: bool = True) -> None:
        """Инициализирует объект класса книга.
        Args:
            title (str): Строка с названием книги
            author (str): Строка с ФИО автора
            status (bool, optional): Статус отражающий наличие книги. Defaults to True.
        """

        self.title = title
        self.author = author
        self.id = id
        self.status = status
        self.borrower = None

    def get_status_book(self):
        """Возвращает строку описывающую статус книги в удобочитаемом формате.
        Returns:
            str: Строка отражающая статус книги.
        """

        if (self.status):
            return 'В наличии'
        else:
            return 'У читателя'

    def get_info_book(self):
        """Возвращает строку содержащую информацию о книге.
        Returns:
            str: Строка с информацией о книге.
        """

        if self.borrower is None:
            return f'Название: {self.title}\nАвтор: {self.author}\nСтатус: {self.get_status_book()}\nid: {self.id}'
        else:
            return f'Название: {self.title}\nАвтор: {self.author}\nСтатус: {self.get_status_book()}\nid: {self.id}\nКем арендована: {self.borrower}'


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

        self.lib = dict()
        self.readers = dict()
        self.borrow_history = []
        self.rental_limit = limit

    def print_list_book(self, list_books: list) -> None:
        """Распечатывает список книг в формате:\n
        Название: ...\n
        Автор: ...\n
        Статус: ...\n
        id: ...\n
        Кем арендована: ...\n
        Args:
            list_books (list): Список экземпляров класса Book.
        """

        count_print = 0
        for b in list_books:
            count_print += 1
            print('')
            print(f'''{count_print}.''')
            print(b.get_info_book())

    def register_reader(self, reader_obj: Reader) -> None:
        """Регистрирует нового читателя в библиотеке.
        Args:
            reader (Reader): Экземпляр объекта Reader.
        """

        if isinstance(reader_obj, Reader) and reader_obj.id not in self.readers:
            self.readers[reader_obj.id] = reader_obj
            print(f'Читатель по имени "{
                  reader_obj.name}" БЫЛ ЗАРЕГИСТРИРОВАН под номером {reader_obj.id}.')
        elif not isinstance(reader_obj, Reader):
            print('Переданный аргумент НЕ ЯВЛЯЕТСЯ объектом ЧИТАТЕЛЯ.')
        elif reader_obj.id in self.readers:
            print(f'''Читатель с id: {
                reader_obj.id} уже БЫЛ ЗАРЕГИСТРИРОВАН в библиотеке ранее.''')

    def add_book(self, book_obj: Book) -> None:
        """Добавляет книгу в библиотеку.
        Args:
            book_obj (Book): Экземпляр объекта Book.
        """

        if isinstance(book_obj, Book) and book_obj.id not in self.lib:
            self.lib[book_obj.id] = book_obj
            print('Книга БЫЛА ЗАРЕГИСТРИРОВАНА в библиотеке.')
            print(book_obj.get_info_book())
            print('')
            return
        elif not isinstance(book_obj, Book):
            print('Переданный аргумент НЕ ЯВЛЯЕТСЯ объектом КНИГИ.')
        elif book_obj.id in self.lib:
            print(f'''Книга с id: {book_obj.id} УЖЕ ЗАРЕГИСТРИРОВАНА.''')

    def get_book_by_id(self, book_id: int):
        """Возвращает объект книги или None.
        Args:
            book_id (int): Уникальный идентификатор книги
        Returns:
            object: Объект класса Book
        """

        return self.lib.get(book_id)

    def get_reader_by_id(self, reader_id: int):
        """Возвращает объект читателя или None.
        Args:
            reader_id (int): Уникальный идентификатор читателя
        Returns:
            object: Объект класса Reader
        """

        return self.readers.get(reader_id)

    def borrow_book(self, book_id: int, reader_id: int) -> None:
        """Выдает книгу читателю, если она в наличии.
        Args:
            book_id (int): Уникальный идентификатор книги
            reader_id (int): Уникальный идентификатор читателя
        """

        book_obj = self.get_book_by_id(book_id)
        reader_obj = self.get_reader_by_id(reader_id)
        book_status = None
        reader_status = None

        if (book_obj is None):
            print(f'Книга c id: "{book_id}" НЕ зарегистрирована')
            return
        elif (book_obj.status):
            book_status = True
        else:
            book_status = False

        if (reader_obj is None):
            print(f'Читатель с id: "{reader_id}" НЕ зарегистрирован')
        elif (len(reader_obj.borrowed_books) < self.rental_limit):
            reader_status = True
        else:
            print(f'У читателя "{reader_obj.name}" ДОСТИГНУТ ЛИМИТ выдачи: {
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
            print(f'Книги "{book_obj.title}" нет в наличии.')
            print(f'Книга "{book_obj.title}" в данный момент у читателя "{
                  book_obj.borrower}".')

    def return_book(self, book_id: int, reader_id: int) -> None:
        """Возвращает книгу в библиотеку.
        Args:
            book_id (int): Уникальный идентификатор книги
            reader_id (int): Уникальный идентификатор читателя
        """

        book_obj = self.get_book_by_id(book_id)
        reader_obj = self.get_reader_by_id(reader_id)
        book_status = None
        reader_status = None

        if (book_obj is None):
            print(f'Книга c id: "{book_id}" НЕ зарегистрирована')
            return
        else:
            book_status = True

        if (reader_obj is None):
            print(f'Читатель с id: "{reader_id}" НЕ зарегистрирован')
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
                reader_obj.name}".')

    def get_book_status(self, book_id: int) -> None:
        """Выводит информацию о статусе книги и у какого читателя она находится.
        Args:
            title (str): Строка с название книги.
        """

        print(self.get_book_by_id(book_id).get_info_book())

    def list_reader_books(self, reader_id: int) -> None:
        """Распечатывает список книг конкретного читателя.
        Args:
            reader (str): Строка с именем читателя.
        """

        reader_obj = self.get_reader_by_id(reader_id)

        if reader_obj is None:
            print(f'Читатель с id: "{reader_id}" НЕ зарегистрирован')
        else:
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

        for b in self.lib.values():
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

    def show_nomenclature_book(self, status: bool = None) -> None:
        """Распечатывает тот или иной список книг в зависимости от аргумента.\n
        Без аргумента: Список всех зарегистрированных в библиотеке книг.\n
        True: Список книг имеющихся в наличии библиотеки.\n
        False: Список книг выданных читателю на данный момент\n
        Args:
            status (bool, optional): Флаг обозначающий тот или иной список.
        """

        in_stock = []
        out_stock = []

        for v in self.lib.values():
            if (v.status):
                in_stock.append(v)
            else:
                out_stock.append(v)

        if (status):
            print(f'Книги в наличии: {len(in_stock)}')
            self.print_list_book(in_stock)
            print('')
            print(f'Книги в наличии: {len(in_stock)}')
        elif (status is False):
            print(f'Книги выданные читателям: {len(out_stock)}')
            self.print_list_book(out_stock)
            print('')
            print(f'Книги выданные читателям: {len(out_stock)}')
        else:
            print(f'Книг всего зарегистрировано: {len(self.lib)}')
            self.print_list_book(list(self.lib.values()))
            print('')
            print(f'Книг всего зарегистрировано: {len(self.lib)}')


# Тесты ###############################################################

print('-------- Создаем Библиотеку')
library = Library(4)
print('')

print('-------- Создаем Книги')
b1 = Book("FastAPI", "Билл Любанович", 1)
b2 = Book("Простой Python", "Билл Любанович", 2)
b3 = Book("Чистый код", "Роберт Мартин", 3)
b4 = Book("Идеальная работа", "Роберт Мартин", 4)
b5 = Book("Идеальный программист", "Роберт Мартин", 5)
b6 = Book("Изучаем Python", "Марк Лутц", 6)
b7 = Book("Python Карманный справочник", "Марк Лутц", 7)
b8 = Book("ES6 и не только", "Кайл Симпсон", 8)
b9 = Book("Замыкания и объекты", "Кайл Симпсон", 9)
b10 = Book("Познакомьтесь, JavaScript", "Кайл Симпсон", 10)
b11 = Book("Изучаем SQL", "Алан Бьюли", 11)
b12 = Book("Django 4 в примерах", "Антонио Меле", 12)
b13 = Book("Linux Книга рецептов", "Карла Шрёдер", 13)
b14 = Book("jQuery в действии", "Аурелио де Роза", 14)
b15 = Book("Внутреннее устройство Linux", "Дмитрий Кетов", 15)
b16 = Book("Внутреннее устройство Linux", "Дмитрий Кетов", 15)  # Duplicate
print('')

print('-------- Регистрируем Книги в библиотеке')
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
library.add_book('Caramba!')
print('')

print('-------- Показываем список Книг')
for k, v in library.lib.items():
    print(f'{k}: {v.title} - {v.author} - {v.status}')
print('')


print('-------- Создаем Читателей')
r1 = Reader('Alice', 123)
r2 = Reader('Bob', 456)
r3 = Reader('Eve', 789)
r4 = Reader('Eve', 789)  # Duplicate
print('')

print('-------- Регистрируем Читателей в библиотеке')
library.register_reader(r1)
library.register_reader(r2)
library.register_reader(r3)
library.register_reader(r4)
library.register_reader('Caramba!')
print('')

print('-------- Показываем список Читателей')
for k, v in library.readers.items():
    print(f'{k}: {v.name} - {v.borrowed_books}')
print('')


print('-------- Выдаем Книги Читателям')
library.borrow_book(1, 123)
library.borrow_book(2, 123)
library.borrow_book(3, 123)
library.borrow_book(4, 123)
library.borrow_book(5, 456)
library.borrow_book(6, 456)
library.borrow_book(7, 456)
library.borrow_book(8, 456)
library.borrow_book(9, 789)
library.borrow_book(10, 789)
library.borrow_book(11, 789)
library.borrow_book(12, 789)
library.borrow_book(13, 123)
library.borrow_book(14, 456)
library.borrow_book(15, 789)

library.borrow_book(7, 246)  # Fake
library.borrow_book(42, 246)  # Fake
print('')

print('-------- Читатели возвращают книги')
library.return_book(13, 123)
library.return_book(14, 456)
library.return_book(15, 789)

library.return_book(7, 246)  # Fake
library.return_book(42, 246)  # Fake
print('')
