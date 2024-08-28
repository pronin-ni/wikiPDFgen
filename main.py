import os
import requests
import pdfkit
from urllib.parse import unquote, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Указываем путь к wkhtmltopdf.exe, если он не в PATH
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # Убедитесь, что путь правильный
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def get_random_wikipedia_page():
    # Получаем URL случайной страницы из Википедии
    response = requests.get("https://ru.wikipedia.org/wiki/Special:Random")
    return response.url

def generate_pdf_from_url(url, output_path):
    # Генерируем PDF из URL с улучшенными опциями
    options = {
        'enable-local-file-access': None,  # Включить доступ к локальным файлам
        'disable-smart-shrinking': None,  # Отключить умное сжатие
        'encoding': "UTF-8",  # Установка кодировки
        'load-error-handling': 'ignore',  # Игнорировать ошибки загрузки контента
        'no-outline': None,  # Удалить оглавление
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'zoom': '1.0',  # Увеличить масштаб по умолчанию
        'viewport-size': '1280x1024',  # Установить размер о��ласти просмотра
        'print-media-type': '',  # Использовать стили для печати
        'disable-javascript': '',  # Отключить JavaScript для стабильности
        'no-stop-slow-scripts': '',  # Отключить остановку медленных скриптов
    }
    pdfkit.from_url(url, output_path, configuration=config, options=options)

def create_output_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def get_page_title_from_url(url):
    # Извлекаем название страницы из URL
    parsed_url = urlparse(url)
    page_title = os.path.basename(parsed_url.path)
    page_title = unquote(page_title)  # Декодируем URL-encoded строку
    # Удаляем недопустимые символы для имени файла
    page_title = page_title.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
    return page_title

def process_page(output_dir):
    try:
        wikipedia_url = get_random_wikipedia_page()
        page_title = get_page_title_from_url(wikipedia_url)
        output_pdf_path = os.path.join(output_dir, f"{page_title}.pdf")
        generate_pdf_from_url(wikipedia_url, output_pdf_path)
        print(f"PDF файл успешно создан: {output_pdf_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    output_dir = "wikipedia_pdfs"
    num_documents = 5000  # Количество генерируемых документов
    max_workers = 10  # Количество потоков
    
    create_output_directory(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_page, output_dir) for _ in range(num_documents)]
        for future in as_completed(futures):
            future.result()  # Получить результат для обработки исключений
