import os
import time
import hashlib
import numpy as np
import multiprocessing as mp
import json


def generate_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_cache(cache_file):

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}


def save_cache(cache, cache_file):
    """Salvează cache-ul într-un fișier JSON."""
    with open(cache_file, 'w') as f:
        json.dump(cache, f)


def process_file_serial(file_path, output_dir, cache, cache_file):
    file_hash = generate_file_hash(file_path)
    output_file_path = os.path.join(output_dir, os.path.basename(file_path).replace('.in', '.out'))

    if cache.get(file_path) == file_hash:
        print(f"{file_path} nu s-a schimbat. Sărind procesarea.")
        return

    with open(file_path, 'r') as fin, open(output_file_path, 'w') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if ':' not in line:
                print(f"Skipping line in {file_path}: {line}")
                continue

            rows_cols, matrix_str = line.split(':')
            try:
                rows, cols = map(int, rows_cols.split('x'))
                matrix = np.fromstring(matrix_str, dtype=int, sep=' ').reshape((rows, cols))

                processed_matrix = matrix * 2
                processed_matrix_str = ' '.join(map(str, processed_matrix.flatten()))
                fout.write(f'{rows}x{cols}:{processed_matrix_str}\n')
            except ValueError as ve:
                print(f"ValueError processing line in {file_path}: {line}")
                print(ve)
            except Exception as e:
                print(f"Error processing line in {file_path}: {line}")
                print(e)

    cache[file_path] = file_hash
    save_cache(cache, cache_file)


def process_files_serial(input_dir):
    output_dir = os.path.join(input_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)  # Creează directorul de ieșire dacă nu există

    cache_file = os.path.join(output_dir, 'cache.json')
    cache = load_cache(cache_file)

    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.in')]

    for file in files:
        process_file_serial(file, output_dir, cache, cache_file)


def process_file(file_path, output_dir, cache, cache_file):
    file_hash = generate_file_hash(file_path)
    output_file_path = os.path.join(output_dir, os.path.basename(file_path).replace('.in', '.out'))

    if cache.get(file_path) == file_hash:
        print(f"{file_path} nu s-a schimbat. Sărind procesarea.")
        return

    with open(file_path, 'r') as fin, open(output_file_path, 'w') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            if ':' not in line:
                print(f"Skipping line in {file_path}: {line}")
                continue

            rows_cols, matrix_str = line.split(':')
            try:
                rows, cols = map(int, rows_cols.split('x'))
                matrix = np.fromstring(matrix_str, dtype=int, sep=' ').reshape((rows, cols))

                processed_matrix = matrix * 2
                processed_matrix_str = ' '.join(map(str, processed_matrix.flatten()))
                fout.write(f'{rows}x{cols}:{processed_matrix_str}\n')
            except ValueError as ve:
                print(f"ValueError processing line in {file_path}: {line}")
                print(ve)
            except Exception as e:
                print(f"Error processing line in {file_path}: {line}")
                print(e)

    cache[file_path] = file_hash
    save_cache(cache, cache_file)


def process_files_parallel(input_dir):
    output_dir = os.path.join(input_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    cache_file = os.path.join(output_dir, 'cache.json')
    cache = load_cache(cache_file)

    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.in')]

    # Folosește Pool pentru a procesa fișierele în paralel
    with mp.Pool(mp.cpu_count()) as pool:

        pool.starmap(process_file, [(file, output_dir, cache, cache_file) for file in files])


def test_serial(input_dir):
    start_time = time.time()
    process_files_serial(input_dir)
    end_time = time.time()
    return end_time - start_time

def test_parallel(input_dir):
    start_time = time.time()
    process_files_parallel(input_dir)
    end_time = time.time()
    return end_time - start_time

if __name__ == '__main__':
    dir_on_disk = r'C:\Users\ASUS\OneDrive\Desktop\TEMA IA\Task-8\input'

    # Testează versiunea secvențială
    time_serial_disk = test_serial(dir_on_disk)
    print(f"Secvențial: {time_serial_disk:.2f} secunde")

    # Testează versiunea paralelă
    time_parallel_disk = test_parallel(dir_on_disk)
    print(f"Paralel: {time_parallel_disk:.2f} secunde")
