"""
EXPENSE TRACKER PRO - Complete Financial Management System
===========================================================
A feature-rich expense tracking application with:
- Colorful terminal interface
- Data persistence (JSON storage)
- Category-wise analysis
- Search and filtering
- Export functionality
- Analytics Dashboard with charts
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# NEW IMPORTS FOR DATA VISUALIZATION
# ============================================================
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ Pandas/Matplotlib not installed. Install with: pip install pandas matplotlib")


# ============================================================
# PART 1: COLOR SETUP FOR TERMINAL DISPLAY
# ============================================================

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ''
    COLORS_AVAILABLE = False


# ============================================================
# PART 2: MAIN EXPENSE TRACKER CLASS
# ============================================================

class ExpenseTracker:
    """
    Main application class that handles everything:
    - Data storage and retrieval
    - User interface
    - Business logic
    - File operations
    """
    
    def __init__(self, filename: str = "expenses.json"):
        """
        CONSTRUCTOR - Runs when you create a new ExpenseTracker object
        Sets up the initial state of the application
        """
        self.filename = filename
        self.expenses = []
        self.categories = [
            "Food", "Transport", "Shopping", "Entertainment", 
            "Bills", "Healthcare", "Education", "Other"
        ]
        self.load_data()
    
    # ============================================================
    # PART 3: DATA PERSISTENCE (Saving/Loading)
    # ============================================================
    
    def load_data(self) -> None:
        """Load expenses from JSON file into memory"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.expenses = json.load(f)
            else:
                self.expenses = []
        except (json.JSONDecodeError, FileNotFoundError):
            self.expenses = []
    
    def save_data(self) -> None:
        """Save current expenses from memory to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.expenses, f, indent=4)
    
    # ============================================================
    # PART 4: ADD EXPENSE
    # ============================================================
    
    def add_expense(self) -> None:
        """Interactive function to add a new expense"""
        self.clear_screen()
        self.print_header("➕ ADD NEW EXPENSE")
        
        # Get Amount
        while True:
            try:
                amount = float(input("💰 Amount (PKR): "))
                if amount <= 0:
                    print(f"{Fore.RED}❌ Amount must be positive!{Style.RESET_ALL}")
                    continue
                break
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")
        
        # Get Category
        print(f"\n{Fore.CYAN}📂 Available Categories:{Style.RESET_ALL}")
        for i, cat in enumerate(self.categories, 1):
            print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {cat}")
            
        while True:
            try:
                cat_choice = int(input("\n🔢 Select category (1-8): "))
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]
                    break
                else:
                    print(f"{Fore.RED}❌ Please enter a number between 1-8!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")
        
        # Get Description
        description = input("📝 Description: ").strip()
        if not description:
            description = "No description"
        
        # Get Date
        date_input = input("📅 Date (DD-MM-YYYY, press Enter for today): ").strip()
        if date_input:
            try:
                datetime.strptime(date_input, "%d-%m-%Y")
                date = date_input
            except ValueError:
                print(f"{Fore.YELLOW}⚠️ Invalid date format! Using today's date.{Style.RESET_ALL}")
                date = datetime.now().strftime("%d-%m-%Y")
        else:
            date = datetime.now().strftime("%d-%m-%Y")
        
        # Create Expense Entry
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "category": category,
            "description": description,
            "date": date,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save and Confirm
        self.expenses.append(expense)
        self.save_data()
        
        print(f"\n{Fore.GREEN}✅ Expense added successfully!{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}💵 Amount:{Style.RESET_ALL} PKR {amount:.2f}")
        print(f"   {Fore.CYAN}📂 Category:{Style.RESET_ALL} {category}")
        print(f"   {Fore.CYAN}📝 Description:{Style.RESET_ALL} {description}")
        print(f"   {Fore.CYAN}📅 Date:{Style.RESET_ALL} {date}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 5: VIEW EXPENSES
    # ============================================================
    
    def view_expenses(self) -> None:
        """Display all expenses in a formatted table"""
        self.clear_screen()
        self.print_header("📊 VIEW ALL EXPENSES")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses recorded yet!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        total = sum(exp['amount'] for exp in self.expenses)
        
        print(f"{Fore.CYAN}{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<30}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*75}{Style.RESET_ALL}")
        
        for exp in self.expenses:
            if exp['amount'] > 1000:
                amount_color = Fore.RED
            elif exp['amount'] > 500:
                amount_color = Fore.YELLOW
            else:
                amount_color = Fore.GREEN
                
            print(f"{exp['id']:<4} {exp['date']:<12} {exp['category']:<15} {amount_color}PKR {exp['amount']:<10.2f}{Style.RESET_ALL} {exp['description'][:30]:<30}")
        
        print(f"\n{Fore.CYAN}📈 Total Expenses:{Style.RESET_ALL} {Fore.GREEN}PKR {total:.2f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Total Entries:{Style.RESET_ALL} {len(self.expenses)}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 6: VIEW SUMMARY
    # ============================================================
    
    def view_summary(self) -> None:
        """Generate a category-wise summary with visual bar charts"""
        self.clear_screen()
        self.print_header("📈 EXPENSE SUMMARY")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to summarize!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        category_totals = {}
        for cat in self.categories:
            category_totals[cat] = 0
            
        for exp in self.expenses:
            category_totals[exp['category']] += exp['amount']
        
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        total = sum(category_totals.values())
        max_amount = max(category_totals.values()) if category_totals else 1
        
        print(f"\n{Fore.CYAN}📊 Category-wise Breakdown{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}\n")
        
        for cat, amount in sorted_cats:
            if amount == 0:
                continue
                
            percentage = (amount / total * 100) if total > 0 else 0
            bar_length = int((amount / max_amount) * 30)
            
            if percentage > 30:
                color = Fore.RED
            elif percentage > 15:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
                
            bar = "█" * bar_length
            print(f"{color}{cat:<15}{Style.RESET_ALL} {Fore.CYAN}PKR {amount:<10.2f}{Style.RESET_ALL} {color}{bar}{Style.RESET_ALL} {percentage:.1f}%")
        
        active_categories = len([a for a in category_totals.values() if a > 0])
        print(f"\n{Fore.GREEN}💰 Total: PKR {total:.2f}{Style.RESET_ALL}")
        if active_categories > 0:
            print(f"{Fore.CYAN}📊 Average per category: PKR {total/active_categories:.2f}{Style.RESET_ALL}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 7: DELETE EXPENSE
    # ============================================================
    
    def delete_expense(self) -> None:
        """Delete an expense by its unique ID"""
        self.clear_screen()
        self.print_header("🗑️ DELETE EXPENSE")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to delete!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}Recent Expenses:{Style.RESET_ALL}")
        for exp in self.expenses[-10:]:
            print(f"   {Fore.YELLOW}ID:{exp['id']}{Style.RESET_ALL} - PKR {exp['amount']:.2f} - {exp['description']}")
        
        try:
            exp_id = int(input(f"\n🔢 Enter expense ID to delete: "))
            found = False
            
            for i, exp in enumerate(self.expenses):
                if exp['id'] == exp_id:
                    confirm = input(f"⚠️ Delete '{exp['description']}' for PKR {exp['amount']:.2f}? (y/n): ")
                    if confirm.lower() == 'y':
                        del self.expenses[i]
                        self.save_data()
                        print(f"{Fore.GREEN}✅ Expense deleted successfully!{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}❌ Deletion cancelled.{Style.RESET_ALL}")
                    found = True
                    break
                    
            if not found:
                print(f"{Fore.RED}❌ Expense not found!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Invalid input!{Style.RESET_ALL}")
            
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 8: SEARCH EXPENSES
    # ============================================================
    
    def search_expenses(self) -> None:
        """Search functionality with two modes: Keyword or Category"""
        self.clear_screen()
        self.print_header("🔍 SEARCH EXPENSES")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to search!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}Search by:{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}1.{Style.RESET_ALL} Keyword")
        print(f"   {Fore.YELLOW}2.{Style.RESET_ALL} Category")
        
        choice = input(f"\n🔢 Enter choice (1-2): ").strip()
        results = []
        
        if choice == '1':
            keyword = input("🔍 Enter keyword: ").strip().lower()
            if not keyword:
                print(f"{Fore.RED}❌ Please enter a keyword!{Style.RESET_ALL}")
                input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                return
                
            results = [exp for exp in self.expenses if 
                      keyword in exp['description'].lower() or 
                      keyword in exp['category'].lower()]
        
        elif choice == '2':
            print(f"\n{Fore.CYAN}📂 Available Categories:{Style.RESET_ALL}")
            for i, cat in enumerate(self.categories, 1):
                print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {cat}")
                
            try:
                cat_choice = int(input("\n🔢 Select category: "))
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]
                    results = [exp for exp in self.expenses if exp['category'] == category]
                else:
                    print(f"{Fore.RED}❌ Invalid category!{Style.RESET_ALL}")
                    input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                    return
            except ValueError:
                print(f"{Fore.RED}❌ Invalid input!{Style.RESET_ALL}")
                input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                return
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        if results:
            print(f"\n{Fore.GREEN}✅ Found {len(results)} expense(s):{Style.RESET_ALL}\n")
            total = sum(exp['amount'] for exp in results)
            for exp in results:
                print(f"   {Fore.CYAN}📅 {exp['date']}{Style.RESET_ALL}")
                print(f"   {Fore.YELLOW}💰 PKR {exp['amount']:.2f}{Style.RESET_ALL}")
                print(f"   📂 {exp['category']}")
                print(f"   📝 {exp['description']}")
                print(f"   {Fore.CYAN}{'-'*40}{Style.RESET_ALL}")
            print(f"\n{Fore.GREEN}💰 Total: PKR {total:.2f}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}❌ No matching expenses found!{Style.RESET_ALL}")
            
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 9: UTILITY FUNCTIONS
    # ============================================================
    
    def clear_screen(self) -> None:
        """Clear terminal screen for cleaner UI"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str) -> None:
        """Print a visually styled header with emojis"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}🎯 {title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # ============================================================
    # PART 10: MAIN MENU DISPLAY
    # ============================================================
    
    def show_menu(self) -> None:
        """Display the main menu with all available options"""
        self.clear_screen()
        print(f"""
{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════╗
║                                                          ║
║     💰  EXPENSE TRACKER PRO - DASHBOARD EDITION        ║
║                                                          ║
║     Track, Analyze & Visualize your spending!           ║
║                                                          ║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}

