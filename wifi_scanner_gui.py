import tkinter as tk
from tkinter import messagebox
import socket
import pyttsx3

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

def check_network_security():
    """Checks if the network is private or public and updates the UI."""
    ip = get_ip()

    if not ip:
        status_label.config(text="❌ No network detected", fg="red")
        network_status.config(text="", fg="black")  # Hide security status
        return

    status_label.config(text=f"🌐 Connected IP: {ip}", fg="black")

    if ip.startswith(("10.", "192.168.", "172.16.", "172.31.")):
        network_status.config(text="🔒 Private & Secured Network", fg="green")
    else:
        network_status.config(text="⚠️ Public/Unsecured Network", fg="red")
        alert_user("Warning: You are on a public network! Avoid sensitive transactions.")

def alert_user(message):
    """Provides an alert for insecure networks."""
    messagebox.showwarning("Security Alert", message)
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

# Create GUI Window
root = tk.Tk()
root.title("WiFi Risk Detector")
root.geometry("400x250")

title_label = tk.Label(root, text="WiFi Security Scanner", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

status_label = tk.Label(root, text="🔍 Scanning network...", font=("Arial", 12))
status_label.pack(pady=5)

network_status = tk.Label(root, text="", font=("Arial", 12, "bold"))  # Initially empty
network_status.pack(pady=10)

scan_button = tk.Button(root, text="Scan Network", command=check_network_security, font=("Arial", 12))
scan_button.pack(pady=15)

# Run security check when app starts
check_network_security()

# Start the GUI event loop
root.mainloop()
