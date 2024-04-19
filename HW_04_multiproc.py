import os
import multiprocessing
from collections import defaultdict
import time


def process_search(file_paths, keywords, queue):
    local_results = defaultdict(list)
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().lower()
                for keyword in keywords:
                    if keyword.lower() in content:
                        local_results[keyword].append(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    queue.put(local_results)


def multiprocessing_based_search(file_list, keywords):
    num_processes = multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    processes = []
    chunk_size = len(file_list) // num_processes

    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (start_index + chunk_size if i <
                     num_processes - 1 else len(file_list))
        process = multiprocessing.Process(target=process_search, args=(
            file_list[start_index:end_index], keywords, queue))
        processes.append(process)
        process.start()

    results = defaultdict(list)
    for process in processes:
        process.join()
    while not queue.empty():
        local_results = queue.get()
        for key, paths in local_results.items():
            results[key].extend(paths)

    return results


def get_file_list(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]


if __name__ == '__main__':
    directory = r'C:\Users\Elena\Desktop\MasterIT\Tier2\Computer Systems\HW04'
    # Автоматично збирає список текстових файлів
    file_list = get_file_list(directory)
    keywords = ['вступ', 'програми', 'пошук']
    start_time = time.time()
    results = multiprocessing_based_search(file_list, keywords)
    end_time = time.time()
    print(f"Multiprocessing-based search took {end_time - start_time} seconds")
    print(results)
