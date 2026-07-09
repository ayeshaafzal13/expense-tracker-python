"""
EXPENSE TRACKER PRO - Complete Financial Management System
===========================================================
A feature-rich expense tracking application with:
- Colorful terminal interface
- Data persistence (JSON storage)
- Category-wise analysis
- Search and filtering
- Export functionality
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# ============================================================
# PART 1: COLOR SETUP FOR TERMINAL DISPLAY
# ============================================================
# Why: Makes the application visually appealing and easier to read
# colorama adds colors to Windows terminals too

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Automatically resets colors after each print
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback classes if colorama isn't installed
    # These provide empty strings so code still works without colors
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
# Why: OOP (Object-Oriented Programming) organizes code logically
# All functionality is encapsulated in one class

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
        self.filename = filename  # Where expenses are stored
        self.expenses = []  # List to hold all expense entries in memory
        self.categories = [
            "Food", "Transport", "Shopping", "Entertainment", 
            "Bills", "Healthcare", "Education", "Other"
        ]  # Predefined categories for organization
        self.load_data()  # Load existing expenses from file
    
    # ============================================================
    # PART 3: DATA PERSISTENCE (Saving/Loading)
    # ============================================================
    # Why: We want expenses to survive even after closing the app
    # JSON is lightweight and human-readable
    
    def load_data(self) -> None:
        """
        Load expenses from JSON file into memory
        If file doesn't exist or is corrupted, start with empty list
        """
        try:
            if os.path.exists(self.filename):
                # Open file in read mode ('r')
                with open(self.filename, 'r') as f:
                    # Convert JSON string back to Python list of dictionaries
                    self.expenses = json.load(f)
            else:
                self.expenses = []  # First time running - no data yet
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle corrupted or missing files gracefully
            self.expenses = []
    
    def save_data(self) -> None:
        """
        Save current expenses from memory to JSON file
        Called after any modification (add, delete, etc.)
        """
        with open(self.filename, 'w') as f:
            # Convert Python objects to JSON string with indentation for readability
            json.dump(self.expenses, f, indent=4)
    
    # ============================================================
    # PART 4: ADD EXPENSE - Most Important Feature
    # ============================================================
    # Why: Users need to enter their spending data
    
    def add_expense(self) -> None:
        """
        Interactive function to add a new expense
        Uses validation loops to ensure correct data entry
        """
        self.clear_screen()
        self.print_header("➕ ADD NEW EXPENSE")
        
        # ---- Step 1: Get Amount ----
        # Why: Amount is the most important piece of data
        # We use a while loop to keep asking until valid input is given
        
        while True:
            try:
                # float() converts string to decimal number (supports decimals)
                amount = float(input("💰 Amount (PKR): "))
                if amount <= 0:
                    print(f"{Fore.RED}❌ Amount must be positive!{Style.RESET_ALL}")
                    continue  # Go back to start of loop
                break  # Exit loop if valid
            except ValueError:
                # User entered text instead of a number
                print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")
        
        # ---- Step 2: Get Category ----
        # Why: Categories help analyze spending patterns later
        
        print(f"\n{Fore.CYAN}📂 Available Categories:{Style.RESET_ALL}")
        # enumerate() gives us both index (starting at 1) and category name
        for i, cat in enumerate(self.categories, 1):
            print(f"   {Fore.YELLOW}{i}.{Style.RESET_ALL} {cat}")
            
        while True:
            try:
                cat_choice = int(input("\n🔢 Select category (1-8): "))
                # Check if choice is within valid range
                if 1 <= cat_choice <= len(self.categories):
                    category = self.categories[cat_choice - 1]  # Convert to 0-based index
                    break
                else:
                    print(f"{Fore.RED}❌ Please enter a number between 1-8!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number!{Style.RESET_ALL}")
        
        # ---- Step 3: Get Description ----
        # Why: Adds context to the expense (what was bought?)
        
        description = input("📝 Description: ").strip()
        if not description:
            description = "No description"  # Default if user presses Enter
        
        # ---- Step 4: Get Date ----
        # Why: For tracking when expenses occurred
        
        date_input = input("📅 Date (DD-MM-YYYY, press Enter for today): ").strip()
        if date_input:
            try:
                # Validate date format using datetime module
                datetime.strptime(date_input, "%d-%m-%Y")
                date = date_input
            except ValueError:
                print(f"{Fore.YELLOW}⚠️ Invalid date format! Using today's date.{Style.RESET_ALL}")
                # Get current date in DD-MM-YYYY format
                date = datetime.now().strftime("%d-%m-%Y")
        else:
            date = datetime.now().strftime("%d-%m-%Y")
        
        # ---- Step 5: Create Expense Dictionary ----
        # Why: Dictionaries are perfect for structured data
        
        expense = {
            "id": len(self.expenses) + 1,  # Auto-increment ID
            "amount": amount,              # Float
            "category": category,          # String
            "description": description,    # String
            "date": date,                  # String
            "timestamp": datetime.now().isoformat()  # Full timestamp for tracking
        }
        
        # ---- Step 6: Save and Confirm ----
        
        self.expenses.append(expense)  # Add to in-memory list
        self.save_data()  # Write to file
        
        # Show success message with details
        print(f"\n{Fore.GREEN}✅ Expense added successfully!{Style.RESET_ALL}")
        print(f"   {Fore.CYAN}💵 Amount:{Style.RESET_ALL} PKR {amount:.2f}")
        print(f"   {Fore.CYAN}📂 Category:{Style.RESET_ALL} {category}")
        print(f"   {Fore.CYAN}📝 Description:{Style.RESET_ALL} {description}")
        print(f"   {Fore.CYAN}📅 Date:{Style.RESET_ALL} {date}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 5: VIEW EXPENSES - Display All Records
    # ============================================================
    # Why: Users need to see their spending history
    
    def view_expenses(self) -> None:
        """
        Display all expenses in a formatted table
        Shows ID, Date, Category, Amount, and Description
        """
        self.clear_screen()
        self.print_header("📊 VIEW ALL EXPENSES")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses recorded yet!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Calculate total for display
        total = sum(exp['amount'] for exp in self.expenses)
        
        # ---- Table Header ----
        # f-string formatting: :<4 means left-align with 4 spaces
        
        print(f"{Fore.CYAN}{'ID':<4} {'Date':<12} {'Category':<15} {'Amount':<12} {'Description':<30}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*75}{Style.RESET_ALL}")
        
        # ---- Table Rows ----
        
        for exp in self.expenses:
            # Color-code amounts based on value (visual prioritization)
            if exp['amount'] > 1000:
                amount_color = Fore.RED  # High expense
            elif exp['amount'] > 500:
                amount_color = Fore.YELLOW  # Medium expense
            else:
                amount_color = Fore.GREEN  # Low expense
                
            print(f"{exp['id']:<4} {exp['date']:<12} {exp['category']:<15} {amount_color}PKR {exp['amount']:<10.2f}{Style.RESET_ALL} {exp['description'][:30]:<30}")
        
        # ---- Summary Footer ----
        print(f"\n{Fore.CYAN}📈 Total Expenses:{Style.RESET_ALL} {Fore.GREEN}PKR {total:.2f}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 Total Entries:{Style.RESET_ALL} {len(self.expenses)}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 6: VIEW SUMMARY - Visual Spending Analysis
    # ============================================================
    # Why: Understand where money is going (category-wise breakdown)
    
    def view_summary(self) -> None:
        """
        Generate a category-wise summary with visual bar charts
        Shows percentage distribution of spending
        """
        self.clear_screen()
        self.print_header("📈 EXPENSE SUMMARY")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to summarize!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # ---- Calculate Category Totals ----
        # Initialize all categories to 0
        category_totals = {}
        for cat in self.categories:
            category_totals[cat] = 0
            
        # Add each expense to its category total
        for exp in self.expenses:
            category_totals[exp['category']] += exp['amount']
        
        # Sort categories by amount (highest first)
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        total = sum(category_totals.values())
        max_amount = max(category_totals.values()) if category_totals else 1
        
        # ---- Display Visual Bars ----
        print(f"\n{Fore.CYAN}📊 Category-wise Breakdown{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}\n")
        
        for cat, amount in sorted_cats:
            if amount == 0:
                continue  # Skip empty categories
                
            # Calculate percentage of total
            percentage = (amount / total * 100) if total > 0 else 0
            
            # Create bar: maximum 30 characters long
            bar_length = int((amount / max_amount) * 30)
            
            # Color based on percentage (red = high spending)
            if percentage > 30:
                color = Fore.RED
            elif percentage > 15:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN
                
            bar = "█" * bar_length  # Unicode block character
            
            print(f"{color}{cat:<15}{Style.RESET_ALL} {Fore.CYAN}PKR {amount:<10.2f}{Style.RESET_ALL} {color}{bar}{Style.RESET_ALL} {percentage:.1f}%")
        
        # ---- Summary Statistics ----
        # Count categories with spending
        active_categories = len([a for a in category_totals.values() if a > 0])
        
        print(f"\n{Fore.GREEN}💰 Total: PKR {total:.2f}{Style.RESET_ALL}")
        if active_categories > 0:
            print(f"{Fore.CYAN}📊 Average per category: PKR {total/active_categories:.2f}{Style.RESET_ALL}")
        
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 7: DELETE EXPENSE - Remove Entries
    # ============================================================
    # Why: Users make mistakes and need to correct them
    
    def delete_expense(self) -> None:
        """
        Delete an expense by its unique ID
        Includes confirmation to prevent accidental deletion
        """
        self.clear_screen()
        self.print_header("🗑️ DELETE EXPENSE")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to delete!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Show recent 10 expenses for reference
        print(f"{Fore.CYAN}Recent Expenses:{Style.RESET_ALL}")
        for exp in self.expenses[-10:]:
            print(f"   {Fore.YELLOW}ID:{exp['id']}{Style.RESET_ALL} - PKR {exp['amount']:.2f} - {exp['description']}")
        
        try:
            exp_id = int(input(f"\n🔢 Enter expense ID to delete: "))
            found = False
            
            # Search for expense by ID
            for i, exp in enumerate(self.expenses):
                if exp['id'] == exp_id:
                    # Confirm deletion
                    confirm = input(f"⚠️ Delete '{exp['description']}' for PKR {exp['amount']:.2f}? (y/n): ")
                    if confirm.lower() == 'y':
                        del self.expenses[i]  # Remove from list
                        self.save_data()  # Save changes
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
    # PART 8: SEARCH EXPENSES - Find Specific Entries
    # ============================================================
    # Why: Users need to find expenses by keyword or category
    
    def search_expenses(self) -> None:
        """
        Search functionality with two modes:
        1. Keyword search (description or category)
        2. Category-based search
        """
        self.clear_screen()
        self.print_header("🔍 SEARCH EXPENSES")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to search!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # ---- Search Options ----
        print(f"\n{Fore.CYAN}Search by:{Style.RESET_ALL}")
        print(f"   {Fore.YELLOW}1.{Style.RESET_ALL} Keyword")
        print(f"   {Fore.YELLOW}2.{Style.RESET_ALL} Category")
        
        choice = input(f"\n🔢 Enter choice (1-2): ").strip()
        
        results = []
        
        # ---- Option 1: Keyword Search ----
        if choice == '1':
            keyword = input("🔍 Enter keyword: ").strip().lower()
            if not keyword:
                print(f"{Fore.RED}❌ Please enter a keyword!{Style.RESET_ALL}")
                input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
                return
                
            # List comprehension: search in description and category
            # .lower() makes search case-insensitive
            results = [exp for exp in self.expenses if 
                      keyword in exp['description'].lower() or 
                      keyword in exp['category'].lower()]
        
        # ---- Option 2: Category Search ----
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
            
        # ---- Display Results ----
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
    # Why: Helper functions that are used throughout the application
    
    def clear_screen(self) -> None:
        """
        Clear terminal screen for cleaner UI
        Works on both Windows (cls) and Unix (clear)
        """
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str) -> None:
        """
        Print a visually styled header with emojis
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}🎯 {title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # ============================================================
    # PART 10: MAIN MENU DISPLAY
    # ============================================================
    # Why: The user's entry point to the application
    
    def show_menu(self) -> None:
        """
        Display the main menu with all available options
        Shows current totals at the top for quick reference
        """
        self.clear_screen()
        print(f"""
{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════╗
║                                                          ║
║     💰  EXPENSE TRACKER PRO  💰                          ║
║                                                          ║
║     Track your spending like a pro!                     ║
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
  {Fore.GREEN}7.{Style.RESET_ALL} 🚀  Exit

{Fore.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
""")
    
    # ============================================================
    # PART 11: EXPORT DATA TO CSV
    # ============================================================
    # Why: Users might want to analyze data in Excel or other tools
    
    def export_data(self) -> None:
        """
        Export all expenses to a CSV file with timestamp
        CSV format is compatible with Excel, Google Sheets, etc.
        """
        self.clear_screen()
        self.print_header("💾 EXPORT DATA")
        
        if not self.expenses:
            print(f"{Fore.YELLOW}📭 No expenses to export!{Style.RESET_ALL}")
            input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        # Create filename with timestamp to avoid overwriting
        csv_filename = f"expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(csv_filename, 'w') as f:
                # Write CSV header
                f.write("ID,Date,Category,Amount,Description\n")
                # Write each expense as a row
                for exp in self.expenses:
                    f.write(f"{exp['id']},{exp['date']},{exp['category']},{exp['amount']},{exp['description']}\n")
            
            print(f"{Fore.GREEN}✅ Data exported to {csv_filename}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}📁 File saved in current directory{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error exporting data: {e}{Style.RESET_ALL}")
            
        input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")
    
    # ============================================================
    # PART 12: MAIN APPLICATION LOOP
    # ============================================================
    # Why: This is the heart of the application - runs forever until exit
    
    def run(self) -> None:
        """
        Main application loop
        Continuously shows menu and processes user choices
        """
        while True:
            self.show_menu()
            
            # Get user choice
            choice = input(f"{Fore.YELLOW}👉 Enter your choice (1-7): {Style.RESET_ALL}").strip()
            
            # Route to appropriate function based on choice
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
                # Exit the application
                self.clear_screen()
                print(f"""
{Fore.GREEN}{Style.BRIGHT}╔══════════════════════════════════════════════════════╗
║                                                                              
║     👋  THANK YOU FOR USING EXPENSE TRACKER PRO!                             
║                                                                              
║     📊 Total Spent: PKR {sum(exp['amount'] for exp in self.expenses):.2f}     
║     📝 Total Entries: {len(self.expenses)}                                   
║                                                                               
║     💡 Tip: Track consistently to build better habits!                        
║                                                                              
╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
                break  # Exit the while loop
            else:
                print(f"{Fore.RED}❌ Invalid choice! Please enter 1-7.{Style.RESET_ALL}")
                input(f"\n{Fore.MAGENTA}Press Enter to continue...{Style.RESET_ALL}")


# ============================================================
# PART 13: DEPENDENCY CHECK AND APPLICATION ENTRY POINT
# ============================================================
# Why: Makes sure required packages are installed before running

def check_dependencies():
    """
    Check if colorama is installed
    If not, attempt to install it automatically
    """
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
# PART 14: APPLICATION LAUNCH
# ============================================================
# Why: This is where the program starts executing

if __name__ == "__main__":
    """
    This runs only when you execute this file directly
    (Not when imported as a module)
    """
    # Check dependencies
    check_dependencies()
    
    # Run the application with error handling
    try:
        # Create an instance of ExpenseTracker
        tracker = ExpenseTracker()
        # Start the main loop
        tracker.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print(f"\n\n{Fore.YELLOW}👋 Goodbye! Thanks for using Expense Tracker Pro!{Style.RESET_ALL}")
    except Exception as e:
        # Handle any unexpected errors
        print(f"{Fore.RED}❌ An error occurred: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Please report this issue on GitHub.{Style.RESET_ALL}")