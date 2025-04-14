import os
import psutil
import requests
import winreg
import wmi
import datetime
import subprocess

# API for checking IP and domain reputation (AbuseIPDB, VirusTotal, etc.)
MALICIOUS_IP_CHECK_API = "https://api.abuseipdb.com/api/v2/check"
API_KEY = ""  # Replace with a valid API key

def check_running_processes():
    """Check running processes for suspicious behavior."""
    print("[+] Scanning running processes...")
    suspicious_processes = []
    known_suspicious = ["mimikatz.exe", "powershell.exe -enc", "cmd.exe /c", "rundll32.exe", "wscript.exe"]

    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            process_name = proc.info['name'].lower()
            cmdline = " ".join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ""

            if any(proc in cmdline or proc in process_name for proc in known_suspicious):
                suspicious_processes.append((proc.info['pid'], process_name, cmdline))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if suspicious_processes:
        print("[!] Suspicious processes detected:")
        for pid, name, cmd in suspicious_processes:
            print(f"   PID: {pid}, Name: {name}, CMD: {cmd}")
    else:
        print("[-] No suspicious processes found.")

def check_network_connections():
    """Check for suspicious network connections."""
    print("[+] Checking active network connections...")
    suspicious_ips = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr:
            ip = conn.raddr.ip
            if check_ip_reputation(ip):
                suspicious_ips.append(ip)

    if suspicious_ips:
        print("[!] Suspicious network connections detected:")
        for ip in suspicious_ips:
            print(f"   Malicious IP found: {ip}")
    else:
        print("[-] No suspicious network connections found.")

def check_ip_reputation(ip):
    """Check if an IP is malicious using an external API."""
    headers = {"Key": API_KEY}
    params = {"ipAddress": ip, "verbose": "true"}

    try:
        response = requests.get(MALICIOUS_IP_CHECK_API, headers=headers, params=params)
        data = response.json()
        return data.get("data", {}).get("abuseConfidenceScore", 0) > 50
    except Exception as e:
        print(f"[-] Error checking IP reputation: {e}")
        return False

def analyze_event_logs():
    """Analyze Windows Security Event Logs for suspicious activity."""
    print("[+] Analyzing Windows Event Logs...")
    log = wmi.WMI(namespace="SecurityCenter2")

    suspicious_events = []
    for event in log.Win32_NTLogEvent(EventType=5):  # EventType=5 (Security)
        if event.EventCode in ["4625", "4740", "4767"]:  # Failed logins, account locks, etc.
            suspicious_events.append((event.EventCode, event.Message, event.TimeGenerated))

    if suspicious_events:
        print("[!] Suspicious events detected:")
        for code, msg, time in suspicious_events:
            print(f"   Event Code: {code}, Time: {time}, Message: {msg[:100]}")
    else:
        print("[-] No suspicious events found.")

def check_registry_persistence():
    """Check registry for persistence mechanisms."""
    print("[+] Checking registry for persistence entries...")
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
    ]

    suspicious_entries = []
    for hkey, path in reg_paths:
        try:
            with winreg.OpenKey(hkey, path, 0, winreg.KEY_READ) as reg:
                i = 0
                while True:
                    try:
                        value = winreg.EnumValue(reg, i)
                        suspicious_entries.append(value)
                        i += 1
                    except OSError:
                        break
        except FileNotFoundError:
            continue

    if suspicious_entries:
        print("[!] Suspicious registry persistence found:")
        for entry in suspicious_entries:
            print(f"   Name: {entry[0]}, Path: {entry[1]}")
    else:
        print("[-] No suspicious registry entries found.")

def scan_system():
    """Run all security checks."""
    print("=== Windows Security Scan ===")
    check_running_processes()
    check_network_connections()
    analyze_event_logs()
    check_registry_persistence()
    print("=== Scan Complete ===")

if __name__ == "__main__":
    scan_system()
