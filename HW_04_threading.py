import threading
from collections import defaultdict
import time
import os


def file_search(file_paths, keywords, results, results_lock):
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                # Додаємо вивід назви файлу, що обробляється
                print(f"Обробка файлу: {file_path}")
                found_any = False
                for keyword in keywords:
                    if keyword.lower() in content:
                        found_any = True
                        with results_lock:
                            results[keyword].append(file_path)
                if not found_any:
                    print(f"Ключові слова не знайдені в файлі {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")


def thread_based_search(file_list, keywords):
    num_threads = 1  # Можна змінити в залежності від кількості ядер та завдань
    results = defaultdict(list)
    results_lock = threading.Lock()
    threads = []
    chunk_size = len(file_list) // num_threads

    start_time = time.time()
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (start_index + chunk_size if i <
                     num_threads - 1 else len(file_list))
        thread = threading.Thread(target=file_search, args=(
            file_list[start_index:end_index], keywords, results, results_lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    end_time = time.time()

    print(f"Thread-based search took {end_time - start_time} seconds")
    return results


def get_file_list(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_list.append(os.path.join(root, file))
    return file_list


if __name__ == '__main__':
    directory = r'C:\Users\Elena\Desktop\MasterIT\Tier2\Computer Systems\HW04'
    file_list = get_file_list(directory)
    keywords = ['дані', 'програми', 'пошук']
    results = thread_based_search(file_list, keywords)
    print(results)
