import datetime
import subprocess
import time
import threading
import os
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logging_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(logging_dir):
    os.mkdir(logging_dir)


def read_output(file, pipe):
    with open(file, "wb") as f:
        f.write(b"")

    while True:
        line = pipe.readline()
        if not line:
            break
        with open(file, "ab") as f:
            f.write(line)

    logger.debug(f"Finished reading {file}")


run_number = 0


def run_process(working_directory, label, cmd, timeout):
    start_process_time = time.time()
    logger.info(f"Running {cmd} in {working_directory}")
    proc = subprocess.Popen(
        cmd,
        cwd=working_directory,
        stderr=subprocess.PIPE,  # Merge stdout and stderr
        stdout=subprocess.PIPE,
        close_fds=True)

    global run_number
    run_number += 1
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S-%f')
    output_file = f"{logging_dir}/{label}_{current_time}_{run_number}"

    with open(f"{output_file}.cmd.txt", "w") as f:
        f.write(f"Working directory: {working_directory}\n")
        f.write(f"Command: {cmd}\n")
        f.write(f"Timeout: {timeout}\n")

    tr1 = threading.Thread(target=read_output, args=(f"{output_file}.stdout.txt", proc.stdout))
    tr1.start()

    tr2 = threading.Thread(target=read_output, args=(f"{output_file}.stderr.txt", proc.stderr))
    tr2.start()

    is_timed_out = False
    while True:
        elapsed = time.time() - start_process_time
        return_code = proc.poll()
        if return_code is not None:
            logger.info(f"Process {proc.pid} - {label} finished with return code {return_code}")
            break

        if elapsed > timeout:
            is_timed_out = True
            logger.warning(f"Killing process {proc.pid} - {label} due to being timed out ({elapsed:.2f}s)")
            proc.kill()
            break
        time.sleep(1)

    with open(f"{output_file}.cmd.txt", "a") as f:
        f.write("Return code: {}\n".format(return_code))
        f.write(f"Running time: {elapsed:.2f}\n")
        f.write("Is timed out: {}\n".format(is_timed_out))

    tr1.join()
    tr2.join()


def run_process_in_bkg(cmd, timeout=86400, working_directory=os.getcwd(), label="cmd"):
    t = threading.Thread(target=run_process, args=(working_directory, label, cmd, timeout))
    t.start()
    return t


if __name__ == "__main__":
    background_tasks = []
    for i in range(10):
        background_tasks.append(run_process_in_bkg("python", timeout=10))

    for task in background_tasks:
        task.join()
