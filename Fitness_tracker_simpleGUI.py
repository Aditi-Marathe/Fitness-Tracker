import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # For icons and images

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date} - {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"

class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join(str(workout) for workout in self.workouts) if self.workouts else "No workouts recorded."

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ Fitness Tracker")
        self.root.configure(bg="#f0f0f0")

        self.user = None
        font = ("Helvetica", 14, "bold")
        button_font = ("Helvetica", 12)
        entry_bg = "#ffffff"

        tk.Label(root, text="🏋️ Fitness Tracker", font=("Helvetica", 18, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=10)

        self.create_input_section("👤 Name:", 1)
        self.create_input_section("🎂 Age:", 2)
        self.create_input_section("⚖️ Weight:", 3)

        self.create_user_button = tk.Button(root, text="Create User", command=self.create_user, bg="#87CEFA", font=button_font)
        self.create_user_button.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Label(root, text="📅 Date (YYYY-MM-DD):", font=font, bg="#f0f0f0").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = tk.Entry(root, font=font, bg=entry_bg)
        self.date_entry.grid(row=5, column=1, padx=10, pady=5)

        self.create_input_section("💪 Exercise Type:", 6)
        self.create_input_section("⏳ Duration (minutes):", 7)
        self.create_input_section("🔥 Calories Burned:", 8)

        self.add_buttons()

    def create_input_section(self, label_text, row):
        font = ("Helvetica", 14)
        tk.Label(self.root, text=label_text, font=font, bg="#f0f0f0").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(self.root, font=font, bg="#ffffff")
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"entry_{row}", entry)

    def add_buttons(self):
        button_font = ("Helvetica", 12, "bold")
        button_bg = "#e0e0e0"

        self.add_workout_button = tk.Button(self.root, text="➕ Add Workout", command=self.add_workout, bg="#90EE90", font=button_font)
        self.add_workout_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.view_workouts_button = tk.Button(self.root, text="📜 View Workouts", command=self.view_workouts, bg="#FFD700", font=button_font)
        self.view_workouts_button.grid(row=10, column=0, columnspan=2, pady=10)

        self.save_data_button = tk.Button(self.root, text="💾 Save Data", command=self.save_data, bg="#FF6347", font=button_font)
        self.save_data_button.grid(row=11, column=0, columnspan=2, pady=10)

        self.load_data_button = tk.Button(self.root, text="📂 Load Data", command=self.load_data, bg="#FF69B4", font=button_font)
        self.load_data_button.grid(row=12, column=0, columnspan=2, pady=10)

    def create_user(self):
        name = self.entry_1.get()
        age = int(self.entry_2.get())
        weight = float(self.entry_3.get())
        self.user = User(name, age, weight)
        messagebox.showinfo("Success", "User created successfully! 🎉")

    def add_workout(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        date = self.date_entry.get()
        exercise_type = self.entry_6.get()
        duration = int(self.entry_7.get())
        calories_burned = int(self.entry_8.get())
        workout = Workout(date, exercise_type, duration, calories_burned)
        self.user.add_workout(workout)
        messagebox.showinfo("Success", "Workout added successfully! ✅")

    def view_workouts(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        workouts = self.user.view_workouts()
        messagebox.showinfo("📜 Workouts", workouts)

    def save_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            self.user.save_data(filename)
            messagebox.showinfo("Success", "Data saved successfully! 💾")

    def load_data(self):
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            self.user.load_data(filename)
            messagebox.showinfo("Success", "Data loaded successfully! 📂")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()