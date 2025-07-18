import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import matplotlib.pyplot as plt

# Hardcoded stock prices
stock_prices = {
    "AAPL": 180,
    "TSLA": 250,
    "GOOGL": 2800,
    "MSFT": 330,
    "AMZN": 140,
    "META": 310
}

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📈 Stock Portfolio Tracker")
        self.root.geometry("500x650")
        self.entries = {}

        tk.Label(root, text="Enter Stock Quantities", font=("Arial", 16, "bold")).pack(pady=10)

        # Stock entry fields
        for stock in stock_prices:
            frame = tk.Frame(root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{stock} (${stock_prices[stock]}):", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.RIGHT)
            self.entries[stock] = entry

        tk.Button(root, text="Calculate Total", command=self.calculate_total, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)
        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.result_label.pack()

        tk.Button(root, text="Show Charts", command=self.show_charts, bg="purple", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(root, text="Save to File", command=self.save_to_file, bg="blue", fg="white", font=("Arial", 12)).pack(pady=10)

    def calculate_total(self):
        self.portfolio = {}
        total = 0
        for stock, entry in self.entries.items():
            try:
                qty = int(entry.get())
                if qty < 0:
                    raise ValueError
                self.portfolio[stock] = qty
                total += stock_prices[stock] * qty
            except ValueError:
                self.result_label.config(text=f"❌ Invalid quantity for {stock}")
                return
        self.total_value = total
        self.result_label.config(text=f"💰 Total Investment: ${total}")

    def show_charts(self):
        if not hasattr(self, 'portfolio') or not self.portfolio:
            messagebox.showwarning("No Data", "Please calculate total first.")
            return

        # Filter out zero-quantity stocks
        filtered = {k: v for k, v in self.portfolio.items() if v > 0}
        labels = filtered.keys()
        values = [stock_prices[stock]*qty for stock, qty in filtered.items()]

        if not values:
            messagebox.showinfo("Empty", "No stock quantities entered.")
            return

        # Pie Chart
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Portfolio Pie Chart")

        # Bar Chart
        plt.subplot(1, 2, 2)
        plt.bar(labels, values, color='skyblue')
        plt.xlabel("Stock")
        plt.ylabel("Investment ($)")
        plt.title("Investment by Stock")

        plt.tight_layout()
        plt.show()

    def save_to_file(self):
        if not hasattr(self, 'portfolio') or not self.portfolio:
            messagebox.showwarning("No Data", "Please calculate total first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if not file_path:
            return

        if file_path.endswith(".txt"):
            with open(file_path, "w") as f:
                f.write("Stock Portfolio Summary\n")
                f.write("-" * 30 + "\n")
                for stock, qty in self.portfolio.items():
                    f.write(f"{stock}: {qty} shares @ ${stock_prices[stock]} = ${stock_prices[stock]*qty}\n")
                f.write("-" * 30 + "\n")
                f.write(f"Total Investment: ${self.total_value}\n")

        elif file_path.endswith(".csv"):
            with open(file_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Stock", "Quantity", "Price", "Total"])
                for stock, qty in self.portfolio.items():
                    writer.writerow([stock, qty, stock_prices[stock], stock_prices[stock]*qty])
                writer.writerow(["", "", "Total", self.total_value])

        messagebox.showinfo("Saved", "✅ Portfolio saved successfully!")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
