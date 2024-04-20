# Process Terminator Script

## Overview
This Python script is designed to "snap" (terminate) approximately half of the running processes on a system at random. It is inspired by the concept of indiscriminately halving the number of entities, as depicted in the Marvel universe.

## Warning
**Use this script with extreme caution.** Terminating system processes can lead to data loss, system instability, or system crashes. It is recommended to thoroughly review and understand the code before running it on any system, particularly in a production environment.

## Requirements
- Python 3.x
- Custom `process` module with `list()` and `kill()` methods

## How It Works
1. **Initialization**: The script starts by defining constants for a pseudorandom number generator (PRNG).
2. **Random Number Generation**: It uses a linear congruential generator (LCG) to produce pseudorandom numbers.
3. **Process Selection**: The script iterates over a massive range, attempting to select and terminate half of the current processes. Processes are selected based on the PRNG output.
4. **Process Termination**: If a process meets certain criteria (not essential and not already terminated), it is added to a list of "snapped" processes and then terminated.

## Running the Script
To run the script, ensure Python and the required `process` module are installed, and execute it from the command line:
```bash
python thanos_snap.py
