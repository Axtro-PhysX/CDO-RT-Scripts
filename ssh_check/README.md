# Default Credential Checker

This script automates SSH connection attempts to a list of IP addresses using specified credentials. It supports different modes of operation, making it suitable for single or multiple team environments, and optionally integrates with a dashboard for reporting successful connections and a pwnboard for visualizing access.

## Features

- **Multiple Modes**: Run checks against single teams, multiple teams, or a single host across teams.
- **Demo Mode**: Simulate SSH checks without actual connection attempts, useful for testing integration with pwnboard/webapp.
- **Integration with Pwnboard**:  Post successful SSH attempts to pwnboard.
- **Integration with Dashboard**: Report successful credentials to a the Flask web application dashboard.

## Requirements

- Python 3.x
- External libraries: `argparse`, `subprocess`, `requests`, `pathlib`, `concurrent.futures`, `time`
- `sshpass` command-line tool for non-interactive ssh password authentication.

## Installation

Ensure you have Python 3.x installed on your system. You can install the required Python libraries using pip:

```bash
pip install requests
```


## Usage

1. Create your IP addresses and credentials files. IP addresses should be listed one per line in the IP file (see example_ips.txt), the "x" is the changing team number. Credentials should be in the format `username:password`, one per line, in the credentials file (see example_creds.txt).

2. Run the script with the required arguments:

```bash
python ssh_attempt_script.py -f <ip_file_path> -c <creds_file> --dashboard_url <dashboard_url> [options]
```

Example using demo mode:
```bash
python3 check_creds.py -m multiple -f example_ips.txt -c example_creds.txt --dashboard_url http://127.0.0.1:5000 --demo
```

3. Start the flask web server
   
```bash
flask run --host=0.0.0.0
```

### Command Line Arguments

- `-m`, `--mode`: Mode of operation (`single`, `multiple`, `host_across_teams`). Default is `multiple`.
- `-t`, `--team_number`: Team number for single team mode. Default is `5`.
- `-n`, `--num_teams`: Number of teams for multiple or host across teams mode. Default is `10`.
- `-p`, `--pwnboard_host`: URL for the pwnboard. Default is `https://127.0.0.1/pwn/boxaccess`.
- `-f`, `--ip_file_path`: Path to the file containing IP addresses. (Required)
- `-c`, `--creds_file`: Path to the file containing credentials. (Required)
- `--demo`: Enable demo mode.
- `--dashboard_url`: URL to the Flask web app for posting valid credentials. (Required)
- `--debug`: Enable debug messages.


## Demo Mode

Enable demo mode to simulate SSH connection attempts without actual connections. This is useful for testing pwnboard and the dashboard integration:

```bash
python ssh_attempt_script.py --demo ...
```


### Other notes:

Clear the dashboard:
```bash
curl -X POST http://127.0.0.1:5000/api/clear_creds
```