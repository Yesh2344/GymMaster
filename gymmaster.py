import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class GymMaster:
    def __init__(self, master):
        self.master = master
        master.title("GymMaster")
        master.geometry("1000x600")

        self.sidebar = ctk.CTkFrame(master, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=20, pady=20)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="GymMaster", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=20)

        self.sidebar_button_1 = ctk.CTkButton(self.sidebar, text="Members", command=self.show_members)
        self.sidebar_button_1.pack(padx=20, pady=10)

        self.sidebar_button_2 = ctk.CTkButton(self.sidebar, text="Classes", command=self.show_classes)
        self.sidebar_button_2.pack(padx=20, pady=10)

        self.sidebar_button_3 = ctk.CTkButton(self.sidebar, text="Equipment", command=self.show_equipment)
        self.sidebar_button_3.pack(padx=20, pady=10)

        self.sidebar_button_4 = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.sidebar_button_4.pack(padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.pack(padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.pack(padx=20, pady=(10, 10))

        self.main_frame = ctk.CTkFrame(master)
        self.main_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        self.members = self.load_data('members.json')
        self.classes = self.load_data('classes.json')
        self.equipment = self.load_data('equipment.json')

        self.show_dashboard()

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Dashboard", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=20, pady=20)

        # Member statistics
        member_count = len(self.members)
        active_members = sum(1 for member in self.members if member.get('status', 'active') == 'active')

        member_stats = ctk.CTkFrame(self.main_frame)
        member_stats.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(member_stats, text=f"Total Members: {member_count}").pack(side="left", padx=10)
        ctk.CTkLabel(member_stats, text=f"Active Members: {active_members}").pack(side="left", padx=10)

        # Class popularity chart
        class_names = [c['name'] for c in self.classes]
        class_attendance = [c.get('attendance', 0) for c in self.classes]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(class_names, class_attendance)
        ax.set_title("Class Popularity")
        ax.set_xlabel("Classes")
        ax.set_ylabel("Attendance")
        plt.xticks(rotation=45, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        # Equipment maintenance reminder
        equipment_to_maintain = [e for e in self.equipment if self.days_since_maintenance(e) > 30]
        if equipment_to_maintain:
            maintenance_frame = ctk.CTkFrame(self.main_frame)
            maintenance_frame.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(maintenance_frame, text="Equipment Needing Maintenance:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            for equip in equipment_to_maintain:
                ctk.CTkLabel(maintenance_frame, text=f"- {equip['name']} (Last maintained: {equip['last_maintenance']})").pack(anchor="w")

    def days_since_maintenance(self, equipment):
        last_maintenance = datetime.strptime(equipment['last_maintenance'], "%Y-%m-%d")
        days_since = (datetime.now() - last_maintenance).days
        return days_since

    def show_members(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Members", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=20, pady=20)

        # Table
        columns = ('ID', 'Name', 'Email', 'Join Date', 'Status')
        self.members_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=100)
        self.members_tree.pack(expand=True, fill="both", padx=20, pady=10)
        self.update_members_list()

        # Input Frame
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(input_frame, text="Name:").pack(side="left")
        self.member_name_entry = ctk.CTkEntry(input_frame)
        self.member_name_entry.pack(side="left", padx=5)

        ctk.CTkLabel(input_frame, text="Email:").pack(side="left")
        self.member_email_entry = ctk.CTkEntry(input_frame)
        self.member_email_entry.pack(side="left", padx=5)

        ctk.CTkButton(input_frame, text="Add Member", command=self.add_member).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Remove Member", command=self.remove_member).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Toggle Status", command=self.toggle_member_status).pack(side="left", padx=5)

    def update_members_list(self):
        self.members_tree.delete(*self.members_tree.get_children())
        for member in self.members:
            self.members_tree.insert('', 'end', values=(member['id'], member['name'], member['email'], member['join_date'], member.get('status', 'active')))

    def add_member(self):
        name = self.member_name_entry.get()
        email = self.member_email_entry.get()
        if name and email:
            new_id = max([m['id'] for m in self.members], default=0) + 1
            self.members.append({
                "id": new_id,
                "name": name,
                "email": email,
                "join_date": datetime.now().strftime("%Y-%m-%d"),
                "status": "active"
            })
            self.save_data(self.members, 'members.json')
            self.update_members_list()
            self.member_name_entry.delete(0, 'end')
            self.member_email_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please enter both name and email.")

    def remove_member(self):
        selected_item = self.members_tree.selection()
        if selected_item:
            member_id = self.members_tree.item(selected_item)['values'][0]
            self.members = [m for m in self.members if m['id'] != member_id]
            self.save_data(self.members, 'members.json')
            self.update_members_list()
        else:
            messagebox.showerror("Error", "Please select a member to remove.")

    def toggle_member_status(self):
        selected_item = self.members_tree.selection()
        if selected_item:
            member_id = self.members_tree.item(selected_item)['values'][0]
            for member in self.members:
                if member['id'] == member_id:
                    member['status'] = 'inactive' if member.get('status', 'active') == 'active' else 'active'
                    break
            self.save_data(self.members, 'members.json')
            self.update_members_list()
        else:
            messagebox.showerror("Error", "Please select a member to toggle status.")

    def show_classes(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Classes", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=20, pady=20)

        # Table
        columns = ('ID', 'Name', 'Instructor', 'Schedule', 'Attendance')
        self.classes_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        for col in columns:
            self.classes_tree.heading(col, text=col)
            self.classes_tree.column(col, width=100)
        self.classes_tree.pack(expand=True, fill="both", padx=20, pady=10)
        self.update_classes_list()

        # Input Frame
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(input_frame, text="Name:").pack(side="left")
        self.class_name_entry = ctk.CTkEntry(input_frame)
        self.class_name_entry.pack(side="left", padx=5)

        ctk.CTkLabel(input_frame, text="Instructor:").pack(side="left")
        self.class_instructor_entry = ctk.CTkEntry(input_frame)
        self.class_instructor_entry.pack(side="left", padx=5)

        ctk.CTkLabel(input_frame, text="Schedule:").pack(side="left")
        self.class_schedule_entry = ctk.CTkEntry(input_frame)
        self.class_schedule_entry.pack(side="left", padx=5)

        ctk.CTkButton(input_frame, text="Add Class", command=self.add_class).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Remove Class", command=self.remove_class).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Increment Attendance", command=self.increment_attendance).pack(side="left", padx=5)

    def update_classes_list(self):
        self.classes_tree.delete(*self.classes_tree.get_children())
        for class_ in self.classes:
            self.classes_tree.insert('', 'end', values=(class_['id'], class_['name'], class_['instructor'], class_['schedule'], class_.get('attendance', 0)))

    def add_class(self):
        name = self.class_name_entry.get()
        instructor = self.class_instructor_entry.get()
        schedule = self.class_schedule_entry.get()
        if name and instructor and schedule:
            new_id = max([c['id'] for c in self.classes], default=0) + 1
            self.classes.append({
                "id": new_id,
                "name": name,
                "instructor": instructor,
                "schedule": schedule,
                "attendance": 0
            })
            self.save_data(self.classes, 'classes.json')
            self.update_classes_list()
            self.class_name_entry.delete(0, 'end')
            self.class_instructor_entry.delete(0, 'end')
            self.class_schedule_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please enter all class details.")

    def remove_class(self):
        selected_item = self.classes_tree.selection()
        if selected_item:
            class_id = self.classes_tree.item(selected_item)['values'][0]
            self.classes = [c for c in self.classes if c['id'] != class_id]
            self.save_data(self.classes, 'classes.json')
            self.update_classes_list()
        else:
            messagebox.showerror("Error", "Please select a class to remove.")

    def increment_attendance(self):
        selected_item = self.classes_tree.selection()
        if selected_item:
            class_id = self.classes_tree.item(selected_item)['values'][0]
            for class_ in self.classes:
                if class_['id'] == class_id:
                    class_['attendance'] = class_.get('attendance', 0) + 1
                    break
            self.save_data(self.classes, 'classes.json')
            self.update_classes_list()
        else:
            messagebox.showerror("Error", "Please select a class to increment attendance.")

    def show_equipment(self):
        self.clear_main_frame()
        label = ctk.CTkLabel(self.main_frame, text="Equipment", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=20, pady=20)

        # Table
        columns = ('ID', 'Name', 'Quantity', 'Last Maintenance')
        self.equipment_tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')
        for col in columns:
            self.equipment_tree.heading(col, text=col)
            self.equipment_tree.column(col, width=100)
        self.equipment_tree.pack(expand=True, fill="both", padx=20, pady=10)
        self.update_equipment_list()

        # Input Frame
        input_frame = ctk.CTkFrame(self.main_frame)
        input_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(input_frame, text="Name:").pack(side="left")
        self.equipment_name_entry = ctk.CTkEntry(input_frame)
        self.equipment_name_entry.pack(side="left", padx=5)

        ctk.CTkLabel(input_frame, text="Quantity:").pack(side="left")
        self.equipment_quantity_entry = ctk.CTkEntry(input_frame)
        self.equipment_quantity_entry.pack(side="left", padx=5)

        ctk.CTkButton(input_frame, text="Add Equipment", command=self.add_equipment).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Remove Equipment", command=self.remove_equipment).pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="Update Maintenance", command=self.update_maintenance).pack(side="left", padx=5)

    def update_equipment_list(self):
        self.equipment_tree.delete(*self.equipment_tree.get_children())
        for equip in self.equipment:
            self.equipment_tree.insert('', 'end', values=(equip['id'], equip['name'], equip['quantity'], equip['last_maintenance']))

    def add_equipment(self):
        name = self.equipment_name_entry.get()
        quantity = self.equipment_quantity_entry.get()
        if name and quantity:
            try:
                quantity = int(quantity)
                new_id = max([e['id'] for e in self.equipment], default=0) + 1
                self.equipment.append({
                    "id": new_id,
                    "name": name,
                    "quantity": quantity,
                    "last_maintenance": datetime.now().strftime("%Y-%m-%d")
                })
                self.save_data(self.equipment, 'equipment.json')
                self.update_equipment_list()
                self.equipment_name_entry.delete(0, 'end')
                self.equipment_quantity_entry.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number.")
        else:
            messagebox.showerror("Error", "Please enter both name and quantity.")

    def remove_equipment(self):
        selected_item = self.equipment_tree.selection()
        if selected_item:
            equipment_id = self.equipment_tree.item(selected_item)['values'][0]
            self.equipment = [e for e in self.equipment if e['id'] != equipment_id]
            self.save_data(self.equipment, 'equipment.json')
            self.update_equipment_list()
        else:
            messagebox.showerror("Error", "Please select an equipment to remove.")

    def update_maintenance(self):
        selected_item = self.equipment_tree.selection()
        if selected_item:
            equipment_id = self.equipment_tree.item(selected_item)['values'][0]
            for equip in self.equipment:
                if equip['id'] == equipment_id:
                    equip['last_maintenance'] = datetime.now().strftime("%Y-%m-%d")
                    break
            self.save_data(self.equipment, 'equipment.json')
            self.update_equipment_list()
        else:
            messagebox.showerror("Error", "Please select an equipment to update maintenance.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = GymMaster(root)
    root.mainloop()