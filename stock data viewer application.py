import datetime
import yfinance as yf
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

def get_stock_data():
    stock_name = stock_entry.get().strip().upper()
    if not stock_name:
        result_label.config(text="Please enter a stock symbol.", foreground="red", font=("Helvetica", 14, "bold"))
        clear_labels_and_charts()
        return

    try:
        ticker = yf.Ticker(stock_name)
        data = ticker.history(period="1mo")

        if data.empty:
            result_label.config(text=f"No data found for symbol: {stock_name}", font=("Helvetica", 14, "bold"), foreground="red")
            clear_labels_and_charts()
            return

        # Display stock data
        result_label.config(text=f"Data of stock {stock_name} in $", font=("Helvetica", 14, "bold"), foreground="darkblue")
        result_label2.config(text=f"Current Price: ${round(data['Close'].iloc[-1], 2)}")
        result_label3.config(text=f"Open: ${round(data['Open'].iloc[-1], 2)}", foreground="green")
        result_label4.config(text=f"High: ${round(data['High'].max(), 2)}", foreground="green")
        result_label5.config(text=f"Low: ${round(data['Low'].min(), 2)}", foreground="red")
        result_label6.config(text=f"Avg Volume: {round(data['Volume'].mean(), 2)}", foreground="darkblue")

        # Plot Line Chart
        ax1.clear()
        ax1.plot(data.index, data["Close"], color='blue', linestyle='-', label='Closing Price')
        ax1.legend(loc='upper left')
        ax1.set_title("Historical Stock Prices")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Closing Price ($)")
        ax1.grid(True)

        # Candlestick Chart
        ohlc = data.reset_index()
        ohlc['Date'] = ohlc['Date'].map(mdates.date2num)
        ohlc_data = ohlc[['Date', 'Open', 'High', 'Low', 'Close']]

        ax2.clear()
        candlestick_ohlc(ax2, ohlc_data.values, width=0.6, colorup='g', colordown='r', alpha=0.8)
        ax2.set_title("Candlestick Chart")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Stock Price ($)")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax2.xaxis_date()
        ax2.grid(True)

        fig.tight_layout()
        canvas.draw()

    except Exception as e:
        result_label.config(text=f"Error fetching data: {str(e)}", font=("Helvetica", 14, "bold"), foreground="red")
        clear_labels_and_charts()

def clear_labels_and_charts():
    result_label2.config(text="")
    result_label3.config(text="")
    result_label4.config(text="")
    result_label5.config(text="")
    result_label6.config(text="")
    ax1.clear()
    ax2.clear()
    canvas.draw()

# Create main window
root = tk.Tk()
root.title("📈 Stock Data Viewer")
root.geometry("1000x800")
root.configure(bg="white")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14))
style.configure("TLabel", font=("Helvetica", 12), background="white")

# Stock input section
stock_label = ttk.Label(root, text="Enter Stock Symbol:", style="TLabel")
stock_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

stock_entry = ttk.Entry(root, width=20)
stock_entry.grid(row=0, column=1, padx=10, pady=10)

search_button = ttk.Button(root, text="Search", command=get_stock_data, style="TButton")
search_button.grid(row=0, column=2, padx=10, pady=10)

# Result Labels
result_label = ttk.Label(root, text="", style="TLabel")
result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

result_label2 = ttk.Label(root, text="", style="TLabel")
result_label2.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

result_label3 = ttk.Label(root, text="", style="TLabel")
result_label3.grid(row=3, column=0, padx=10, pady=5)

result_label4 = ttk.Label(root, text="", style="TLabel")
result_label4.grid(row=3, column=1, padx=10, pady=5)

result_label5 = ttk.Label(root, text="", style="TLabel")
result_label5.grid(row=4, column=0, padx=10, pady=5)

result_label6 = ttk.Label(root, text="", style="TLabel")
result_label6.grid(row=4, column=1, padx=10, pady=5)

# Matplotlib Figure
fig = Figure(figsize=(9, 5))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=6, column=0, columnspan=3, pady=10)

# Run main loop
root.mainloop()
