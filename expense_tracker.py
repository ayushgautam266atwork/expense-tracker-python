import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from collections import defaultdict
import threading

# Database Setup
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT NOT NULL,
                  amount REAL NOT NULL,
                  date TEXT NOT NULL,
                  description TEXT)''')
    conn.commit()
    conn.close()

# Database Operations
def add_expense(category, amount, date, description):
    try:
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (category, amount, date, description) VALUES (?, ?, ?, ?)",
                  (category, float(amount), date, description))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def view_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def get_monthly_summary():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    current_month = datetime.now().strftime('%Y-%m')
    c.execute("SELECT category, amount FROM expenses WHERE date LIKE ?", (f"{current_month}%",))
    data = c.fetchall()
    conn.close()
    
    summary = defaultdict(float)
    total = 0
    for category, amount in data:
        summary[category] += amount
        total += amount
    
    return dict(summary), total

# Gritty Monochrome Sports-Editorial Theme
BG_COLOR = "#000000"      # Pure black background
CARD_BG = "#1A1A1A"       # Dark gray cards
INPUT_BG = "#2A2A2A"      # Medium dark gray inputs
ACCENT = "#DC143C"        # Deep red accent (crimson)
ACCENT_HOVER = "#B22222"  # Firebrick (darker red)
TEXT_PRIMARY = "#FFFFFF"  # Pure white text
TEXT_SECONDARY = "#A0A0A0" # Light gray secondary text
SUCCESS = "#DC143C"       # Deep red for success
ERROR = "#8B0000"         # Dark red for errors
STRUCTURAL_LINE = "#333333" # Dark gray for structural elements

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, bg=BG_COLOR, highlightthickness=0, **kwargs)
        self.command = command
        self.text = text
        self.hovered = False
        
        self.rect = self.create_rectangle(2, 2, 198, 48, fill=CARD_BG, outline=ACCENT, width=2)
        self.text_item = self.create_text(100, 25, text=text, fill=TEXT_PRIMARY, 
                                          font=("Impact", 12, "bold"))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
    
    def on_enter(self, e):
        self.hovered = True
        self.animate_hover(ACCENT, ACCENT_HOVER, 0)
    
    def on_leave(self, e):
        self.hovered = False
        self.animate_hover(ACCENT_HOVER, ACCENT, 0)
    
    def animate_hover(self, start, end, step):
        if step > 10:
            return
        
        r1, g1, b1 = int(start[1:3], 16), int(start[3:5], 16), int(start[5:7], 16)
        r2, g2, b2 = int(end[1:3], 16), int(end[3:5], 16), int(end[5:7], 16)
        
        r = r1 + (r2 - r1) * step // 10
        g = g1 + (g2 - g1) * step // 10
        b = b1 + (b2 - b1) * step // 10
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        self.itemconfig(self.rect, fill=color)
        
        self.after(20, lambda: self.animate_hover(start, end, step + 1))
    
    def on_click(self, e):
        self.command()

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EXPENSE TRACKER - DISCIPLINE & CONTROL")
        self.root.geometry("1400x900")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(True, True)
        self.root.state('zoomed')  # Maximize window
        
        init_db()
        self.create_ui()
        self.refresh_table()
    
    def create_ui(self):
        # Main Container with large negative space
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=60)
        
        # Title with gritty minimal typography
        title_frame = tk.Frame(main_frame, bg=BG_COLOR)
        title_frame.pack(fill=tk.X, pady=(0, 50))
        
        # Structural line above title
        structural_line = tk.Canvas(title_frame, height=3, bg=BG_COLOR, highlightthickness=0)
        structural_line.create_line(0, 1, 1400, 1, fill=ACCENT, width=3)
        structural_line.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(title_frame, text="EXPENSE\nTRACKER", 
                        font=("Impact", 48, "bold"), fg=TEXT_PRIMARY, bg=BG_COLOR,
                        justify=tk.LEFT)
        title.pack(side=tk.LEFT, padx=(0, 50))
        
        # Motivational anchor text
        subtitle = tk.Label(title_frame, text="DISCIPLINE • FOCUS • CONTROL", 
                           font=("Impact", 10), fg=TEXT_SECONDARY, bg=BG_COLOR)
        subtitle.pack(side=tk.RIGHT, padx=(0, 50))
        
        # Input Section - Minimalist Grid with Structural Lines
        input_frame = tk.Frame(main_frame, bg=BG_COLOR, relief=tk.FLAT)
        input_frame.pack(fill=tk.X, pady=(0, 50))
        
        input_container = tk.Frame(input_frame, bg=CARD_BG, relief=tk.FLAT)
        input_container.pack(padx=60, pady=40)
        
        # Add structural border
        border_canvas = tk.Canvas(input_container, height=2, bg=CARD_BG, highlightthickness=0)
        border_canvas.create_line(0, 0, 1400, 0, fill=ACCENT, width=2)
        border_canvas.pack(fill=tk.X, pady=(0, 30))
        
        # Create structured layout using frames
        fields_frame = tk.Frame(input_container, bg=CARD_BG)
        fields_frame.pack(fill=tk.X)
        
        # Category section
        cat_frame = tk.Frame(fields_frame, bg=CARD_BG)
        cat_frame.pack(side=tk.LEFT, padx=(0, 40))
        tk.Label(cat_frame, text="CATEGORY", font=("Impact", 10), 
                fg=TEXT_SECONDARY, bg=CARD_BG).pack(anchor="w", pady=(0, 8))
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(cat_frame, textvariable=self.category_var, 
                                     values=["Food", "Transport", "Shopping", "Entertainment", 
                                            "Bills", "Health", "Miscellaneous"], 
                                     font=("Impact", 11), width=18)
        category_combo.pack(ipady=8)
        category_combo.set("Food")
        
        # Amount section
        amt_frame = tk.Frame(fields_frame, bg=CARD_BG)
        amt_frame.pack(side=tk.LEFT, padx=(0, 40))
        tk.Label(amt_frame, text="AMOUNT", font=("Impact", 10), 
                fg=TEXT_SECONDARY, bg=CARD_BG).pack(anchor="w", pady=(0, 8))
        self.amount_entry = tk.Entry(amt_frame, font=("Impact", 11), 
                                     bg=INPUT_BG, fg=TEXT_PRIMARY, 
                                     insertbackground=TEXT_PRIMARY, relief=tk.FLAT, width=20)
        self.amount_entry.pack(ipady=8)
        
        # Date section
        date_frame = tk.Frame(fields_frame, bg=CARD_BG)
        date_frame.pack(side=tk.LEFT, padx=(0, 40))
        tk.Label(date_frame, text="DATE", font=("Impact", 10), 
                fg=TEXT_SECONDARY, bg=CARD_BG).pack(anchor="w", pady=(0, 8))
        self.date_entry = tk.Entry(date_frame, font=("Impact", 11), 
                                   bg=INPUT_BG, fg=TEXT_PRIMARY, 
                                   insertbackground=TEXT_PRIMARY, relief=tk.FLAT, width=20)
        self.date_entry.pack(ipady=8)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Description section
        desc_frame = tk.Frame(fields_frame, bg=CARD_BG)
        desc_frame.pack(side=tk.LEFT)
        tk.Label(desc_frame, text="DESCRIPTION", font=("Impact", 10), 
                fg=TEXT_SECONDARY, bg=CARD_BG).pack(anchor="w", pady=(0, 8))
        self.desc_entry = tk.Entry(desc_frame, font=("Impact", 11), 
                                   bg=INPUT_BG, fg=TEXT_PRIMARY, 
                                   insertbackground=TEXT_PRIMARY, relief=tk.FLAT, width=30)
        self.desc_entry.pack(ipady=8)
        
        # Buttons Frame - Minimalist horizontal layout
        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(pady=(30, 50))
        
        # Structural line above buttons
        btn_line = tk.Canvas(btn_frame, height=2, bg=BG_COLOR, highlightthickness=0)
        btn_line.create_line(0, 0, 1400, 0, fill=STRUCTURAL_LINE, width=1)
        btn_line.pack(fill=tk.X, pady=(0, 20))
        
        ModernButton(btn_frame, "ADD EXPENSE", self.add_expense_action, 
                    width=200, height=50).pack(side=tk.LEFT, padx=(60, 10))
        ModernButton(btn_frame, "DELETE SELECTED", self.delete_selected, 
                    width=200, height=50).pack(side=tk.LEFT, padx=10)
        ModernButton(btn_frame, "MONTHLY SUMMARY", self.show_summary, 
                    width=200, height=50).pack(side=tk.LEFT, padx=10)
        
        # Table Frame with minimal structural design
        table_container = tk.Frame(main_frame, bg=BG_COLOR)
        table_container.pack(fill=tk.BOTH, expand=True)
        
        # Structural frame with minimal border
        table_frame = tk.Frame(table_container, bg=CARD_BG, relief=tk.FLAT)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=(0, 40))
        
        # Add top structural line
        table_border = tk.Canvas(table_frame, height=2, bg=CARD_BG, highlightthickness=0)
        table_border.create_line(0, 0, 1400, 0, fill=ACCENT, width=1)
        table_border.pack(fill=tk.X, pady=(20, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview with gritty styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                       background=CARD_BG, 
                       foreground=TEXT_PRIMARY, 
                       fieldbackground=CARD_BG,
                       rowheight=45,
                       font=("Impact", 10))
        style.configure("Treeview.Heading", 
                       background=CARD_BG, 
                       foreground=ACCENT, 
                       font=("Impact", 11, "bold"))
        style.map("Treeview", background=[("selected", INPUT_BG)])
        
        # Configure Treeview borders
        style.configure("Treeview", borderwidth=0, relief="flat")
        style.map("Treeview", borderwidth=[("selected", 0)])
        
        self.tree = ttk.Treeview(table_frame, columns=("ID", "Category", "Amount", "Date", "Description"),
                                show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("ID", text="NO.")
        self.tree.heading("Category", text="CATEGORY")
        self.tree.heading("Amount", text="AMOUNT")
        self.tree.heading("Date", text="DATE")
        self.tree.heading("Description", text="DESCRIPTION")
        
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Category", width=180, anchor="center")
        self.tree.column("Amount", width=180, anchor="center")
        self.tree.column("Date", width=180, anchor="center")
        self.tree.column("Description", width=500, anchor="center")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def add_expense_action(self):
        category = self.category_var.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        description = self.desc_entry.get()
        
        if not amount or not category:
            messagebox.showerror("Error", "Please fill in Category and Amount!")
            return
        
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number!")
            return
        
        if add_expense(category, amount, date, description):
            messagebox.showinfo("Success", "Expense added successfully!")
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showerror("Error", "Failed to add expense!")
    
    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        expenses = view_expenses()
        for i, exp in enumerate(expenses, 1):
            self.tree.insert("", tk.END, values=(i, exp[1], f"₹{exp[2]:.2f}", exp[3], exp[4]), tags=(exp[0],))
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an expense to delete!")
            return
        
        for item in selected:
            expense_id = self.tree.item(item, 'tags')[0]
            delete_expense(expense_id)
        
        messagebox.showinfo("Success", "Selected expense(s) deleted!")
        self.refresh_table()
    
    def show_summary(self):
        summary, total = get_monthly_summary()
        
        if not summary:
            messagebox.showinfo("Monthly Summary", "No expenses recorded this month!")
            return
        
        # AI-like Insights
        max_category = max(summary, key=summary.get)
        max_amount = summary[max_category]
        avg_expense = total / len(summary)
        
        summary_text = f"📊 Monthly Summary for {datetime.now().strftime('%B %Y')}\n\n"
        summary_text += f"Total Spent: ₹{total:.2f}\n\n"
        summary_text += "Breakdown by Category:\n"
        for cat, amt in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            percentage = (amt / total) * 100
            summary_text += f"  • {cat}: ₹{amt:.2f} ({percentage:.1f}%)\n"
        
        summary_text += f"\n💡 Smart Insights:\n"
        summary_text += f"  • You spent the most on {max_category} (₹{max_amount:.2f})\n"
        summary_text += f"  • Average expense per category: ₹{avg_expense:.2f}\n"
        
        if summary[max_category] > total * 0.4:
            summary_text += f"  • ⚠️ {max_category} accounts for over 40% of your spending!\n"
        
        messagebox.showinfo("Monthly Summary", summary_text)

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
