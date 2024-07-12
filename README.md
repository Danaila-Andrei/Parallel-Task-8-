Prerequisites:
• Learn as much as possible about multithreading.
• Learn as much as possible about multiprocessing.
• Learn as much as possible about Python's Global Interpreter Lock (GIL).
• Learn as much as possible about tmpfs


Description:
1. The typical input for Task "Python3 Basics (matrices, cont'd.)"
consists of large files with more than 100,000 lines, each line
containing at least a 5x5 matrix. Thousands of such files may be present
in the "input" directory (e.g., mat96.in, mat512.in, mat10020.in).
Develop a mechanism for processing these input files in parallel. Each
CPU core should run a thread/process to process an input file. These
threads/processes will generate the corresponding output files (e.g.,
mat96.out, mat512.out, mat10020.out).

Proof of successful task completion:

• Demonstrate the program's functionality by testing with large input
directories containing more than 100 input files, each with more than
100,000 lines and each line containing at least a 5x5 matrix.

• Compare the performance between the regular implementation of "Python3
Basics (matrices, cont'd.)" and the parallel one.

• Avoid the GIL.

• Test with a RAM-mounted "input" directory.(e.g. sudo mount -t tmpfs -o
size=1G tmpfs /mnt/input)

• Continue to use the previously developed caching mechanism.

Provide the following files for download from GitHub:
• "mat-cache-parallel.py" program.

• "task-mat-cache-parallel-testing.txt": a document comparing the
runtime of the parallel implementation with the standard, non-parallel
implementation.

• "task-mat-cache-parallel-ram-testing.txt": : a document comparing the
runtime between the case when the "input" directory is in-memory with
the case when the "input" directory is on-disk (e.g., SSD, spinning disk).
