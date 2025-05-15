from lxml import etree
import random

# Пути к файлам
XML_FILE = 'albums.xml'
DTD_FILE = 'schema.dtd'
XSD_FILE = 'schema.xsd'
TXT_XSL_FILE = 'transform_to_txt.xsl'
HTML_XSL_FILE = 'transform_to_html.xsl'
OUTPUT_TXT_FILE = 'albums_output.txt'
OUTPUT_HTML_FILE = 'albums_output.html'


def validate_xml_with_dtd(xml_path, dtd_path):
    """Валидация XML документа с использованием DTD."""
    try:
        dtd = etree.DTD(open(dtd_path, 'rb'))  # 'rb' для чтения в байтах
        xml_doc = etree.parse(xml_path)
        if dtd.validate(xml_doc):
            print(f"XML документ '{xml_path}' валиден по DTD '{dtd_path}'.")
            return True
        else:
            print(f"XML документ '{xml_path}' не валиден по DTD '{dtd_path}'.")
            print("Ошибки DTD валидации:")
            for error in dtd.error_log.filter_from_errors():
                print(
                    f"  - {error.message} (строка {error.line}, колонка {error.column})")
            return False
    except Exception as e:
        print(f"Ошибка при DTD валидации: {e}")
        return False


def validate_xml_with_xsd(xml_path, xsd_path):
    """Валидация XML документа с использованием XSD."""
    try:
        xsd_doc = etree.parse(xsd_path)
        xsd = etree.XMLSchema(xsd_doc)
        xml_doc = etree.parse(xml_path)
        if xsd.validate(xml_doc):
            print(f"XML документ '{xml_path}' валиден по XSD '{xsd_path}'.")
            return True
        else:
            print(f"XML документ '{xml_path}' не валиден по XSD '{xsd_path}'.")
            print("Ошибки XSD валидации:")
            for error in xsd.error_log:
                print(
                    f"  - {error.message} (строка {error.line}, колонка {error.column})")
            return False
    except Exception as e:
        print(f"Ошибка при XSD валидации: {e}")
        return False


def execute_xpath_query(xml_doc, query, query_description):
    """Выполнение XPath запроса и вывод результатов."""
    print(f"\n--- {query_description} ---")
    print(f"XPath: {query}")
    try:
        results = xml_doc.xpath(query)
        if isinstance(results, list):
            if not results:
                print("Результатов нет.")
            for item in results:
                if isinstance(item, etree._Element):
                    print(etree.tostring(item, pretty_print=True,
                          encoding='unicode').strip())
                elif isinstance(item, etree._ElementUnicodeResult):  # для text()
                    print(item)
                else:  # для sum(), count() и др.
                    print(item)
        else:  # Если результат не список (например, для sum(), count())
            print(f"Результат: {results}")
    except etree.XPathEvalError as e:
        print(f"Ошибка XPath: {e}")


def generate_random_playlist(xml_doc, num_tracks=5):
    """Генерация случайного плейлиста."""
    print(f"\n--- Случайный плейлист из {num_tracks} композиций ---")
    all_compositions = []
    # Собираем информацию о композициях: название, альбом, исполнитель
    for album_el in xml_doc.xpath('//album'):
        album_title = album_el.findtext('title')
        artist_names = [
            artist.text for artist in album_el.xpath('artists/artist')]
        for comp_el in album_el.xpath('compositions/composition'):
            comp_name = comp_el.findtext('name')
            duration = comp_el.findtext('duration')
            all_compositions.append({
                "name": comp_name,
                "duration": duration,
                "album": album_title,
                "artists": ", ".join(artist_names)
            })

    if not all_compositions:
        print("Композиции не найдены.")
        return

    if len(all_compositions) < num_tracks:
        print(
            f"В библиотеке меньше {num_tracks} композиций. Будут выбраны все доступные.")
        selected_tracks = all_compositions
    else:
        selected_tracks = random.sample(all_compositions, num_tracks)

    for i, track in enumerate(selected_tracks, 1):
        print(
            f"{i}. {track['name']} ({track['duration']}) - {track['artists']} (Альбом: {track['album']})")


