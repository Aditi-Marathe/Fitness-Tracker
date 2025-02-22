import tkinter as tk
from tkinter import messagebox, filedialog

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
        self.root.title("Fitness Tracker")
        self.root.geometry("500x600")
        self.root.configure(bg="#ADD8E6")  # Light Blue Background

        self.user = None

        title_font = ("Helvetica", 32, "bold")  # Increased title size
        label_font = ("Helvetica", 14)
        button_font = ("Helvetica", 12, "bold")

        # **Title Label (Big Size)**
        self.title_label = tk.Label(root, text="Fitness Tracker", font=title_font, fg="black", bg="#ADD8E6")
        self.title_label.pack(pady=20)

        # Create User Button
        self.create_user_button = tk.Button(root, text="Create User", command=self.create_user_window, font=button_font, bg="#001f3f", fg="white", width=20)
        self.create_user_button.pack(pady=10)

        # Add Workout Section
        self.create_label_entry("Date (YYYY-MM-DD):", "date_entry")
        self.create_label_entry("Exercise Type:", "exercise_entry")
        self.create_label_entry("Duration (minutes):", "duration_entry")
        self.create_label_entry("Calories Burned:", "calories_entry")

        self.add_workout_button = tk.Button(root, text="Add Workout", command=self.add_workout, font=button_font, bg="#4682B4", fg="white", width=20)
        self.add_workout_button.pack(pady=10)

        # View Workouts
        self.view_workouts_button = tk.Button(root, text="View Workouts", command=self.view_workouts, font=button_font, bg="#FF8C00", fg="white", width=20)
        self.view_workouts_button.pack(pady=10)

        # Save and Load Data
        self.save_data_button = tk.Button(root, text="Save Data", command=self.save_data, font=button_font, bg="#DC143C", fg="white", width=20)
        self.save_data_button.pack(pady=10)

        self.load_data_button = tk.Button(root, text="Load Data", command=self.load_data, font=button_font, bg="#8A2BE2", fg="white", width=20)
        self.load_data_button.pack(pady=10)

    def create_label_entry(self, label_text, attr_name):
        label = tk.Label(self.root, text=label_text, font=("Helvetica", 14), fg="black", bg="#ADD8E6")
        label.pack()
        entry = tk.Entry(self.root, font=("Helvetica", 14))
        entry.pack(pady=5)
        setattr(self, attr_name, entry)

    def create_user_window(self):
        """Opens a popup window to create a user"""
        user_window = tk.Toplevel(self.root)
        user_window.title("Create User")
        user_window.geometry("400x300")
        user_window.configure(bg="#87CEEB")  # Slightly Darker Light Blue

        label_font = ("Helvetica", 14)

        tk.Label(user_window, text="Name:", font=label_font, fg="black", bg="#87CEEB").pack(pady=5)
        name_entry = tk.Entry(user_window, font=label_font)
        name_entry.pack()

        tk.Label(user_window, text="Age:", font=label_font, fg="black", bg="#87CEEB").pack(pady=5)
        age_entry = tk.Entry(user_window, font=label_font)
        age_entry.pack()

        tk.Label(user_window, text="Weight:", font=label_font, fg="black", bg="#87CEEB").pack(pady=5)
        weight_entry = tk.Entry(user_window, font=label_font)
        weight_entry.pack()

        def create_user():
            name = name_entry.get()
            age = age_entry.get()
            weight = weight_entry.get()

            if not name or not age or not weight:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                age = int(age)
                weight = float(weight)
            except ValueError:
                messagebox.showerror("Error", "Age and Weight must be numbers.")
                return

            self.user = User(name, age, weight)
            messagebox.showinfo("Success", "User created successfully!")
            user_window.destroy()

        tk.Button(user_window, text="Create", command=create_user, font=label_font, bg="#4682B4", fg="white").pack(pady=10)

    def add_workout(self):
        """Adds a workout after validation"""
        if self.user is None:
            messagebox.showerror("Error", "Please create a user first.")
            return

        date = self.date_entry.get()
        exercise_type = self.exercise_entry.get()
        duration = self.duration_entry.get()
        calories_burned = self.calories_entry.get()

        if not date or not exercise_type or not duration or not calories_burned:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            duration = int(duration)
            calories_burned = int(calories_burned)
        except ValueError:
            messagebox.showerror("Error", "Duration and Calories Burned must be numbers.")
            return

        self.user.add_workout(Workout(date, exercise_type, duration, calories_burned))
        messagebox.showinfo("Success", "Workout added successfully!")

    def view_workouts(self):
        if self.user:
            messagebox.showinfo("Workouts", self.user.view_workouts())
        else:
            messagebox.showerror("Error", "Please create a user first.")

    def save_data(self):
        if self.user:
            filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if filename:
                self.user.save_data(filename)
                messagebox.showinfo("Success", "Data saved successfully!")
        else:
            messagebox.showerror("Error", "Please create a user first.")

    def load_data(self):
        if self.user:
            filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if filename:
                self.user.load_data(filename)
                messagebox.showinfo("Success", "Data loaded successfully!")
        else:
            messagebox.showerror("Error", "Please create a user first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()
