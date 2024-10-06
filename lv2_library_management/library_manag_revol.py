class Book:

    def __init__(self, title: str, author: str, id: int) -> None:
        """Инициализирует объект класса книга.
        Args:
            title (str): Строка с названием книги.
            author (str): Строка с ФИО автора.
            id (int): Уникальный идентификатор книги.
        """

        self.title = title
        self.author = author
        self.id = id
        self.status = True
        self.borrower = None

    def __str__(self) -> str:
        return f'Название: {self.title}\nАвтор: {self.author}\nИдентификатор: {self.id}\nСтатус: {'В наличии' if self.status else 'У читателя'}'

#######################################################################


class Reader:

    def __init__(self, name: str, id: int) -> None:
        """Инициализирует объект класса читатель.
        Args:
            name (str): Имя читателя.
            id (int): Уникальный идентификатор читателя.
        """

        self.name = name.capitalize()
        self.id = id
        self.borrowed_books = list()

    def __str__(self) -> str:
        return f'Имя: {self.name}\nИдентификатор: {self.id}'


#######################################################################


class Library:

    def __init__(self, limit: int) -> None:
        """Инициализирует объект класса библиотека.
        Args:
            limit (int): Число определяющее максимальное количество книг
        которые читатель может взять.
        """

        self.lib = dict()
        self.readers = dict()
        self.borrow_history = set()
        self.rental_limit = limit
        self.index_books_by_title = dict()
        self.index_books_by_author = dict()
        self.index_books_by_reader = dict()
        self.index_readers_by_name = dict()

    def add_book_in_index_by_author(self, book: Book) -> None:
        """Добавляет ID книги в словарь указатель по ключу имени автора. Если автор уже имеется в словаре, то по этому ключу добавляется список с ID всех книг данного автора.
        Args:
            book (Book): Экземпляр класса Book.
        """

        if book.author not in self.index_books_by_author:
            self.index_books_by_author[book.author] = book.id

        elif book.author in self.index_books_by_author:
            temp = self.index_books_by_author[book.author]

            if isinstance(temp, int):
                self.index_books_by_author[book.author] = list()
                self.index_books_by_author[book.author].append(temp)
                self.index_books_by_author[book.author].append(book.id)
            else:
                self.index_books_by_author[book.author].append(book.id)

    def find_book_by_title(self, title: str) -> Book:
        """Находит объект книги в основном словаре книг библиотеки.
        Args:
            title (str): Строка с название книги.
        Raises:
            LookupError: Возбуждает исключение если ID книги не найден в индексе index_books_by_title.
        Returns:
            Book: Объект класса Book.
        """

        book_id = self.index_books_by_title.get(title)

        if book_id is None:
            raise LookupError(f'ОТМЕНА: ID книги "{
                              title}" не найден в индексе: index_books_by_title')
        else:
            return self.lib[book_id]

    def find_books_by_author(self, author: str) -> Book | list:
        """Находит объект книги в основном словаре книг библиотеки.
        Args:
            author (str): Строка с именем автора.
        Raises:
            LookupError: Возбуждает исключение если ID книги не найден в индексе index_books_by_author.
        Returns:
            Book | list: Объект класса Book или список объектов класса Book.
        """

        book_id = self.index_books_by_author.get(author)

        if book_id is None:
            raise LookupError(f'ОТМЕНА: ID книги "{
                              author}" не найден в индексе: index_books_by_author')
        elif isinstance(book_id, int):
            return self.lib[book_id]
        elif isinstance(book_id, list):
            return [self.lib[book] for book in book_id]

    def find_reader_by_name(self, name: str) -> Reader:
        """Находит объект читателя в основном словаре читателей библиотеки.
        Args:
            name (str): Строка с именем читателя.
        Raises:
            LookupError: Возбуждает исключение если ID читателя не найден в индексе index_readers_by_name.
        Returns:
            Reader: Объект класса Reader.
        """

        reader_id = self.index_readers_by_name.get(name)

        if reader_id is None:
            raise LookupError(f'ОТМЕНА: ID читателя "{
                              name}" не найден в индексе: index_readers_by_name')
        else:
            return library.readers[reader_id]

    def add_book(self, book: Book) -> None:
        """Добавляет книгу в библиотеку.
        Args:
            book (Book): Экземпляр класса Book.
        """

        if isinstance(book, Book):
            self.lib[book.id] = book
            self.index_books_by_title[book.title] = book.id
            self.add_book_in_index_by_author(book)
            print(f'УСПЕХ: Книга "{
                book.title}" БЫЛА ДОБАВЛЕНА в библиотеку.')
        else:
            print(f'ОШИБКА: "{
                book}" НЕ ЯВЛЯЕТСЯ объектом книги.')

    def register_reader(self, reader: Reader) -> None:
        """Регистрирует нового читателя.
        Args:
            reader (Reader): Экземпляр класса Reader.
        """

        if isinstance(reader, Reader):
            self.readers[reader.id] = reader
            self.index_readers_by_name[reader.name] = reader.id
            print(f'УСПЕХ: Читатель по имени "{
                  reader.name}" БЫЛ ЗАРЕГИСТРИРОВАН в библиотеке.')
        else:
            print(f'ОШИБКА: "{
                  reader}" НЕ ЯВЛЯЕТСЯ объектом читателя.')

    def borrow_book(self, title: str, reader: str) -> None:
        """Выдает книгу читателю, если она в наличии.
        Args:
            title (str): Строка с названием книги.
            reader (str): Строка с именем читателя.
        """

        try:
            current_book = self.find_book_by_title(title)
            current_reader = self.find_reader_by_name(reader)
        except LookupError as e:
            print(f'{e}')
            return

        if current_book.status and len(current_reader.borrowed_books) < self.rental_limit:
            current_book.status = False
            current_book.borrower = current_reader
            current_reader.borrowed_books.append(current_book)
            self.borrow_history.add(current_reader.name)
            print(f'УСПЕХ: Книга "{current_book.title}" БЫЛА ВЫДАНА читателю "{
                current_reader.name}"')
        elif len(current_reader.borrowed_books) >= self.rental_limit:
            print(f'ОТМЕНА: Для читателя "{
                  current_reader.name}" был ДОСТИГНУТ ЛИМИТ.')
        else:
            print(f'ОТМЕНА: Книга "{current_book.title}" В ДАННЫЙ МОМЕНТ У ЧИТАТЕЛЯ "{
                current_book.borrower.name}"')

    def return_book(self, title, reader) -> None:
        """Возвращает книгу от читателя в библиотеку если она числится в списке читателя.
        Args:
            title (str): Строка с названием книги.
            reader (str): Строка с именем читателя.
        """

        try:
            current_book = self.find_book_by_title(title)
            current_reader = self.find_reader_by_name(reader)
        except LookupError as e:
            print(f'{e}')
            return

        if current_book.borrower is not None and current_book.borrower.name == current_reader.name:
            current_book.status = True
            current_book.borrower = None
            current_reader.borrowed_books.remove(current_book)
            print(f'УСПЕХ: Книга "{current_book.title}" БЫЛА ВОЗВРАЩЕНА читателем "{
                current_reader.name}"')
        else:
            print(f'ОТМЕНА: Книга "{current_book.title}" НЕ ЧИСЛИТСЯ в списке читателя "{
                current_reader.name}"')

    def get_book_status(self, title) -> None:
        """Выводит информацию о статусе книги и у какого читателя она находится если не в библиотеке.
        Args:
            title (str): Строка с названием книги.
        """

        current_book = self.find_book_by_title(title)

        print(current_book)
        if current_book.borrower is not None:
            print(f'Имя читателя: {current_book.borrower.name}\nИдентификатор читателя: {
                  current_book.borrower.id}')

    def list_reader_books(self, reader) -> None:
        """Выводит список книг, находящихся у читателя.
        Args:
            reader (str): Строка с именем читателя.
        """

        current_reader = self.find_reader_by_name(reader)
        count = 1

        print(f'За читателем по имени "{current_reader.name}" числится {
            len(current_reader.borrowed_books)} книг.')

        for b in current_reader.borrowed_books:
            print('')
            print(f'{count}.')
            count += 1
            print(b)

    def search_book(self, prompt: str) -> None:
        """Метод поиска книг, который позволит искать книги по названию, автору или по тому, у какого читателя она находится.
        """

        title_book = None
        author_book = None
        reader_name = None

        try:
            title_book = self.find_book_by_title(prompt)
        except LookupError:
            pass
        try:
            author_book = self.find_books_by_author(prompt)
        except LookupError:
            pass
        try:
            reader_name = self.find_reader_by_name(prompt)
        except LookupError:
            pass

        if title_book is not None or author_book is not None or reader_name is not None:

            if title_book is not None:
                print('--------------------------------')
                print(f'По запросу "{prompt}" найдено 1 книга.')
                print(title_book)

            if author_book is not None:
                print('--------------------------------')
                print(f'По запросу "{prompt}" найдено несколько ({
                    len(author_book)}) книг.')

                count = 1
                for b in author_book:
                    print('')
                    print(f'{count}.')
                    count += 1
                    print(b)

            if reader_name is not None:
                print('--------------------------------')
                print(f'По запросу "{
                      prompt}" найден читатель:\n{reader_name}')
                answer = input(f'Показать список книг читателя {
                               reader_name.name} (Y/n): ').lower()
                if answer == 'y' or answer == '':
                    self.list_reader_books(reader_name.name)
                    print('')
                else:
                    return

        else:
            print(f'По запросу "{prompt}" ни чего не найдено.')


