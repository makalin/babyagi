import requests
import datetime
import wikipedia
import json
import random
import re
import subprocess
import time
import base64
import uuid
import csv
from io import StringIO
import hashlib
import sqlite3

try:
    import markdown
except ImportError:
    markdown = None

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Existing tools

def web_search(query):
    url = f'https://duckduckgo.com/html/?q={query}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return f"Web search for '{query}' completed. (HTML content omitted)"
    return f"Web search failed for '{query}'"

def file_read(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        return f"File read error: {e}"

def write_file(filepath_and_text):
    try:
        filepath, text = filepath_and_text.split('::', 1)
        with open(filepath.strip(), 'w') as f:
            f.write(text)
        return f"Wrote to {filepath.strip()}"
    except Exception as e:
        return f"File write error: {e}"

def summarize_text(text, llm=None):
    if llm is None:
        return "LLM not provided for summarization."
    prompt = f"Summarize the following text:\n{text}"
    return llm.generate(prompt)

def math_calculator(expr):
    try:
        return str(eval(expr, {"__builtins__": {}}))
    except Exception as e:
        return f"Math error: {e}"

def current_datetime(_):
    return datetime.datetime.now().isoformat()

def send_email(args):
    try:
        to, subject, body = args.split('::', 2)
        return f"Email sent to {to} with subject '{subject}'. Body: {body}"
    except Exception as e:
        return f"Email error: {e}"

def wikipedia_search(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception as e:
        return f"Wikipedia error: {e}"

def translate_text(args):
    # args: "text::target_language" (stub)
    try:
        text, lang = args.split('::', 1)
        return f"[Stub] '{text.strip()}' translated to {lang.strip()}"
    except Exception as e:
        return f"Translate error: {e}"

def extract_entities(text):
    # Simple regex for capitalized words as entities
    entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    return f"Entities: {entities}"

def image_generation(prompt):
    # Stub: just return a placeholder path
    return f"[Stub] Image generated for prompt: '{prompt}'. Saved to /tmp/generated_image.png"

def url_fetch(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text[:1000] + ('... [truncated]' if len(resp.text) > 1000 else '')
        return f"URL fetch failed: {resp.status_code}"
    except Exception as e:
        return f"URL fetch error: {e}"

def json_validator(text):
    try:
        obj = json.loads(text)
        return json.dumps(obj, indent=2)
    except Exception as e:
        return f"JSON error: {e}"

def random_number(args):
    try:
        start, end = map(int, args.split('::'))
        return str(random.randint(start, end))
    except Exception as e:
        return f"Random number error: {e}"

def weather_info(location):
    # Stub: return fake weather
    return f"[Stub] Weather for {location}: Sunny, 25°C"

def shell_command(cmd):
    # WARNING: This is dangerous! Only for trusted environments.
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
        return result[:1000] + ('... [truncated]' if len(result) > 1000 else '')
    except Exception as e:
        return f"Shell error: {e}"

def csv_reader(csv_text):
    try:
        f = StringIO(csv_text)
        reader = csv.reader(f)
        rows = list(reader)
        summary = f"CSV with {len(rows)} rows and {len(rows[0]) if rows else 0} columns. First row: {rows[0] if rows else 'N/A'}"
        return summary
    except Exception as e:
        return f"CSV error: {e}"

def timer_sleep(seconds):
    try:
        s = float(seconds)
        time.sleep(min(s, 5))  # Limit to 5 seconds for safety
        return f"Slept for {min(s, 5)} seconds."
    except Exception as e:
        return f"Sleep error: {e}"

def markdown_to_html(md_text):
    if markdown is None:
        return "Markdown package not installed."
    try:
        return markdown.markdown(md_text)
    except Exception as e:
        return f"Markdown error: {e}"

def unit_converter(args):
    # args: "value::from_unit::to_unit" (very simple, only a few units)
    conversions = {
        ('meters', 'feet'): lambda v: v * 3.28084,
        ('feet', 'meters'): lambda v: v / 3.28084,
        ('celsius', 'fahrenheit'): lambda v: v * 9/5 + 32,
        ('fahrenheit', 'celsius'): lambda v: (v - 32) * 5/9,
    }
    try:
        value, from_unit, to_unit = args.split('::')
        value = float(value)
        key = (from_unit.strip().lower(), to_unit.strip().lower())
        if key in conversions:
            return str(conversions[key](value))
        return f"Conversion not supported: {from_unit} to {to_unit}"
    except Exception as e:
        return f"Unit conversion error: {e}"

def base64_encode(text):
    try:
        return base64.b64encode(text.encode()).decode()
    except Exception as e:
        return f"Base64 encode error: {e}"

def base64_decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception as e:
        return f"Base64 decode error: {e}"

def uuid_generator(_):
    return str(uuid.uuid4())

def palindrome_checker(text):
    s = re.sub(r'[^A-Za-z0-9]', '', text.lower())
    return str(s == s[::-1])

def password_generator(length):
    try:
        length = int(length)
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
        return ''.join(random.choice(chars) for _ in range(min(length, 100)))
    except Exception as e:
        return f"Password error: {e}"

def zip_file_creator(args):
    # args: "zipname.zip::file1.txt,file2.txt" (stub)
    try:
        zipname, files = args.split('::', 1)
        file_list = [f.strip() for f in files.split(',')]
        return f"[Stub] Created zip {zipname} with files: {file_list}"
    except Exception as e:
        return f"Zip error: {e}"

def pdf_text_extractor(filepath):
    # Stub: just return a message
    return f"[Stub] Extracted text from PDF: {filepath}"

def image_to_text(filepath):
    # Stub: just return a message
    return f"[Stub] OCR text from image: {filepath}"

def html_title_extractor(html):
    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else 'No title found.'

def currency_converter(args):
    # args: "amount::from_currency::to_currency" (stub)
    try:
        amount, from_cur, to_cur = args.split('::')
        return f"[Stub] {amount} {from_cur} = {float(amount) * 1.1:.2f} {to_cur} (fake rate)"
    except Exception as e:
        return f"Currency conversion error: {e}"

def ip_geolocation(ip):
    # Stub: return fake location
    return f"[Stub] IP {ip} is located in Example City, Country."

def url_shortener(url):
    # Stub: return a fake short URL
    return f"[Stub] Shortened URL: https://short.url/{abs(hash(url)) % 100000}"

def http_status_checker(url):
    try:
        resp = requests.get(url)
        return f"HTTP status for {url}: {resp.status_code}"
    except Exception as e:
        return f"HTTP status error: {e}"

def prime_number_checker(n):
    try:
        n = int(n)
        if n < 2:
            return 'False'
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return 'False'
        return 'True'
    except Exception as e:
        return f"Prime check error: {e}"

def fibonacci_calculator(n):
    try:
        n = int(n)
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return str(a)
    except Exception as e:
        return f"Fibonacci error: {e}"

def anagram_finder(word):
    # Very simple: return reversed word as a fake anagram
    return f"Anagram: {word[::-1]}"

def sha256_hasher(text):
    return hashlib.sha256(text.encode()).hexdigest()

def rot13_encoder(text):
    return text.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'))

def palindrome_generator(text):
    s = re.sub(r'[^A-Za-z0-9]', '', text.lower())
    return text + s[::-1]

def caesar_cipher(args):
    # args: "text::shift" (encode only)
    try:
        text, shift = args.split('::')
        shift = int(shift) % 26
        def shift_char(c):
            if 'a' <= c <= 'z':
                return chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
            if 'A' <= c <= 'Z':
                return chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
            return c
        return ''.join(shift_char(c) for c in text)
    except Exception as e:
        return f"Caesar cipher error: {e}"

def morse_code_encoder(text):
    MORSE = {'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....', 'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.', 'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-', 'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ' ':'/'}
    try:
        return ' '.join(MORSE.get(c.upper(), '?') for c in text)
    except Exception as e:
        return f"Morse code error: {e}"

def plot_data(args):
    # args: "x1,x2,x3::y1,y2,y3::title"; saves to plot.png
    if plt is None:
        return "matplotlib not installed."
    try:
        x_str, y_str, title = args.split('::')
        x = [float(i) for i in x_str.split(',')]
        y = [float(i) for i in y_str.split(',')]
        plt.figure()
        plt.plot(x, y, marker='o')
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig('plot.png')
        plt.close()
        return "Plot saved to plot.png"
    except Exception as e:
        return f"Plot error: {e}"

def web_scrape(url):
    if BeautifulSoup is None:
        return "BeautifulSoup not installed."
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return f"Web scrape failed: {resp.status_code}"
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:1000] + ('... [truncated]' if len(text) > 1000 else '')
    except Exception as e:
        return f"Web scrape error: {e}"

def database_query(args):
    # args: "dbfile.sqlite::SELECT ..."
    try:
        dbfile, query = args.split('::', 1)
        conn = sqlite3.connect(dbfile.strip())
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return json.dumps(rows)
    except Exception as e:
        return f"Database error: {e}"

def ai_image_generate(prompt):
    # Stub: just return a placeholder path
    return f"[Stub] AI image generated for prompt: '{prompt}'. Saved to /tmp/ai_image.png"

tool_registry = {
    'web_search': web_search,
    'file_read': file_read,
    'write_file': write_file,
    'summarize_text': summarize_text,
    'math_calculator': math_calculator,
    'current_datetime': current_datetime,
    'send_email': send_email,
    'wikipedia_search': wikipedia_search,
    'translate_text': translate_text,
    'extract_entities': extract_entities,
    'image_generation': image_generation,
    'url_fetch': url_fetch,
    'json_validator': json_validator,
    'random_number': random_number,
    'weather_info': weather_info,
    'shell_command': shell_command,
    'csv_reader': csv_reader,
    'timer_sleep': timer_sleep,
    'markdown_to_html': markdown_to_html,
    'unit_converter': unit_converter,
    'base64_encode': base64_encode,
    'base64_decode': base64_decode,
    'uuid_generator': uuid_generator,
    'palindrome_checker': palindrome_checker,
    'password_generator': password_generator,
    'zip_file_creator': zip_file_creator,
    'pdf_text_extractor': pdf_text_extractor,
    'image_to_text': image_to_text,
    'html_title_extractor': html_title_extractor,
    'currency_converter': currency_converter,
    'ip_geolocation': ip_geolocation,
    'url_shortener': url_shortener,
    'http_status_checker': http_status_checker,
    'prime_number_checker': prime_number_checker,
    'fibonacci_calculator': fibonacci_calculator,
    'anagram_finder': anagram_finder,
    'sha256_hasher': sha256_hasher,
    'rot13_encoder': rot13_encoder,
    'palindrome_generator': palindrome_generator,
    'caesar_cipher': caesar_cipher,
    'morse_code_encoder': morse_code_encoder,
    'plot_data': plot_data,
    'web_scrape': web_scrape,
    'database_query': database_query,
    'ai_image_generate': ai_image_generate,
}

def call_tool(tool_name, *args, **kwargs):
    if tool_name in tool_registry:
        return tool_registry[tool_name](*args, **kwargs)
    return f"Tool '{tool_name}' not found." 