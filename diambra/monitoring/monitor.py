import subprocess
import threading
import re
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
import os
from colorama import Fore, Style
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Monitor Docker containers based on log outputs.")
    parser.add_argument('-m', '--min_stage', type=int, default=0,
                        help='Minimum stage level to start monitoring (default: 0/off)')
    return parser.parse_args()

def setup_logging():
    """Sets up logging with both file and console handlers."""
    logger = logging.getLogger('DockerLogMonitor')
    logger.propagate = False
    output_log_path = './output/logs'
    os.makedirs(os.path.dirname(output_log_path), exist_ok=True)

    logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter('%(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(output_log_path + '/monitor.log', maxBytes=5*1024*1024, backupCount=2)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

class ColorFormatter(logging.Formatter):
    """Custom formatter to add color to console output based on log level."""
    def format(self, record):
        if 'reached stage' in record.msg:
            color = Fore.WHITE
        elif 'Game completed' in record.msg:
            color = Fore.YELLOW
        else:
            levelno = record.levelno
            color = Fore.GREEN if levelno == 20 else Fore.RED if levelno >= 40 else Fore.CYAN
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super(ColorFormatter, self).format(record)
    
def create_docker_monitor(min_stage=0, delay_start=5, initial_scan=True):
    return DockerMonitor(min_stage=min_stage, delay_start=delay_start, initial_scan=initial_scan)

class DockerMonitor:
    """A class to monitor Docker containers for specific log outputs."""
    def __init__(self, min_stage=0, delay_start=0, initial_scan=False):
        self.logger = setup_logging()
        self.minimum_stage = min_stage
        self.delay_start = delay_start
        self.initial_scan = initial_scan
        self.containers = self.get_active_containers()
        self.container_stages = {}
        self.game_completion = {container: [] for container in self.containers}
        self.lock = threading.Lock()
        self.threads = []
        self.monitoring = True

    def get_active_containers(self):
        """Fetches a list of currently active Docker containers."""
        command = ["docker", "ps", "--format", "{{.Names}}"]
        try:
            result = subprocess.check_output(command).decode().strip().split('\n')
            self.logger.debug("Active containers: " + ", ".join(result))
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error("Failed to get Docker containers: " + str(e))
            return []

    def scan_for_completed_games(self):
        """Scans for already completed games upon initial startup."""
        for container in self.containers:
            self.logger.debug(f"Scanning past logs for completed games in container: {container}")
            cmd = ["docker", "logs", container]
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            completions = process.stdout.count("Game completed!")
            self.game_completion[container] += [f"Past completion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"] * completions
            self.logger.debug(f"Found {completions} past completions for {container}")
        total_completions = sum(len(completions) for completions in self.game_completion.values())
        self.logger.info(f"Total past completions: {total_completions}")

    def follow_logs(self, container_name):
        """Follows the logs of a specific container and processes relevant output."""
        start_time = datetime.now().isoformat()
        cmd = ["docker", "logs", "--since", start_time, "-f", container_name]
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1) as process:
            while self.monitoring:
                output = process.stdout.readline()
                if output:
                    self.process_output(output.strip(), container_name)

    def process_output(self, output, container_name):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stage_match = re.search(r'\((\d+)\)Moving to stage (\d+) of (\d+)', output)
        episode_done_match = re.search(r'\((\d+)\)Episode done', output)
        game_completed_match = re.search(r'\((\d+)\)Game completed!', output)

        with self.lock:
            if stage_match:
                env_number, current_stage, max_stage = stage_match.groups()
                if int(current_stage) >= self.minimum_stage:
                    self.container_stages[container_name] = f"[{current_time}] {container_name}({env_number}) reached stage {current_stage} of {max_stage}"
                    self.logger.debug(f"[{current_time}] {container_name}({env_number}) reached stage {current_stage}. Now monitoring...")

            if episode_done_match:
                env_number = episode_done_match.group(1)
                if container_name in self.container_stages:
                    self.logger.debug(f"[{current_time}] 'Episode done' for {container_name}({env_number}): Monitoring stopped.")
                    del self.container_stages[container_name]

            if game_completed_match:
                env_number = game_completed_match.group(1)
                completion_info = f"[{current_time}] {container_name}({env_number}): Game completed!"
                if container_name not in self.game_completion:
                    self.game_completion[container_name] = []
                self.game_completion[container_name].append(completion_info)
                self.logger.debug(f"[{current_time}] {container_name}({env_number}) completed the game at {current_time}! Congratulations!")

    def print_current_status(self):
        """Periodically logs the current status of the monitored containers."""
        while self.monitoring:
            with self.lock:
                if not self.container_stages and all(not completions for completions in self.game_completion.values()):
                    self.logger.info("No containers are currently monitored.")
                else:
                    if self.container_stages:
                        self.logger.info(f"***Currently monitoring statuses for {len(self.container_stages)} container(s)***")
                        for container, stage_info in self.container_stages.items():
                            self.logger.info(stage_info)
                    total_completions = sum(len(completions) for completions in self.game_completion.values())
                    if total_completions:
                        self.logger.info(f"***{total_completions} Game(s) Completed!***")
                        for container, completions in self.game_completion.items():
                            for completion in completions:
                                self.logger.info(completion)
                    else:
                        self.logger.info("No games have been completed yet.")
            time.sleep(60)

    def start_monitoring(self):
        # Check if minimum stage is equal to 0
        if self.minimum_stage == 0:
            self.logger.info("Monitoring disabled, minimum stage is set to 0.")
            return  

        """Starts the monitoring threads after an optional delay."""
        if self.initial_scan:
            self.scan_for_completed_games()
        if self.delay_start > 0:
            self.logger.info(f"Delaying start of monitoring for {self.delay_start} seconds.")
            time.sleep(self.delay_start)

        self.status_thread = threading.Thread(target=self.print_current_status)
        self.status_thread.start()
        for container in self.containers:
            thread = threading.Thread(target=self.follow_logs, args=(container,))
            self.threads.append(thread)
            thread.start()

    def stop_monitoring(self):
        """Stops all monitoring activities."""
        self.monitoring = False
        for thread in self.threads:
            thread.join(timeout=5)  # Join with timeout to prevent hang up
        if self.status_thread.is_alive():
            self.status_thread.join(timeout=5) 
            
if __name__ == "__main__":
    args = parse_args()

    if args.min_stage > 0:
        print(f"Setting minimum stage to {args.min_stage}")
        delay_start = 5 
        initial_scan = True 
        monitor = create_docker_monitor(min_stage=args.min_stage)
        monitor.start_monitoring()
    else:
        print("No minimum stage set. Please provide a minimum stage to start monitoring.")
        # End the script
        print("Monitoring disabled, minimum stage is set to 0.")
        exit(0)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user, stopping monitoring...")
        monitor.stop_monitoring()