# tests ###############################################################


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
b16 = Book("Внутреннее устройство Linux", "Дмитрий Кетов", 16)  # Duplicate
b17 = Book("Alice in Wonderland", "Льюис Кэрролл", 17)
b18 = Book("Yeah! Yeah! Yeah!", "Bob Stanley", 18)
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
library.add_book(b17)
library.add_book(b18)
library.add_book('b42')
print('')

print('-------- Показываем основной словарь Книг')
for k, v in library.lib.items():
    print(f'{k}: {v.title} - {v.author}')
print('')

print('-------- Показываем индекс Книг по автору')
for k, v in library.index_books_by_author.items():
    print(f'{k}: {v}')
print('')

#######################################################################


print('-------- Создаем Читателей')
r1 = Reader('Alice', 123)
r2 = Reader('Bob', 456)
r3 = Reader('Eve', 789)
print('')

print('-------- Регистрируем Читателей в библиотеке')
library.register_reader(r1)
library.register_reader(r2)
library.register_reader(r3)
library.register_reader('Chuck')
print('')

print('-------- Показываем основной словарь Читателей')
for k, v in library.readers.items():
    print(f'{k}: {v.name}')
print('')

print('-------- Показываем индекс Читателей по имени')
for k, v in library.index_readers_by_name.items():
    print(f'{k}: {v}')
