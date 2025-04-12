
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------- Data File Setup ----------
FILES = {
    "members": "members.json",
    "classes": "classes.json",
    "equipment": "equipment.json"
}

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Main Application ----------
class GymMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GymMaster - Gym Management System")
        self.root.geometry("700x500")

        self.tabControl = ttk.Notebook(root)
        self.member_tab = ttk.Frame(self.tabControl)
        self.class_tab = ttk.Frame(self.tabControl)
        self.equipment_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.member_tab, text='Members')
        self.tabControl.add(self.class_tab, text='Classes')
        self.tabControl.add(self.equipment_tab, text='Equipment')
        self.tabControl.pack(expand=1, fill="both")

        self.init_member_tab()
        self.init_class_tab()
        self.init_equipment_tab()

    # ---------- Member Tab ----------
    def init_member_tab(self):
        self.member_data = load_data(FILES["members"])

        tk.Label(self.member_tab, text="Name").grid(row=0, column=0)
        tk.Label(self.member_tab, text="Age").grid(row=0, column=1)

        self.member_name = tk.Entry(self.member_tab)
        self.member_age = tk.Entry(self.member_tab)
        self.member_name.grid(row=1, column=0)
        self.member_age.grid(row=1, column=1)

        tk.Button(self.member_tab, text="Add Member", command=self.add_member).grid(row=1, column=2)
        tk.Button(self.member_tab, text="Remove Selected", command=self.remove_member).grid(row=2, column=2)

        self.member_list = tk.Listbox(self.member_tab, width=80)
        self.member_list.grid(row=3, column=0, columnspan=3)
        self.update_member_list()

    def add_member(self):
        name = self.member_name.get()
        age = self.member_age.get()
        if name and age:
            self.member_data.append({"name": name, "age": age})
            save_data(FILES["members"], self.member_data)
            self.update_member_list()
        else:
            messagebox.showwarning("Input Error", "Please provide both name and age.")

    def remove_member(self):
        selection = self.member_list.curselection()
        if selection:
            del self.member_data[selection[0]]
            save_data(FILES["members"], self.member_data)
            self.update_member_list()

    def update_member_list(self):
        self.member_list.delete(0, tk.END)
        for member in self.member_data:
            self.member_list.insert(tk.END, f"{member['name']} - Age: {member['age']}")

    # ---------- Class Tab ----------
    def init_class_tab(self):
        self.class_data = load_data(FILES["classes"])

        tk.Label(self.class_tab, text="Class Name").grid(row=0, column=0)
        tk.Label(self.class_tab, text="Schedule").grid(row=0, column=1)

        self.class_name = tk.Entry(self.class_tab)
        self.class_schedule = tk.Entry(self.class_tab)
        self.class_name.grid(row=1, column=0)
        self.class_schedule.grid(row=1, column=1)

        tk.Button(self.class_tab, text="Add Class", command=self.add_class).grid(row=1, column=2)
        tk.Button(self.class_tab, text="Remove Selected", command=self.remove_class).grid(row=2, column=2)

        self.class_list = tk.Listbox(self.class_tab, width=80)
        self.class_list.grid(row=3, column=0, columnspan=3)
        self.update_class_list()

    def add_class(self):
        name = self.class_name.get()
        schedule = self.class_schedule.get()
        if name and schedule:
            self.class_data.append({"name": name, "schedule": schedule})
            save_data(FILES["classes"], self.class_data)
            self.update_class_list()
        else:
            messagebox.showwarning("Input Error", "Please provide both class name and schedule.")

    def remove_class(self):
        selection = self.class_list.curselection()
        if selection:
            del self.class_data[selection[0]]
            save_data(FILES["classes"], self.class_data)
            self.update_class_list()

    def update_class_list(self):
        self.class_list.delete(0, tk.END)
        for cls in self.class_data:
            self.class_list.insert(tk.END, f"{cls['name']} - Schedule: {cls['schedule']}")

    # ---------- Equipment Tab ----------
    def init_equipment_tab(self):
        self.equipment_data = load_data(FILES["equipment"])

        tk.Label(self.equipment_tab, text="Equipment").grid(row=0, column=0)
        tk.Label(self.equipment_tab, text="Maintenance Date").grid(row=0, column=1)

        self.equipment_name = tk.Entry(self.equipment_tab)
        self.equipment_date = tk.Entry(self.equipment_tab)
        self.equipment_name.grid(row=1, column=0)
        self.equipment_date.grid(row=1, column=1)

        tk.Button(self.equipment_tab, text="Add Equipment", command=self.add_equipment).grid(row=1, column=2)
        tk.Button(self.equipment_tab, text="Remove Selected", command=self.remove_equipment).grid(row=2, column=2)

        self.equipment_list = tk.Listbox(self.equipment_tab, width=80)
        self.equipment_list.grid(row=3, column=0, columnspan=3)
        self.update_equipment_list()

    def add_equipment(self):
        name = self.equipment_name.get()
        date = self.equipment_date.get()
        if name and date:
            self.equipment_data.append({"name": name, "maintenance": date})
            save_data(FILES["equipment"], self.equipment_data)
            self.update_equipment_list()
        else:
            messagebox.showwarning("Input Error", "Please provide both equipment name and maintenance date.")

    def remove_equipment(self):
        selection = self.equipment_list.curselection()
        if selection:
            del self.equipment_data[selection[0]]
            save_data(FILES["equipment"], self.equipment_data)
            self.update_equipment_list()

    def update_equipment_list(self):
        self.equipment_list.delete(0, tk.END)
        for item in self.equipment_data:
            self.equipment_list.insert(tk.END, f"{item['name']} - Maintenance: {item['maintenance']}")



# ---------- Launch ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = GymMasterApp(root)
    root.mainloop()
