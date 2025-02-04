import subprocess
import socket
import pyttsx3
import re

def get_ip():
    """Detects the current local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS to get network IP
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def get_wifi_name():
    """Fetches the connected WiFi SSID using airport command."""
    try:
        output = subprocess.check_output(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
        ).decode("utf-8")
        ssid_match = re.search(r"SSID: (.+)", output)
        if ssid_match:
            return ssid_match.group(1).strip()
        return "Unknown"
    except subprocess.CalledProcessError:
        return "Unknown"

def check_network_security(ip, wifi_name):
    """Warns if the network is public (non-private IP range)."""
    print(f"📡 Connected to WiFi: {wifi_name}")
    print(f"🌐 IP Address: {ip}")

    # Check if the IP is in a private range (safe network)
    if ip.startswith(("10.", "192.168.", "172.16.", "172.31.")):
        print("🔒 Connected to a secured network (Private IP Range)")
    else:
        warning_msg = f"⚠️ Warning: You are on a public network ({wifi_name})! Avoid sensitive transactions."
        print(warning_msg)
        alert_user(warning_msg)

def alert_user(message):
    """Provides an audio and text alert for insecure networks."""
    print(message)
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Run the Network Scanner
if __name__ == "__main__":
    ip = get_ip()
    wifi_name = get_wifi_name()
    if ip:
        check_network_security(ip, wifi_name)
    else:
        print("❌ No network detected. Make sure you're connected to WiFi.")
