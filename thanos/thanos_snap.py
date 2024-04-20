# Constants used in the pseudorandom number generator
a = 1103515245
c = 12345

def random(seed):
    # Implements a linear congruential generator (LCG) for pseudorandom numbers
    seed = (a * seed + c) % 999999999
    return seed

def main():
    # Retrieve a list of process IDs from the system
    procs = list(map(lambda x: x['pid'], process.list()))
    snapped = []  # List to hold the IDs of processes to be terminated
    seed = 12345  # Initial seed for the random number generator

    # Iterate up to a very large number, though likely to break out early
    for i in range(0,999999999):
        # Print the current status of how many processes have been "snapped"
        print(str(len(snapped)) + ' / ' + str(len(procs) // 2))
        
        # Stop if half of the processes have been terminated
        if len(snapped) >= len(procs) // 2:
            break
        
        # Generate a new pseudorandom seed
        seed = random(seed)
        # Select a new process based on the pseudorandom number
        new_proc = procs[seed % len(procs)]

        # Check if the process can be added to the snapped list (not essential and not already added)
        if new_proc > 1 and new_proc not in snapped:
            print('Adding ' + str(new_proc))
            snapped.append(new_proc)
        else:
            print('Failed to add ' + str(new_proc))

    # For each process in the snapped list, terminate it
    for snap in snapped:
        print('KILL ' + str(snap))
        process.kill(snap)

# Entry point of the script
main()
