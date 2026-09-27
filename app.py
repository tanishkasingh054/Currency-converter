import json
import tkinter as tk
from datetime import datetime
from tkinter import ttk

import requests


API_URL = "https://api.frankfurter.app/latest"
SUPPORTED_CURRENCIES = {
    "USD": "US Dollar ($)",
    "EUR": "Euro (€)",
    "JPY": "Japanese Yen (¥)",
    "GBP": "British Pound (£)",
    "CNY": "Chinese Yuan (¥)",
    "AUD": "Australian Dollar (A$)",
    "CAD": "Canadian Dollar (C$)",
    "KWD": "Kuwaiti Dinar (KD)",
    "KRW": "South Korean Won (₩)",
    "INR": "Indian Rupee (₹)",
}


def validate_amount(raw_value):
    """Validate the input amount and return a numeric value or an error message."""
    value = (raw_value or "").strip()

    if value == "":
        return None, "Please enter an amount to convert."

    try:
        amount = float(value)
    except ValueError:
        return None, "Please enter a valid number."

    if amount < 0:
        return None, "Amount cannot be negative."

    return amount, None


def calculate_converted_amount(amount, rate):
    """Return the converted amount using the exchange rate."""
    return amount * rate


def fetch_exchange_rate(from_currency, to_currency):
    """Fetch the latest exchange rate from the Frankfurter API."""
    try:
        response = requests.get(
            f"{API_URL}?from={from_currency}&to={to_currency}",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "rates" not in data or to_currency not in data["rates"]:
            raise ValueError("The selected currencies are not available in the API response.")

        rate = data["rates"][to_currency]
        update_time = data.get("date")
        return rate, update_time, None

    except requests.exceptions.Timeout:
        return None, None, "The request timed out. Please try again."
    except requests.exceptions.RequestException:
        return None, None, "Could not connect to the exchange rate service. Please check your internet connection."
    except (ValueError, json.JSONDecodeError):
        return None, None, "The exchange rate service returned an unexpected response."


def create_app():
    """Create and configure the main Tkinter window."""
    root = tk.Tk()
    root.title("Currency Converter")
    root.geometry("450x500")
    root.resizable(False, False)
    root.configure(bg="#f4f7fb")

    style = ttk.Style(root)
    style.theme_use("clam")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    heading = tk.Label(
        root,
        text="Currency Converter",
        font=("Arial", 24, "bold"),
        fg="#1f2937",
        bg="#f4f7fb",
        pady=20,
    )
    heading.grid(row=0, column=0, columnspan=2, sticky="nsew")

    amount_label = tk.Label(
        root,
        text="Amount",
        font=("Arial", 12, "bold"),
        bg="#f4f7fb",
        fg="#374151",
    )
    amount_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=25, pady=(0, 6))

    amount_entry = tk.Entry(
        root,
        font=("Arial", 14),
        width=30,
        bd=1,
        relief="solid",
    )
    amount_entry.grid(row=2, column=0, columnspan=2, padx=25, pady=(0, 12), sticky="ew")

    from_label = tk.Label(
        root,
        text="From",
        font=("Arial", 11, "bold"),
        bg="#f4f7fb",
        fg="#374151",
    )
    from_label.grid(row=3, column=0, sticky="w", padx=25, pady=6)

    to_label = tk.Label(
        root,
        text="To",
        font=("Arial", 11, "bold"),
        bg="#f4f7fb",
        fg="#374151",
    )
    to_label.grid(row=3, column=1, sticky="w", padx=25, pady=6)

    from_currency = ttk.Combobox(
        root,
        values=list(SUPPORTED_CURRENCIES.keys()),
        state="readonly",
        width=20,
    )
    from_currency.set("USD")
    from_currency.grid(row=4, column=0, padx=25, pady=(0, 12), sticky="ew")

    to_currency = ttk.Combobox(
        root,
        values=list(SUPPORTED_CURRENCIES.keys()),
        state="readonly",
        width=20,
    )
    to_currency.set("EUR")
    to_currency.grid(row=4, column=1, padx=25, pady=(0, 12), sticky="ew")

    buttons_frame = tk.Frame(root, bg="#f4f7fb")
    buttons_frame.grid(row=5, column=0, columnspan=2, padx=25, pady=8, sticky="ew")
    buttons_frame.columnconfigure(0, weight=1)
    buttons_frame.columnconfigure(1, weight=1)
    buttons_frame.columnconfigure(2, weight=1)

    convert_button = tk.Button(
        buttons_frame,
        text="Convert",
        bg="#4f46e5",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=12,
        pady=8,
        command=lambda: None,
    )
    convert_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

    swap_button = tk.Button(
        buttons_frame,
        text="Swap",
        bg="#dbeafe",
        fg="#1e3a8a",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=12,
        pady=8,
        command=lambda: None,
    )
    swap_button.grid(row=0, column=1, sticky="ew", padx=8)

    clear_button = tk.Button(
        buttons_frame,
        text="Clear",
        bg="#e5e7eb",
        fg="#111827",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=12,
        pady=8,
        command=lambda: None,
    )
    clear_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

    result_var = tk.StringVar()
    result_var.set("Converted amount will appear here")
    result_label = tk.Label(
        root,
        textvariable=result_var,
        font=("Arial", 14, "bold"),
        bg="#ecfeff",
        fg="#0f172a",
        justify="center",
        wraplength=350,
        pady=16,
        borderwidth=1,
        relief="solid",
    )
    result_label.grid(row=6, column=0, columnspan=2, padx=25, pady=(10, 6), sticky="ew")

    info_var = tk.StringVar()
    info_var.set("Exchange rate info will appear here")
    info_label = tk.Label(
        root,
        textvariable=info_var,
        font=("Arial", 10),
        bg="#f4f7fb",
        fg="#475569",
        justify="left",
        wraplength=350,
    )
    info_label.grid(row=7, column=0, columnspan=2, padx=25, pady=(0, 8), sticky="ew")

    status_var = tk.StringVar()
    status_var.set("")
    status_label = tk.Label(
        root,
        textvariable=status_var,
        fg="#b91c1c",
        bg="#f4f7fb",
        font=("Arial", 10),
        wraplength=350,
        justify="left",
    )
    status_label.grid(row=8, column=0, columnspan=2, padx=25, sticky="ew")

    def handle_convert():
        """Convert the entered amount using the live exchange rate."""
        amount, error = validate_amount(amount_entry.get())
        if error:
            status_var.set(error)
            result_var.set("Converted amount will appear here")
            info_var.set("Exchange rate info will appear here")
            return

        source_currency = from_currency.get()
        target_currency = to_currency.get()

        if source_currency == target_currency:
            final_amount = amount
            rate = 1.0
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_var.set("")
            result_var.set(f"{final_amount:.2f} {source_currency} = {final_amount:.2f} {target_currency}")
            info_var.set(f"Exchange rate: 1 {source_currency} = 1 {target_currency} | Updated: {update_time}")
            return

        rate, update_time, error_message = fetch_exchange_rate(source_currency, target_currency)
        if error_message:
            status_var.set(error_message)
            result_var.set("Converted amount will appear here")
            info_var.set("Exchange rate info will appear here")
            return

        converted_amount = calculate_converted_amount(amount, rate)
        status_var.set("")
        result_var.set(f"{amount:.2f} {source_currency} = {converted_amount:.2f} {target_currency}")
        info_var.set(f"Exchange rate: 1 {source_currency} = {rate:.4f} {target_currency} | Updated: {update_time}")

    def handle_swap():
        """Swap source and target currencies."""
        source_value = from_currency.get()
        target_value = to_currency.get()
        from_currency.set(target_value)
        to_currency.set(source_value)

    def handle_clear():
        """Clear all inputs and reset the result area."""
        amount_entry.delete(0, tk.END)
        from_currency.set("USD")
        to_currency.set("EUR")
        result_var.set("Converted amount will appear here")
        info_var.set("Exchange rate info will appear here")
        status_var.set("")

    convert_button.configure(command=handle_convert)
    swap_button.configure(command=handle_swap)
    clear_button.configure(command=handle_clear)

    return root


if __name__ == "__main__":
    window = create_app()
    window.mainloop()
