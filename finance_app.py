from datetime import datetime
class Transaction:
  def __init__(self,name,category,amount,t_type):
     self.name=name
     self.category=category
     self.amount=amount
     self.t_type=t_type
     self.date=datetime.now().strftime("%d-%m-%Y")
  def __str__(self):
    return f"[{self.t_type.upper()}] {self.name} | {self.category} | ₹{self.amount} | {self.date}"

    
class TransactionFactory:
  def  create(self,t_type,name,category,amount):
    if t_type == "income":
      return Transaction(name, category, amount, "income")
    elif t_type == "expense":
      return Transaction(name, category, amount, "expense")
    else:
      print("❌ Unknown transaction type!")
      return None
      # linkedlist
class TransactionNode:
  def __init__(self, transaction):
      self.transaction = transaction    
    # stores Transaction object!
      self.next = None
  

class TransactionHistory:
  def __init__(self):
      self.head = None
      self.size = 0

  def add(self,transaction):
    new_node=TransactionNode(transaction)
    if self.head is None:
      self.head=new_node
      self.size+=1
      return
    current=self.head
    while current.next is not None:
      current=current.next
    current.next=new_node
    self.size+=1
      
  def show(self):
    if self.head is None:
      print("No transactions yet")
      return
    print("Transaction History")
    current=self.head
    count=1
    while current is not None:
      print(f"{count}.{current.transaction}")
   
      current=current.next
      count+=1
      
  def __len__(self): 
    return self.size

  def delete_last(self):
    if self.head is None:
        return
    if self.head.next is None:
        self.head = None
        self.size -= 1
        return
    current = self.head
    while current.next.next is not None:
        current = current.next
    current.next = None
    self.size -= 1
# stack
class UndoStack:
  def __init__(self):
    self.__stack=[]
  def save(self,transaction):
    self.__stack.append(transaction)

  def undo(self):
    if self.is_empty():
      print("Nothing to undo")
      return None
    transaction=self.__stack.pop()
    print(f"Undoing:{transaction}")
    return transaction
    
  def __len__(self):
    return len(self.__stack)
  def is_empty(self):
    return len(self.__stack)==0
    
# hashmap
class CategoryMap:
  def __init__(self):
    self.__categories={}

  def add(self,category,amount):
    if category not in self.__categories:
      self.__categories[category]=[]
    self.__categories[category].append(amount)
    print(f"{amount} added to {category}")

  def get_total(self,category):
    if category not in self.__categories:
      print("No expenses yet")
      return 0
    return sum(self.__categories[category])
    
  def highest_spending(self):
    max_category=None
    max_amount=0
    for category, amount in self.__categories.items():
      total=sum(amount)
      if total>max_amount:
        max_amount=total
        max_category=category
    print(f"🏆 Highest: {max_category} (₹{max_amount})")

  def show_all(self):
    print("Expenses:")
    for category, amount in self.__categories.items():
        total = sum(amount)                    
        print(f"   {category} → ₹{total}") 


from abc import ABC, abstractmethod
class BudgetObserver(ABC):
  @abstractmethod
  def update(self,category,spent,limit):
    pass

class EmailAlert(BudgetObserver):
  def __init__(self,email):
    self.email=email
    
  def update(self,category,spent,limit):
    print(f"Email sent to {self.email}:")
    print(f"{category} budget crossed!")
    print(f"Spent ₹{spent} of ₹{limit}")

class SMSAlert(BudgetObserver):
  def __init__(self,phone):
    self.phone=phone

  def update(self,category,spent,limit):
    print(f"SMS Alert to {self.phone} ")
    print(f"{category} budget crossed!")
    print(f"Spent ₹{spent} of ₹{limit}")

class AppAlert(BudgetObserver):
  def update(self,category,spent,limit):
     print(f"App Alert: {category} budget crossed!")
     print(f"Spent ₹{spent} of ₹{limit}")

class FinanceApp:
  _instance = None

  def __new__(cls):
      if cls._instance is None:
          cls._instance = super().__new__(cls)
          cls._instance.history      = TransactionHistory()
          cls._instance.undo_stack   = UndoStack()
          cls._instance.category_map = CategoryMap()
          cls._instance.observers    = []
          cls._instance.budgets      = {}
          cls._instance.balance      = 0
      return cls._instance

  # ===== OBSERVER METHODS =====
  def add_observer(self, observer):
      self.observers.append(observer)
      print(f"✅ {observer.__class__.__name__} subscribed!")

  def __notify(self, category, spent, limit):
      for observer in self.observers:
          observer.update(category, spent, limit)

  # ===== BUDGET METHODS =====
  def set_budget(self, category, limit):
      self.budgets[category] = limit
      print(f"✅ Budget set: {category} → ₹{limit}")

  def __check_budget(self, category, amount):
      if category in self.budgets:
          spent = self.category_map.get_total(category)
          limit = self.budgets[category]
          if spent > limit:
              print(f"🚨 {category} budget crossed!")
              self.__notify(category, spent, limit)

  # ===== TRANSACTION METHODS =====
  def add_income(self, name, category, amount):
      t = TransactionFactory().create("income", name, category, amount)
      self.history.add(t)
      self.undo_stack.save(t)
      self.balance += amount
      print(f"✅ Income: ₹{amount} from {name}")

  def add_expense(self, name, category, amount):
      t = TransactionFactory().create("expense", name, category, amount)
      self.history.add(t)
      self.undo_stack.save(t)
      self.category_map.add(category, amount)
      self.balance -= amount
      print(f"💸 Expense: ₹{amount} on {name}")
      self.__check_budget(category, amount)   # check after adding!

  def undo_last(self):
      t = self.undo_stack.undo()
      if t is None:
          return
      if t.t_type == "income":
          self.balance -= t.amount
      else:
          self.balance += t.amount
      self.history.delete_last()
      print(f"✅ Undo done! Balance: ₹{self.balance}")

  # ===== DISPLAY METHODS =====
  def show_balance(self):
      print(f"\n💰 Balance: ₹{self.balance}")
      print(f"📝 Transactions: {len(self.history)}")
      print(f"↩️  Undoable: {len(self.undo_stack)}")

  def show_history(self):
      self.history.show()

  def show_categories(self):
      self.category_map.show_all()
      self.category_map.highest_spending()


# ===== STEP 10 — RUN THE APP! =====
app = FinanceApp()

# Set up alerts
app.add_observer(AppAlert())
app.add_observer(SMSAlert("9876543210"))

# Set budgets
app.set_budget("Food", 2000)
app.set_budget("Transport", 1000)

# Add transactions
app.add_income("Salary", "Job", 50000)
app.add_expense("Lunch", "Food", 1200)
app.add_expense("Dinner", "Food", 500)
app.add_expense("Dinner", "Food", 400)   # 🚨 crosses ₹2000!
app.add_expense("Bus", "Transport", 300)

# Show everything
app.show_balance()
app.show_history()
app.show_categories()

# Undo last transaction
print("\n--- UNDO ---")
app.undo_last()
app.show_balance()

# Singleton check!
app2 = FinanceApp()
print(f"\nSame app? {app is app2}")   # True!

