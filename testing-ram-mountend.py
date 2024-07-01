import os
import glob
import numpy as np
import time
from multiprocessing import Pool

def create_large_test_files(input_dir, num_files, num_lines):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)

    for i in range(num_files):
        with open(os.path.join(input_dir, f'mat{i}.in'), 'w') as f:
            for _ in range(num_lines):
                matrix = np.random.randint(1, 10, size=(5, 5)).flatten()
                f.write(' '.join(map(str, matrix)) + '\n')

def process_file_with_cache(input_file, output_file):
    cache = {}
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line not in cache:
                matrix = np.fromstring(line.strip(), sep=' ').reshape(5, 5)
                result = np.sum(matrix)
                cache[line] = result
            else:
                result = cache[line]
            outfile.write(f"{result}\n")

def process_file_no_cache(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            matrix = np.fromstring(line.strip(), sep=' ').reshape(5, 5)
            result = np.sum(matrix)
            outfile.write(f"{result}\n")

def process_file_wrapper(file_info, use_cache):
    input_file, output_file = file_info
    if use_cache:
        process_file_with_cache(input_file, output_file)
    else:
        process_file_no_cache(input_file, output_file)

def run_performance_test(input_dir, output_dir, use_cache):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    input_files = glob.glob(os.path.join(input_dir, '*.in'))
    file_info_list = [(f, os.path.join(output_dir, os.path.basename(f).replace('.in', '.out'))) for f in input_files]

    start_time = time.time()
    with Pool(processes=os.cpu_count()) as pool:
        pool.starmap(process_file_wrapper, [(file_info, use_cache) for file_info in file_info_list])
    elapsed_time = time.time() - start_time

    return elapsed_time

def main():
    ram_input_dir = 'E:\\input'  # Calea către RAM disk
    ram_output_dir = 'E:\\output'  # Calea către RAM disk pentru rezultate

    disk_input_dir = r'C:\Users\ASUS\OneDrive\Desktop\TEMA IA\input'
    disk_output_dir = r'C:\Users\ASUS\OneDrive\Desktop\TEMA IA\output'


    create_large_test_files(ram_input_dir, 100, 100000)

    # Rularea testului pe RAM disk cu caching activat
    print("Testare performanță pe RAM disk cu caching...")
    ram_time_with_cache = run_performance_test(ram_input_dir, ram_output_dir, use_cache=True)
    print(f"Timp de execuție pentru RAM disk cu caching: {ram_time_with_cache:.2f} secunde")

    # Rularea testului pe RAM disk fără caching
    print("Testare performanță pe RAM disk fără caching...")
    ram_time_without_cache = run_performance_test(ram_input_dir, ram_output_dir, use_cache=False)
    print(f"Timp de execuție pentru RAM disk fără caching: {ram_time_without_cache:.2f} secunde")

    # Crearea fișierelor de test pentru HDD/SSD
    create_large_test_files(disk_input_dir, 100, 100000)

    # Rularea testului pe HDD/SSD cu caching activat
    print("Testare performanță pe HDD/SSD cu caching...")
    disk_time_with_cache = run_performance_test(disk_input_dir, disk_output_dir, use_cache=True)
    print(f"Timp de execuție pentru HDD/SSD cu caching: {disk_time_with_cache:.2f} secunde")

    # Rularea pe HDD/SSD fără caching
    print("Testare performanță pe HDD/SSD fără caching...")
    disk_time_without_cache = run_performance_test(disk_input_dir, disk_output_dir, use_cache=False)
    print(f"Timp de execuție pentru HDD/SSD fără caching: {disk_time_without_cache:.2f} secunde")


    with open('task-mat-cache-parallel-ram-testing.txt', 'w') as f:
        f.write(f'RAM-based time with caching: {ram_time_with_cache:.2f} secunde\n')
        f.write(f'RAM-based time without caching: {ram_time_without_cache:.2f} secunde\n')
        f.write(f'Disk-based time with caching: {disk_time_with_cache:.2f} secunde\n')
        f.write(f'Disk-based time without caching: {disk_time_without_cache:.2f} secunde\n')

if __name__ == '__main__':
    main()
