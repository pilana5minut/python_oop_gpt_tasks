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
        return f'Название книги: {self.title}\nАвтор книги: {self.author}\nID книги: {self.id}\nСтатус книги: {'В наличии' if self.status else 'У читателя'}'

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
        return f'Имя читателя: {self.name}\nID читателя: {self.id}'


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
            raise LookupError(f'ОТМЕНА: ID читателя по имени "{
                              name}" не найден в индексе: index_readers_by_name')
        else:
            return library.readers[reader_id]

    def add_book(self, book: Book) -> str:
        """Добавляет книгу в библиотеку.
        Args:
            book (Book): Экземпляр класса Book.
        Returns:
            str: Строку отражающую статус процедуры регистрации книги.
        """

        if isinstance(book, Book):

            if book.id in self.lib:
                print(f'ОТМЕНА: Книга с ID "{
                      book.id}" УЖЕ зарегистрирована в библиотеке.')
                return

            self.lib[book.id] = book
            self.index_books_by_title[book.title] = book.id
            self.add_book_in_index_by_author(book)
            print(f'УСПЕХ: Книга "{
                  book.title}" БЫЛА УСПЕШНО зарегистрирована в библиотеке.')
        else:
            print(f'ОШИБКА: "{book}" НЕ ЯВЛЯЕТСЯ объектом книги.')

    def register_reader(self, reader: Reader) -> str:
        """Регистрирует нового читателя.
        Args:
            reader (Reader): Экземпляр класса Reader.
        Returns:
            str: Строку отражающую статус процедуры регистрации читателя.
        """

        if isinstance(reader, Reader):

            if reader.id in self.readers:
                print(f'Читатель с ID "{
                      reader.id}" УЖЕ зарегистрирован в библиотеке.')
                return

            self.readers[reader.id] = reader
            self.index_readers_by_name[reader.name] = reader.id
            print(f'УСПЕХ: Читатель по имени "{
                  reader.name}" БЫЛ УСПЕШНО зарегистрирован в библиотеке.')
        else:
            print(f'ОШИБКА: "{reader}" НЕ ЯВЛЯЕТСЯ объектом читателя.')

    def borrow_book(self, title: str, reader: str) -> str:
        """Выдает книгу читателю, если она в наличии.
        Args:
            title (str): Строка с названием книги.
            reader (str): Строка с именем читателя.
        Returns:
            str: Строку отражающую статус процедуры выдачи книги читателю.
        """

        try:
            current_book = self.find_book_by_title(title)
            current_reader = self.find_reader_by_name(reader)

            if current_book.status and len(current_reader.borrowed_books) < self.rental_limit:
                current_book.status = False
                current_book.borrower = current_reader
                current_reader.borrowed_books.append(current_book)
                self.borrow_history.add(current_reader.name)
                print(f'УСПЕХ: Книга "{current_book.title}" БЫЛА ВЫДАНА читателю "{
                    current_reader.name}"')
            elif len(current_reader.borrowed_books) >= self.rental_limit:
                print(f'ОТМЕНА: Для читателя "{
                    current_reader.name}" БЫЛ ДОСТИГНУТ ЛИМИТ.')
            else:
                print(f'ОТМЕНА: Книга "{current_book.title}" в данный момент У ДРУГОГО ЧИТАТЕЛЯ "{
                    current_book.borrower.name}"')
        except LookupError as e:
            print(f'{e}')

    def return_book(self, title, reader) -> str:
        """Возвращает книгу от читателя в библиотеку если она числится в списке читателя.
        Args:
            title (str): Строка с названием книги.
            reader (str): Строка с именем читателя.
        Returns:
            str: Строку отражающую статус процедуры возврата книги читателем.
        """

        try:
            current_book = self.find_book_by_title(title)
            current_reader = self.find_reader_by_name(reader)

            if current_book.borrower is not None and current_book.borrower.name == current_reader.name:
                current_book.status = True
                current_book.borrower = None
                current_reader.borrowed_books.remove(current_book)
                print(f'УСПЕХ: Книга "{current_book.title}" БЫЛА ВОЗВРАЩЕНА читателем "{
                    current_reader.name}"')
            else:
                print(f'ОТМЕНА: Книга "{current_book.title}" НЕ ЧИСЛИТСЯ в списке читателя "{
                    current_reader.name}"')
        except LookupError as e:
            print(f'{e}')

    def get_book_status(self, title: str) -> str:
        """Выводит информацию о статусе книги, и о читателе у которого она находится, если не в библиотеке.
        Args:
            title (str): Строка с названием книги.
        Returns:
            str: Строку о статусе книги и у какого читателя она находится.
        """

        current_book = self.find_book_by_title(title)
        result_string = f'{current_book}'

        if current_book.borrower is not None:
            result_string += f'\n{current_book.borrower}'

        print(result_string)

    def list_reader_books(self, reader) -> None:
        """Выводит список книг, находящихся у читателя.
        Args:
            reader (str): Строка с именем читателя.
        """

        current_reader = self.find_reader_by_name(reader)
        count = 1

        print(f'Список книг читателя "{current_reader.name}" {
            len(current_reader.borrowed_books)} шт.')

        for b in current_reader.borrowed_books:
            print('')
            print(f'{count}.')
            count += 1
            print(b)

    def search_book(self, prompt: str) -> None:
        """Метод поиска книг, который позволит искать книги по названию, автору или по тому, у какого читателя она находится.
        Args:
            prompt (str): Строка с название книги или именем автора или именем читателя.
        """

        found = False

        # Поиск книги по названию.
        try:
            title_book = self.find_book_by_title(prompt)
            found = True
            print('--------------------------------')
            print(f'По запросу "{prompt}" найдено 1 книга.')
            print('')
            print(title_book)
            if title_book.borrower is not None:
                print(title_book.borrower)
        except LookupError:
            pass

        # Поиск книги по автору
        try:
            author_book = self.find_books_by_author(prompt)
            found = True
            print('--------------------------------')
            if isinstance(author_book, list):
                print(f'По запросу "{prompt}" найдено несколько ({
                    len(author_book)}) книг.')
                print('')

                count = 1
                for b in author_book:
                    print('')
                    print(f'{count}.')
                    count += 1
                    print(b)
            else:
                print(f'По запросу "{prompt}" найдена 1 книга.')
                print('')
                print(author_book)
        except LookupError:
            pass

        # Поиск читателя по имени.
        try:
            reader_name = self.find_reader_by_name(prompt)
            found = True
            print('--------------------------------')
            print(f'По запросу "{
                prompt}" найден читатель:\n{reader_name}')
            if len(reader_name.borrowed_books) > 0:
                print(f'За читателем по имени "{
                    reader_name.name}" числится {len(reader_name.borrowed_books)} книг.')
                answer = input(f'Показать список книг читателя {
                    reader_name.name} (Y/n): ').lower()
                if answer == 'y' or answer == '':
                    self.list_reader_books(reader_name.name)
                    print('')
                else:
                    return
            else:
                print(f'За читателем по имени "{
                    reader_name.name}" числится 0 книг.')
        except LookupError:
            pass

        #  Ни чего не найдено.
        if not found:
            print(f'По запросу "{prompt}" ни чего не найдено.')


