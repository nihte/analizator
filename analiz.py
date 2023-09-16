import re
import pymorphy3
import collections
from wordcloud import WordCloud
from PIL import Image
from typing import NoReturn

class TextAnalyser:
    def __init__(self, file_name=None, pos_list=['VERB', 'NOUN'], chislo=None, background="Black") -> None:
        """
        Инициализирует объект TextAnalyser.
        Параметры:
        - file_name (строка, по умолчанию None): Имя файла для анализа.
        - pos_list (список строк, по умолчанию ["VERB", "NOUN"]): Список желаемых частей речи.
        Возвращает: None.
        Выбрасывает исключение Exception, если не указан file_name.
        Вызывает методы read_file(), check_empty_file(), prepare_text(), filter_words_by_pos(), print_text() и create_wordcloud().
        """
        if file_name is None:
            raise Exception('Не указан файл для анализа!')
        self.file_name = file_name
        self.background_color = background
        self.pos_list = pos_list
        self.chislo = chislo
        self.read_file()
        self.check_empty_file()
        self.prepare_text()
        self.filter_words_by_pos()
        self.print_text()
        self.create_wordcloud()

    def read_file(self) -> None | NoReturn:
        """
        Читает содержимое указанного файла и сохраняет текст.
        Возвращает: None | NoReturn:.
        Может вызывать исключение FileNotFoundError, если файл не найден.
        """
        try:
            with open(self.file_name, 'r', encoding='UTF-8') as file:
                self.file = file
                self.text = self.file.read()
        except FileNotFoundError:
            raise Exception(f'Файл {self.file_name} не найден!')

    def check_empty_file(self) -> None | NoReturn:
        """
        Проверяет, является ли прочитанный текст пустым.
        Возвращает: None | NoReturn:.
        Может вызывать исключение RuntimeError, если текст пуст.
        """
        if not self.text:
            raise RuntimeError(f'Прочитанный файл: {self.file_name}, пуст!')

    def prepare_text(self) -> None:
        """
        Предварительно обрабатывает текст, приводя его к нижнему регистру и удаляя небуквенно-цифровые символы,
        кроме пробелов и дефисов. Разделяет текст на отдельные слова.
        Возвращает: None.
        """
        self.text = self.text.lower()
        clean_text = ''.join(re.findall(r'[\w\s-]', self.text))
        self.words = clean_text.split()

    def filter_words_by_pos(self) -> list:
        """
        Фильтрует слова по заданным частям речи с использованием библиотеки pymorphy3.
        Возвращает: list.
        """
        morph = pymorphy3.MorphAnalyzer()
        self.words_by_pos = []

        for word in self.words:
            parsed_word = morph.parse(word)[0]
            pos = parsed_word.tag.POS
            if pos in self.pos_list:
                self.words_by_pos.append(parsed_word.normal_form)

    def print_text(self) -> None:
        """
        Выводит исходные слова, общее количество слов и отфильтрованные слова.
        Возвращает: None.
        """
        print(f'Обычные слова: {self.words}')
        print(f'В этом тексте {len(self.words)} слов')
        print(f'Отфильтрованные слова: {self.words_by_pos}')
        print(f'В этом тексте {len(self.words_by_pos)} отфильтрованных слов')

    def create_wordcloud(self) -> None:
        """
        Создает облако слов на основе отфильтрованных слов и сохраняет его в файл.
        Возвращает: None.
        """
        word_counts = collections.Counter(self.words_by_pos)
        top_10_words = word_counts.most_common(self.chislo)

        self.wordcloud = WordCloud(width=800, height=400, background_color=self.background_color).generate_from_frequencies(dict(top_10_words))
        image = self.wordcloud.to_image()
        image.save('wordcloud.png')
        print("Облако слов сохранено в файл 'wordcloud.png'")