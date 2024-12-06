import tkinter as tk
from tkinter import messagebox
from flask import Flask, jsonify
from flask_cors import CORS
import threading

# Create the Flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
mock_routes = {}

# Flask route for dynamic URL handling
@app.route("/<path:url>", methods=["GET", "POST", "PUT", "DELETE"])
def mock_response(url):
    response = mock_routes.get(url, "Endpoint not found!")
    return jsonify(response) if isinstance(response, dict) else response, 200 if url in mock_routes else 404

def start_flask_server(port):
    try:
        app.run(port=int(port), host="0.0.0.0")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start server: {e}")

# Function to start the server in a separate thread
def run_server():
    port = port_entry.get()
    if not port.isdigit():
        messagebox.showerror("Error", "Port must be a number!")
        return
    threading.Thread(target=start_flask_server, args=(port,), daemon=True).start()
    status_label.config(text=f"Server running on port {port}", fg="green")

# Function to add a mock route
def add_mock_route():
    url = url_entry.get()
    response = response_text.get("1.0", tk.END).strip()  # Get text from the Text widget

    if not url or not response:
        messagebox.showerror("Error", "URL and Response fields cannot be empty!")
        return

    status_label.config(text="Adding response, please wait...", fg="blue")
    root.update_idletasks()  # Force the UI to update

    try:
        mock_routes[url] = response
        status_label.config(text=f"Mock endpoint added: {url}", fg="green")
        messagebox.showinfo("Success", f"Added mock endpoint: {url}")
    except Exception as e:
        status_label.config(text="Error adding response", fg="red")
        messagebox.showerror("Error", f"Failed to add endpoint: {e}")

# Create the Tkinter GUI
root = tk.Tk()
root.title("Mock Server")

tk.Label(root, text="Port:").grid(row=0, column=0, padx=10, pady=5)
port_entry = tk.Entry(root)
port_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="URL:").grid(row=1, column=0, padx=10, pady=5)
url_entry = tk.Entry(root)
url_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Response:").grid(row=2, column=0, padx=10, pady=5)
response_text = tk.Text(root, height=10, width=50)  # Use Text widget for large input
response_text.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Add Mock Route", command=add_mock_route)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

start_button = tk.Button(root, text="Start Mock Server", command=run_server)
start_button.grid(row=4, column=0, columnspan=2, pady=10)

status_label = tk.Label(root, text="", fg="black")
status_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
