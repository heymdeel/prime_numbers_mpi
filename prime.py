import sys

import math
import random
from mpi4py import MPI

def isPrime(x):
    if (x % 2 == 0):
        return False

    i = 3
    while (i < math.sqrt(x)):
        if (x % i == 0):
            return False
        i += 2
    return True

master = 0
comm = MPI.COMM_WORLD

try:
    n = int(sys.argv[1])
except (IndexError, ValueError) as e:
    print('Error!')
    print(__doc__)
    sys.exit(1)

# rank, cluster size and proc names
rank = comm.rank
world_size = comm.size
name = MPI.Get_processor_name()

all_primes, cur_primes = [], []
clock = MPI.Wtime()

if (rank == master):
    print("Searching for prime numbers")
start = rank * n // world_size
if (start == 0):
    start = 3
end = (rank + 1) * n // world_size
for i in range(start, end):
    if isPrime(i):
        cur_primes.append(i)

if (rank == master):
    print("Collecting results")

if (rank == master):
    all_primes.extend(cur_primes)

    for i in range(1, world_size):
        primes = comm.recv(source = i)
        all_primes.extend(primes)
else:
    comm.send(cur_primes, dest = master)

if (rank == master):
    clock = MPI.Wtime() - clock
    print("Found all primes in {0:.5} sec".format(clock))
    
    out = open('output.txt', 'w')
    out.write('{}\n'.format(len(all_primes)))
    for item in all_primes:
        out.write("{} ".format(item))