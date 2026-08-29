"""
Food Expense Tracker (GUI - Tkinter) 

Based on my console:
- Added **Date** field (defaults to today) and saves it to JSON
- Added **Edit Selected** (update an existing expense)
- Added **Search** box + **Category filter** (shows matching rows)
- Added **Sort by clicking column headers**
- Added **Export CSV** button
- Data file is stored next to this script (no surprises about where expenses.json is)
- Stronger validation and safer loading (handles older JSON without "date")

Categories: Breakfast, Lunch, Dinner, Snack
"""

import csv
import json
import os
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk, messagebox

VALID_CATEGORIES = ["Breakfast", "Lunch", "Dinner", "Snack"]


def _script_dir() -> str:
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except Exception:
        return os.getcwd()


DATA_FILE = os.path.join(_script_dir(), "expenses.json")


def _today_str() -> str:
    return date.today().strftime("%Y-%m-%d")


def _parse_date(raw: str) -> str:
    raw = (raw or "").strip()
    if raw == "":
        raise ValueError("Date is required (format: YYYY-MM-DD).")
    try:
        # Accept YYYY-MM-DD
        dt = datetime.strptime(raw, "%Y-%m-%d").date()
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format (example: 2026-01-14).")


def load_expenses(filename: str = DATA_FILE):
    """Loads expenses from JSON; returns list[dict]. Safely handles old/invalid data."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []

        cleaned = []
        for item in data:
            if not isinstance(item, dict):
                continue
            desc = str(item.get("description", "")).strip() or "Unknown"
            cat = str(item.get("category", "Uncategorized")).strip() or "Uncategorized"
            raw_amt = item.get("amount", 0)
            try:
                amt = float(raw_amt)
            except Exception:
                amt = 0.0

            # Backward compatible: older files might not have "date"
            raw_dt = str(item.get("date", "")).strip()
            if raw_dt == "":
                raw_dt = _today_str()
            try:
                dt_str = _parse_date(raw_dt)
            except ValueError:
                dt_str = _today_str()

            cleaned.append({"date": dt_str, "description": desc, "amount": amt, "category": cat})
        return cleaned
    except (OSError, json.JSONDecodeError):
        return []


def save_expenses(expenses, filename: str = DATA_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)
    except OSError:
        messagebox.showwarning("Save Warning", "Could not save expenses to file.")


class ExpenseTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Expense Tracker (GUI)")
        self.geometry("920x560")
        self.minsize(920, 560)

        self.expenses = load_expenses()
        self.filtered_indexes = list(range(len(self.expenses)))  # indexes into self.expenses
        self.sort_state = {"col": None, "descending": False}

        self._build_ui()
        self._apply_filters(refresh_status=False)

        if self.expenses:
            self.status_var.set(f"Loaded {len(self.expenses)} expense(s) from {os.path.basename(DATA_FILE)}.")
        else:
            self.status_var.set("No saved expenses found. Starting fresh.")

    # ---------- UI ----------
    def _build_ui(self):
        # Inputs
        frm_inputs = ttk.LabelFrame(self, text="Add / Edit Expense")
        frm_inputs.pack(fill="x", padx=12, pady=10)

        # Row 0
        ttk.Label(frm_inputs, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.date_var = tk.StringVar(value=_today_str())
        ttk.Entry(frm_inputs, textvariable=self.date_var, width=14).grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(frm_inputs, text="Merchant/Description:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.desc_var = tk.StringVar()
        ttk.Entry(frm_inputs, textvariable=self.desc_var, width=35).grid(row=0, column=3, padx=8, pady=8, sticky="w")

        ttk.Label(frm_inputs, text="Amount ($):").grid(row=0, column=4, padx=8, pady=8, sticky="w")
        self.amount_var = tk.StringVar()
        ttk.Entry(frm_inputs, textvariable=self.amount_var, width=12).grid(row=0, column=5, padx=8, pady=8, sticky="w")

        ttk.Label(frm_inputs, text="Category:").grid(row=0, column=6, padx=8, pady=8, sticky="w")
        self.cat_var = tk.StringVar(value=VALID_CATEGORIES[0])
        self.cat_combo = ttk.Combobox(
            frm_inputs, textvariable=self.cat_var, values=VALID_CATEGORIES, state="readonly", width=12
        )
        self.cat_combo.grid(row=0, column=7, padx=8, pady=8, sticky="w")

        ttk.Button(frm_inputs, text="Add Expense", command=self.add_expense).grid(row=0, column=8, padx=8, pady=8)
        ttk.Button(frm_inputs, text="Edit Selected", command=self.edit_selected).grid(row=0, column=9, padx=8, pady=8)

        # Row 1 (filters)
        frm_filters = ttk.Frame(frm_inputs)
        frm_filters.grid(row=1, column=0, columnspan=10, sticky="ew", padx=8, pady=(0, 8))
        frm_inputs.columnconfigure(3, weight=1)

        ttk.Label(frm_filters, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        ent_search = ttk.Entry(frm_filters, textvariable=self.search_var, width=28)
        ent_search.pack(side="left", padx=(6, 12))
        ent_search.bind("<KeyRelease>", lambda _e: self._apply_filters())

        ttk.Label(frm_filters, text="Filter Category:").pack(side="left")
        self.filter_cat_var = tk.StringVar(value="All")
        self.filter_cat_combo = ttk.Combobox(
            frm_filters, textvariable=self.filter_cat_var, values=["All"] + VALID_CATEGORIES, state="readonly", width=12
        )
        self.filter_cat_combo.pack(side="left", padx=6)
        self.filter_cat_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        ttk.Button(frm_filters, text="Clear Filters", command=self._clear_filters).pack(side="left", padx=12)

        # Table
        frm_table = ttk.LabelFrame(self, text="Expenses (click column header to sort)")
        frm_table.pack(fill="both", expand=True, padx=12, pady=10)

        columns = ("#", "date", "description", "category", "amount")
        self.tree = ttk.Treeview(frm_table, columns=columns, show="headings", height=14)

        headings = {
            "#": "#",
            "date": "Date",
            "description": "Merchant/Description",
            "category": "Category",
            "amount": "Amount ($)",
        }
        for col in columns:
            self.tree.heading(col, text=headings[col], command=lambda c=col: self._sort_by(c))

        self.tree.column("#", width=50, anchor="center")
        self.tree.column("date", width=110, anchor="center")
        self.tree.column("description", width=420, anchor="w")
        self.tree.column("category", width=130, anchor="center")
        self.tree.column("amount", width=130, anchor="e")

        vsb = ttk.Scrollbar(frm_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        vsb.pack(side="right", fill="y", padx=(0, 8), pady=8)

        # Actions
        frm_actions = ttk.Frame(self)
        frm_actions.pack(fill="x", padx=12, pady=(0, 10))

        ttk.Button(frm_actions, text="Delete Selected", command=self.delete_selected).pack(side="left")
        ttk.Button(frm_actions, text="Export CSV", command=self.export_csv).pack(side="left", padx=(8, 0))

        ttk.Separator(frm_actions, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Label(frm_actions, text="Category Total:").pack(side="left")
        self.cat_total_var = tk.StringVar(value=VALID_CATEGORIES[0])
        self.cat_total_combo = ttk.Combobox(
            frm_actions, textvariable=self.cat_total_var, values=VALID_CATEGORIES, state="readonly", width=12
        )
        self.cat_total_combo.pack(side="left", padx=8)

        ttk.Button(frm_actions, text="Show", command=self.show_category_total).pack(side="left")

        ttk.Separator(frm_actions, orient="vertical").pack(side="left", fill="y", padx=10)

        ttk.Button(frm_actions, text="Save Now", command=self.save_now).pack(side="left")
        ttk.Button(frm_actions, text="Quit", command=self.destroy).pack(side="right")

        # Bottom: totals + status
        frm_bottom = ttk.Frame(self)
        frm_bottom.pack(fill="x", padx=12, pady=(0, 10))

        self.total_label_var = tk.StringVar(value="Total food spending: $0.00")
        ttk.Label(frm_bottom, textvariable=self.total_label_var, font=("Segoe UI", 10, "bold")).pack(side="left")

        self.status_var = tk.StringVar(value="")
        ttk.Label(frm_bottom, textvariable=self.status_var).pack(side="right")

        # Double-click a row to load it into inputs for editing
        self.tree.bind("<Double-1>", lambda _e: self._load_selected_into_inputs())

        # Keyboard shortcuts
        self.bind("<Return>", lambda _e: self.add_expense())
        self.bind("<Delete>", lambda _e: self.delete_selected())

    # ---------- Helpers ----------
    def _validate_amount(self, raw: str) -> float:
        raw = (raw or "").strip()
        if raw == "":
            raise ValueError("Amount is required.")
        try:
            amt = float(raw)
        except ValueError:
            raise ValueError("Amount must be a number (example: 12.50).")
        if amt < 0:
            raise ValueError("Amount must be 0 or greater.")
        return amt

    def _validate_category(self, cat: str) -> str:
        cat = (cat or "").strip()
        if cat not in VALID_CATEGORIES:
            raise ValueError("Please choose a valid category.")
        return cat

    def _selected_expense_index(self):
        """Return (expense_index_in_list, display_row_number) or (None, None)."""
        selected = self.tree.selection()
        if not selected:
            return None, None
        values = self.tree.item(selected[0], "values")
        if not values:
            return None, None
        # "#" is display row number within filtered view (1-based)
        try:
            display_row = int(values[0])
        except Exception:
            return None, None
        if display_row < 1 or display_row > len(self.filtered_indexes):
            return None, None
        return self.filtered_indexes[display_row - 1], display_row

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, idx in enumerate(self.filtered_indexes, start=1):
            exp = self.expenses[idx]
            dt_str = exp.get("date", _today_str())
            desc = exp.get("description", "Unknown")
            cat = exp.get("category", "Uncategorized")
            amt = float(exp.get("amount", 0))
            self.tree.insert("", "end", values=(i, dt_str, desc, cat, f"{amt:.2f}"))

    def _update_totals(self):
        total = sum(float(e.get("amount", 0)) for e in self.expenses)
        self.total_label_var.set(f"Total food spending: ${total:.2f}")

    def _clear_inputs(self):
        self.date_var.set(_today_str())
        self.desc_var.set("")
        self.amount_var.set("")
        self.cat_var.set(VALID_CATEGORIES[0])

    def _clear_filters(self):
        self.search_var.set("")
        self.filter_cat_var.set("All")
        self._apply_filters()

    def _apply_filters(self, refresh_status: bool = True):
        """Recompute filtered_indexes based on current Search + Category filter."""
        q = (self.search_var.get() or "").strip().lower()
        cat_filter = (self.filter_cat_var.get() or "All").strip()

        def match(exp):
            if cat_filter != "All" and str(exp.get("category", "")).strip() != cat_filter:
                return False
            if q == "":
                return True
            hay = f"{exp.get('date','')} {exp.get('description','')} {exp.get('category','')} {exp.get('amount','')}".lower()
            return q in hay

        self.filtered_indexes = [i for i, e in enumerate(self.expenses) if match(e)]

        # Keep current sort applied
        if self.sort_state["col"] is not None:
            self._sort_filtered_in_place(self.sort_state["col"], self.sort_state["descending"])

        self._refresh_table()
        if refresh_status:
            self.status_var.set(f"Showing {len(self.filtered_indexes)} of {len(self.expenses)} expense(s).")
        self._update_totals()

    # ---------- Sorting ----------
    def _sort_key(self, exp, col):
        if col == "#":
            return 0
        if col == "date":
            try:
                return datetime.strptime(exp.get("date", _today_str()), "%Y-%m-%d")
            except Exception:
                return datetime.min
        if col == "amount":
            try:
                return float(exp.get("amount", 0))
            except Exception:
                return 0.0
        return str(exp.get(col, "")).lower()

    def _sort_filtered_in_place(self, col: str, descending: bool):
        self.filtered_indexes.sort(
            key=lambda idx: self._sort_key(self.expenses[idx], col),
            reverse=descending,
        )

    def _sort_by(self, col: str):
        if col == "#":
            return

        if self.sort_state["col"] == col:
            self.sort_state["descending"] = not self.sort_state["descending"]
        else:
            self.sort_state["col"] = col
            self.sort_state["descending"] = False

        self._sort_filtered_in_place(col, self.sort_state["descending"])
        self._refresh_table()

        arrow = "↓" if self.sort_state["descending"] else "↑"
        self.status_var.set(f"Sorted by {col} {arrow}")

    # ---------- Actions ----------
    def add_expense(self):
        try:
            dt_str = _parse_date(self.date_var.get())
            desc = (self.desc_var.get() or "").strip() or "Unknown"
            cat = self._validate_category(self.cat_var.get())
            amt = self._validate_amount(self.amount_var.get())
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.expenses.append({"date": dt_str, "description": desc, "amount": amt, "category": cat})
        save_expenses(self.expenses)
        self._clear_inputs()
        self._apply_filters()
        self.status_var.set("✅ Expense added and saved.")

    def _load_selected_into_inputs(self):
        idx, _display_row = self._selected_expense_index()
        if idx is None:
            return
        exp = self.expenses[idx]
        self.date_var.set(exp.get("date", _today_str()))
        self.desc_var.set(exp.get("description", ""))
        self.amount_var.set(str(exp.get("amount", "")))
        cat = exp.get("category", VALID_CATEGORIES[0])
        self.cat_var.set(cat if cat in VALID_CATEGORIES else VALID_CATEGORIES[0])
        self.status_var.set("Loaded selected row into inputs. Edit fields, then click 'Edit Selected'.")

    def edit_selected(self):
        idx, display_row = self._selected_expense_index()
        if idx is None:
            messagebox.showinfo("Edit", "Select an expense row to edit (or double-click it).")
            return

        try:
            dt_str = _parse_date(self.date_var.get())
            desc = (self.desc_var.get() or "").strip() or "Unknown"
            cat = self._validate_category(self.cat_var.get())
            amt = self._validate_amount(self.amount_var.get())
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        old = self.expenses[idx].copy()
        self.expenses[idx] = {"date": dt_str, "description": desc, "amount": amt, "category": cat}
        save_expenses(self.expenses)
        self._apply_filters()
        self.status_var.set(f"✏️ Updated row {display_row}: {old.get('description','Unknown')} → {desc}")

    def delete_selected(self):
        idx, display_row = self._selected_expense_index()
        if idx is None:
            messagebox.showinfo("Delete", "Select an expense row to delete.")
            return

        exp = self.expenses[idx]
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete this expense?\n\n{exp.get('date','')} — {exp.get('description','Unknown')} "
            f"- ${float(exp.get('amount',0)):.2f} ({exp.get('category','')})"
        ):
            return

        removed = self.expenses.pop(idx)
        save_expenses(self.expenses)
        self._clear_inputs()
        self._apply_filters()
        self.status_var.set(f"🗑️ Deleted: {removed.get('description','Unknown')}")

    def show_category_total(self):
        cat = (self.cat_total_var.get() or "").strip()
        total_cat = sum(float(e.get("amount", 0)) for e in self.expenses if str(e.get("category", "")).strip() == cat)
        messagebox.showinfo("Category Total", f"Total spent on {cat}: ${total_cat:.2f}")

    def export_csv(self):
        """Exports the *currently filtered rows* to a CSV file next to the script."""
        if not self.filtered_indexes:
            messagebox.showinfo("Export CSV", "No rows to export (your filter returned 0 results).")
            return

        out_name = f"expenses_export_{date.today().strftime('%Y%m%d')}.csv"
        out_path = os.path.join(_script_dir(), out_name)
        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["date", "description", "category", "amount"])
                for idx in self.filtered_indexes:
                    e = self.expenses[idx]
                    w.writerow([e.get("date",""), e.get("description",""), e.get("category",""), f"{float(e.get('amount',0)):.2f}"])
            self.status_var.set(f"📄 Exported {len(self.filtered_indexes)} row(s) to {out_name}")
            messagebox.showinfo("Export CSV", f"Exported to:\n{out_path}")
        except OSError:
            messagebox.showerror("Export CSV", "Could not write the CSV file. Try running from a writable folder.")

    def save_now(self):
        save_expenses(self.expenses)
        self.status_var.set(f"💾 Saved to {os.path.basename(DATA_FILE)}")


if __name__ == "__main__":
    # Tk themed widgets + DPI scaling on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = ExpenseTrackerGUI()
    app.mainloop()