{Fore.CYAN}📊 Total Expenses: {Fore.GREEN}PKR {sum(exp['amount'] for exp in self.expenses):.2f}{Style.RESET_ALL}
{Fore.CYAN}📝 Total Entries: {Fore.YELLOW}{len(self.expenses)}{Style.RESET_ALL}

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}

{Fore.CYAN}📌 MAIN MENU:{Style.RESET_ALL}

  {Fore.GREEN}1.{Style.RESET_ALL} ➕  Add Expense
  {Fore.GREEN}2.{Style.RESET_ALL} 📊  View All Expenses
  {Fore.GREEN}3.{Style.RESET_ALL} 📈  View Summary
  {Fore.GREEN}4.{Style.RESET_ALL} 🔍  Search Expenses
  {Fore.GREEN}5.{Style.RESET_ALL} 🗑️  Delete Expense
  {Fore.GREEN}6.{Style.RESET_ALL} 💾  Export Data
  {Fore.GREEN}7.{Style.RESET_ALL} 📊  Analytics Dashboard (NEW!)
  {Fore.GREEN}8.{Style.RESET_ALL} 🚀  Exit

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
""")
    
    # ============================================================
    # PART 11: EXPORT DATA TO CSV
    # ============================================================
    
    def export_data(self) -> None:
        """Export all expenses to a CSV file with timestamp"""
        self.clear_screen()
        self.print_header("💾 EXPORT DATA")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to export!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        csv_filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(csv_filename, 'w') as f:
                f.write("ID,Date,Category,Amount,Description\n")
                for exp in self.expenses:
                    f.write(f"{exp['id']},{exp['date']},{exp['category']},{exp['amount']},{exp['description']}\n")
            
            print(f"{Fore.GREEN}✅ Data exported to {csv_filename}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📁 File saved in current directory{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error exporting data: {e}{Style.RESET_ALL}")
            
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 12: DATA ANALYSIS & VISUALIZATION (NEW!)
    # ============================================================
    
    def analyze_data(self) -> Optional[pd.DataFrame]:
        """Convert expenses to Pandas DataFrame for analysis"""
        if not self.expenses:
            return None
        
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Pandas not available! Install with: pip install pandas{Style.RESET_ALL}")
            return None
            
        df = pd.DataFrame(self.expenses)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['weekday'] = df['date'].dt.day_name()
        df['month_name'] = df['date'].dt.strftime('%B')
        df['year'] = df['date'].dt.year
        
        return df

    def show_dashboard(self) -> None:
        """Complete analytics dashboard with statistics and visualizations"""
        self.clear_screen()
        self.print_header("📊 FINANCIAL ANALYTICS DASHBOARD")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to analyze! Add some expenses first.{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Pandas/Matplotlib not available!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Install with: pip install pandas matplotlib{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        df = self.analyze_data()
        if df is None:
            return
        
        # SUMMARY STATISTICS
        print(f"\n{Fore.CYAN}📈 SPENDING SUMMARY{Style.RESET_ALL}")
        print(f"{'─'*55}")
        total_spent = df['amount'].sum()
        avg_transaction = df['amount'].mean()
        max_transaction = df['amount'].max()
        min_transaction = df['amount'].min()
        
        print(f"💰 Total Spent:        {Fore.GREEN}PKR {total_spent:,.2f}{Style.RESET_ALL}")
        print(f"📊 Average Transaction: PKR {avg_transaction:,.2f}")
        print(f"📝 Total Transactions:  {len(df)}")
        print(f"🔥 Highest Expense:     PKR {max_transaction:,.2f}")
        print(f"💚 Lowest Expense:      PKR {min_transaction:,.2f}")
        
        # TOP CATEGORIES
        print(f"\n{Fore.CYAN}🏆 TOP SPENDING CATEGORIES{Style.RESET_ALL}")
        print(f"{'─'*55}")
        category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        for i, (cat, amt) in enumerate(category_totals.head(5).items(), 1):
            percentage = (amt / total_spent * 100) if total_spent > 0 else 0
            bar_len = int((amt / category_totals.max()) * 25)
            bar = "█" * bar_len
            print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {cat:<15} {Fore.CYAN}PKR {amt:>10,.2f}{Style.RESET_ALL} {bar} {percentage:.1f}%")
        
        # MONTHLY TREND
        print(f"\n{Fore.CYAN}📊 MONTHLY SPENDING TREND{Style.RESET_ALL}")
        print(f"{'─'*55}")
        monthly = df.groupby('month')['amount'].sum()
        
        if len(monthly) > 0:
            max_monthly = monthly.max()
            for month, amt in monthly.items():
                month_name = datetime(2024, int(month), 1).strftime('%B')
                bar_len = int((amt / max_monthly) * 25) if max_monthly > 0 else 0
                bar = "█" * bar_len
                print(f"   {month_name:<12} {Fore.CYAN}PKR {amt:>10,.2f}{Style.RESET_ALL} {bar}")
        
        # WEEKLY PATTERN
        print(f"\n{Fore.CYAN}📆 WEEKLY SPENDING PATTERN{Style.RESET_ALL}")
        print(f"{'─'*55}")
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_spend = df.groupby('weekday')['amount'].sum().reindex(weekday_order)
        
        if len(weekday_spend.dropna()) > 0:
            max_weekday = weekday_spend.max()
            for day, amt in weekday_spend.items():
                if not pd.isna(amt):
                    bar_len = int((amt / max_weekday) * 25) if max_weekday > 0 else 0
                    bar = "█" * bar_len
                    print(f"   {day:<12} {Fore.CYAN}PKR {amt:>10,.2f}{Style.RESET_ALL} {bar}")
        
        # VISUALIZATION OPTIONS
        print(f"\n{Fore.CYAN}📊 VISUAL CHARTS{Style.RESET_ALL}")
        print(f"{'─'*55}")
        print(f"   {Fore.GREEN}1.{Style.RESET_ALL} 📈 Monthly Trend (Line Chart)")
        print(f"   {Fore.GREEN}2.{Style.RESET_ALL} 🥧 Category Breakdown (Pie Chart)")
        print(f"   {Fore.GREEN}3.{Style.RESET_ALL} 📊 Daily Spending (Bar Chart)")
        print(f"   {Fore.GREEN}4.{Style.RESET_ALL} 📅 Weekly Pattern (Bar Chart)")
        print(f"   {Fore.GREEN}5.{Style.RESET_ALL} 🔙 Back to Menu")
        
        choice = input(f"\n{Fore.YELLOW}👉 Select chart to view (1-5): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            self.plot_monthly_trend()
        elif choice == '2':
            self.plot_category_pie()
        elif choice == '3':
            self.plot_daily_spending()
        elif choice == '4':
            self.plot_weekly_pattern()
        elif choice == '5':
            return
        else:
            print(f"{Fore.RED}❌ Invalid choice!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")

    def plot_monthly_trend(self) -> None:
        """Plot monthly spending trend as line chart"""
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Matplotlib not available!{Style.RESET_ALL}")
            return
        
        df = self.analyze_data()
        if df is None or len(df) == 0:
            return
        
        monthly = df.groupby('month')['amount'].sum()
        
        if len(monthly) == 0:
            print(f"{Fore.YELLOW}📭 No data to plot!{Style.RESET_ALL}")
            return
        
        plt.figure(figsize=(10, 6))
        plt.plot(monthly.index, monthly.values, marker='o', linewidth=2, color='#2E86AB', markersize=8)
        plt.title('📈 Monthly Spending Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Total Spending (PKR)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(monthly.index, [datetime(2024, int(m), 1).strftime('%B') for m in monthly.index])
        plt.tight_layout()
        plt.show()

    def plot_category_pie(self) -> None:
        """Plot category distribution as pie chart"""
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Matplotlib not available!{Style.RESET_ALL}")
            return
        
        df = self.analyze_data()
        if df is None or len(df) == 0:
            return
        
        category_totals = df.groupby('category')['amount'].sum()
        
        if len(category_totals) == 0:
            print(f"{Fore.YELLOW}📭 No data to plot!{Style.RESET_ALL}")
            return
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FF8C94', '#C3B1E1']
        
        plt.figure(figsize=(8, 8))
        plt.pie(category_totals.values, labels=category_totals.index, 
                autopct='%1.1f%%', startangle=90, colors=colors[:len(category_totals)])
        plt.title('🥧 Spending by Category', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def plot_daily_spending(self) -> None:
        """Plot daily spending for the current month as bar chart"""
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Matplotlib not available!{Style.RESET_ALL}")
            return
        
        df = self.analyze_data()
        if df is None or len(df) == 0:
            return
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_data = df[(df['date'].dt.month == current_month) & (df['date'].dt.year == current_year)]
        
        if len(monthly_data) == 0:
            print(f"{Fore.YELLOW}📭 No data for current month!{Style.RESET_ALL}")
            return
        
        daily = monthly_data.groupby('day')['amount'].sum()
        
        plt.figure(figsize=(12, 5))
        plt.bar(daily.index, daily.values, color='#2E86AB', edgecolor='white')
        plt.title(f'📊 Daily Spending - {datetime.now().strftime("%B %Y")}', fontsize=14, fontweight='bold')
        plt.xlabel('Day of Month', fontsize=12)
        plt.ylabel('Spending (PKR)', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()

    def plot_weekly_pattern(self) -> None:
        """Plot weekly spending pattern as bar chart"""
        if not PANDAS_AVAILABLE:
            print(f"{Fore.RED}❌ Matplotlib not available!{Style.RESET_ALL}")
            return
        
        df = self.analyze_data()
        if df is None or len(df) == 0:
            return
        
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_spend = df.groupby('weekday')['amount'].sum().reindex(weekday_order)
        weekday_spend = weekday_spend.fillna(0)
        
        if weekday_spend.sum() == 0:
            print(f"{Fore.YELLOW}📭 No data to plot!{Style.RESET_ALL}")
            return
        
        colors = ['#FF6B6B' if day in ['Saturday', 'Sunday'] else '#2E86AB' for day in weekday_spend.index]
        
        plt.figure(figsize=(10, 6))
        plt.bar(weekday_spend.index, weekday_spend.values, color=colors, edgecolor='white')
        plt.title('📅 Weekly Spending Pattern', fontsize=14, fontweight='bold')
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Total Spending (PKR)', fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.show()

    # ============================================================
    # PART 13: MAIN APPLICATION LOOP
    # ============================================================
    
    def run(self) -> None:
        """Main application loop"""
        while True:
            self.show_menu()
            
            choice = input(f"{Fore.YELLOW}👉 Enter your choice (1-8): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.view_summary()
            elif choice == '4':
                self.search_expenses()
            elif choice == '5':
                self.delete_expense()
            elif choice == '6':
                self.export_data()
            elif choice == '7':
                self.show_dashboard()
            elif choice == '8':
                self.clear_screen()
                print(f"""
{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════╗
║                                                          ║
║     👋  THANK YOU FOR USING EXPENSE TRACKER PRO!       ║
║                                                          ║
║     📊 Total Spent: PKR {sum(exp['amount'] for exp in self.expenses):.2f}        ║
║     📝 Total Entries: {len(self.expenses)}                               ║
║                                                          ║
║     💡 Tip: Track consistently to build better habits!  ║
║                                                          ║
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
                break
            else:
                print(f"{Fore.RED}❌ Invalid choice! Please enter 1-8.{Style.RESET_ALL}")
                input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")


# ============================================================
# PART 14: DEPENDENCY CHECK AND APPLICATION ENTRY POINT
# ============================================================

def check_dependencies():
    """Check if colorama is installed"""
    try:
        import colorama
        return True
    except ImportError:
        print("⚠️  colorama not installed. Installing...")
        try:
            import subprocess
            subprocess.check_call(['pip', 'install', 'colorama'])
            print("✅ colorama installed successfully!")
            return True
        except:
            print("❌ Could not install colorama. Colors will be disabled.")
            return False


# ============================================================
# PART 15: APPLICATION LAUNCH
# ============================================================

if __name__ == "__main__":
    check_dependencies()
    
    try:
        tracker = ExpenseTracker()
        tracker.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}👋 Goodbye! Thanks for using Expense Tracker Pro!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Please report this issue on GitHub.{Style.RESET_ALL}")