print('')

#######################################################################


print('-------- Выдаем Книги Читателям')
library.borrow_book('FastAPI', 'Alice')
library.borrow_book('Простой Python', 'Alice')
library.borrow_book('Чистый код', 'Alice')
library.borrow_book('Идеальная работа', 'Alice')
library.borrow_book('Alice in Wonderland', 'Bob')
library.borrow_book('Изучаем Python', 'Bob')
library.borrow_book('Python Карманный справочник', 'Bob')
library.borrow_book('ES6 и не только', 'Bob')
library.borrow_book('Yeah! Yeah! Yeah!', 'Eve')
library.borrow_book('Познакомьтесь, JavaScript', 'Eve')
library.borrow_book('Изучаем SQL', 'Eve')
library.borrow_book('Django 4 в примерах', 'Eve')
library.borrow_book('Linux Книга рецептов', 'Alice')
library.borrow_book('jQuery в действии', 'Bob')
library.borrow_book('Внутреннее устройство Linux', 'Eve')
library.borrow_book('Внутреннее устройство Linux', 'Bob')  # !
library.borrow_book('Идеальный программист', 'Chukc')  # Fake
library.borrow_book('Замыкания и объекты', 'Eve')
library.borrow_book('Идеальный программист', 'Bob')
print('')

print('-------- Читатели возвращают книги')
library.return_book('Python Карманный справочник', 'Bob')
library.return_book('Чистый код', 'Alice')
library.return_book('Django 4 в примерах', 'Eve')
library.return_book('Идеальный программист', 'Eve')  # Fake
library.return_book('Идеальный программист', 'Chukc')  # Fake
library.return_book('Fake book', 'Chukc')  # Fake
print('')