# tests ###############################################################


print('-------- Создаем Библиотеку: class Library(limit: int)')
library = Library(4)
print('')

print('-------- Создаем Книги: class Book(title: str, author: str, id: int)')
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
b16 = Book("Alice in Wonderland", "Льюис Кэрролл", 16)
b17 = Book("Yeah! Yeah! Yeah!", "Bob Stanley", 17)
b18 = Book("Yeah! Yeah! Yeah!", "Bob Stanley", 17)  # Duplicate
print('')

print('-------- Регистрируем Книги в библиотеке: (method) def add_book(book: Book) -> str')
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
library.add_book(b18)  # Duplicate
library.add_book('Fake_book')
print('')

print('-------- Показываем основной словарь Книг')
for k, v in library.lib.items():
    print(f'{k}: (obj_book) {v.title} - {v.author}')
print('')

print('-------- Показываем индекс Книг по автору')
for k, v in library.index_books_by_author.items():
    print(f'{k}: {v}')
print('')

#######################################################################


print('-------- Создаем Читателей: class Reader(name: str, id: int)')
r1 = Reader('Alice', 123)
r2 = Reader('Bob', 456)
r3 = Reader('Eve', 789)
r4 = Reader('Eve', 789)  # Duplicate
r5 = Reader('Trent', 246)
print('')

print('-------- Регистрируем Читателей в библиотеке: (method) def register_reader(reader: Reader) -> str')
library.register_reader(r1)
library.register_reader(r2)
library.register_reader(r3)
library.register_reader(r4)  # Duplicate
library.register_reader(r5)
library.register_reader('Chuck')
print('')

print('-------- Показываем основной словарь Читателей')
for k, v in library.readers.items():
    print(f'{k}: (obj_reader) {v.name}')
print('')

print('-------- Показываем индекс Читателей по имени')
for k, v in library.index_readers_by_name.items():
    print(f'{k}: {v}')
print('')

#######################################################################


print('-------- Выдаем Книги Читателям: (method) def borrow_book(title: str, reader: str) -> str')
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

print('-------- Читатели возвращают книги: (method) def return_book(title: Any, reader: Any) -> str')
library.return_book('Python Карманный справочник', 'Bob')
library.return_book('Чистый код', 'Alice')
library.return_book('Django 4 в примерах', 'Eve')
library.return_book('Идеальный программист', 'Eve')  # Fake
library.return_book('Идеальный программист', 'Chukc')  # Fake
library.return_book('Fake book', 'Chukc')  # Fake
print('')

print('-------- Проверяем статус книг: (method) def get_book_status(title: str) -> str')
library.get_book_status("Чистый код")
print('')
library.get_book_status("Идеальная работа")