def apply_xslt_transform(xml_path, xsl_path, output_path, transform_description):
    """Применение XSLT преобразования."""
    print(f"\n--- {transform_description} ---")
    try:
        xml_doc = etree.parse(xml_path)
        xsl_doc = etree.parse(xsl_path)
        transformer = etree.XSLT(xsl_doc)
        result_tree = transformer(xml_doc)

        # Для HTML вывода используем tostring, для TXT тоже можно, но указать encoding
        # method='text' в XSLT уже позаботился о формате.
        # XSLT определяет method (html, text, xml), так что просто пишем результат.
        with open(output_path, 'wb') as f:  # 'wb' для записи байтов
            f.write(result_tree)
        print(
            f"Преобразование завершено. Результат сохранен в '{output_path}'.")
    except Exception as e:
        print(f"Ошибка при XSLT преобразовании: {e}")


if __name__ == "__main__":
    print("=== Валидация XML ===")
    # Примечание: lxml может иметь проблемы с валидацией DTD, если DOCTYPE указан внутри XML,
    # но XSD обрабатывается хорошо. Для DTD лучше всего, если XML не содержит DOCTYPE,
    # а DTD передается в функцию валидации явно.
    # Если DOCTYPE в XML, etree.parse может автоматически попытаться его загрузить.
    # Чтобы избежать этого при XSD валидации, можно распарсить без DTD:
    # parser = etree.XMLParser(dtd_validation=False, load_dtd=False)
    # xml_doc_for_xsd = etree.parse(XML_FILE, parser)
    # А для DTD валидации использовать xml_doc = etree.parse(XML_FILE) (с DOCTYPE в файле)

    # Валидация DTD (убедитесь, что DOCTYPE есть в albums.xml)
    validate_xml_with_dtd(XML_FILE, DTD_FILE)

    # Валидация XSD (убедитесь, что xsi:noNamespaceSchemaLocation есть в albums.xml)
    validate_xml_with_xsd(XML_FILE, XSD_FILE)

    # Загрузка XML для XPath
    try:
        xml_doc = etree.parse(XML_FILE)
        print("\n=== XPath Запросы ===")

        # a) Альбомы указанного жанра
        genre_to_find = "Progressive Rock"
        query_a = f"//album[genres/genre='{genre_to_find}']"
        execute_xpath_query(
            xml_doc, query_a, f"Альбомы жанра '{genre_to_find}'")

        # b) Жанры указанного исполнителя
        artist_to_find = "Queen"
        query_b = f"//album[artists/artist='{artist_to_find}']/genres/genre/text()"
        # Для уникальности можно обработать в Python:
        # results_b = xml_doc.xpath(query_b)
        # unique_genres = set(results_b)
        # print(f"Уникальные жанры для {artist_to_find}: {unique_genres}")
        execute_xpath_query(
            xml_doc, query_b, f"Жанры исполнителя '{artist_to_find}'")

        # c) Альбомы с композициями длиннее 5 минут
        query_c = "//album[compositions/composition[number(substring-before(duration, ':')) * 60 + number(substring-after(duration, ':')) > 300]]"
        execute_xpath_query(
            xml_doc, query_c, "Альбомы с композициями > 5 минут")

        # d) Случайный плейлист (реализация в Python)
        # Выбираем 3 случайных трека
        generate_random_playlist(xml_doc, num_tracks=3)

        # e) Собственный запрос
        # "Альбомы, где количество композиций равно 3 И название альбома содержит 'The'"
        query_e = "//album[count(compositions/composition) = 3 and contains(title, 'The')]"
        execute_xpath_query(
            xml_doc, query_e, "Собственный запрос: альбомы с 3 композициями и 'The' в названии")

        # Другой вариант для (e)
        # query_e2 = "sum(//album[artists/artist='Pink Floyd']/count(compositions/composition))"
        # execute_xpath_query(xml_doc, query_e2, "Собственный запрос: общее количество композиций Pink Floyd")
        # query_e2 = "count(//album[artists/artist='Pink Floyd']/compositions/composition)"
        # execute_xpath_query(
        #     xml_doc, query_e2, "Собственный запрос: общее количество композиций Pink Floyd (используя count)")

    except etree.XMLSyntaxError as e:
        print(f"Ошибка парсинга XML: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print("\n=== XSLT Преобразования ===")
    # XSLT в TXT
    apply_xslt_transform(XML_FILE, TXT_XSL_FILE,
                         OUTPUT_TXT_FILE, "Преобразование XML в TXT")
    # XSLT в HTML
    apply_xslt_transform(XML_FILE, HTML_XSL_FILE,
                         OUTPUT_HTML_FILE, "Преобразование XML в HTML")
