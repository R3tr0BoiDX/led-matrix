import subprocess


def ping_host(target_host="1.1.1.1") -> bool:
    """
    Ping a host and return True if reachable, False otherwise.
    """
    result = subprocess.run(
        ["ping", "-c", "1", target_host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0
