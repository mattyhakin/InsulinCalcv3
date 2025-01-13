import tkinter as tk
from tkinter import messagebox

# Constants
BLOOD_SUGAR_MIN = 4
BLOOD_SUGAR_MIN_CORRECTION = -1
BLOOD_SUGAR_MAX = 7
BLOOD_SUGAR_MAX_CORRECTION = 1

DOSAGE_RATIO = {
    'breakfast': 2,
    'lunch': 1.5,
    'dinner': 1.5,
    'snack': 1.5,
}

def update_ratio():
    try:
        # Get the new ratio entered by the user
        new_ratio = float(new_ratio_entry.get())
        selected_type = dose_type_var.get()
        
        # Update the ratio for the selected dose type
        DOSAGE_RATIO[selected_type] = new_ratio
        messagebox.showinfo("Success", f"The ratio for {selected_type} has been updated to {new_ratio}.")
        current_ratio_label.config(text=f"Current Ratio: {new_ratio}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric value for the new ratio.")

def confirm_ratio(*args):
    # Display the current ratio
    selected_type = dose_type_var.get()
    if selected_type in DOSAGE_RATIO:
        ratio = DOSAGE_RATIO[selected_type]
        current_ratio_label.config(text=f"Current Ratio: {ratio}")

def calculate_dose():
    try:
        # Get dose type and ratio
        dose_type = dose_type_var.get()
        ratio = DOSAGE_RATIO[dose_type]
        
        # Get carbs and base dose
        carbs = float(carbs_entry.get())
        dose = ratio * carbs / 10

        # Check for recent insulin dose
        if recent_insulin_var.get() == "yes":
            messagebox.showinfo("Result", f"You need {dose:.1f} units of insulin.")
            return

        # Get blood sugar level
        blood_sugar_level = float(blood_sugar_entry.get())
        multiplier = 0
        limit = 0

        # Determine correctional dose
        if blood_sugar_level > BLOOD_SUGAR_MAX:
            multiplier = BLOOD_SUGAR_MAX_CORRECTION
            limit = BLOOD_SUGAR_MAX
        elif blood_sugar_level < BLOOD_SUGAR_MIN:
            multiplier = BLOOD_SUGAR_MIN_CORRECTION
            limit = BLOOD_SUGAR_MIN

        cordiff = blood_sugar_level - limit
        correction = cordiff * multiplier if multiplier != 0 else 0
        total_dose = round(dose + correction)

        # Show the result
        messagebox.showinfo("Result", f"You need {total_dose} units of insulin.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# GUI Setup
root = tk.Tk()
root.title("Insulin Dose Calculator")

# Dose Type
tk.Label(root, text="Select Dose Type:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
dose_type_var = tk.StringVar(value="breakfast")
dose_type_var.trace("w", confirm_ratio)  # Trace changes in the dose type variable
dose_type_menu = tk.OptionMenu(root, dose_type_var, *DOSAGE_RATIO.keys())
dose_type_menu.grid(row=0, column=1, padx=10, pady=5)

# Current Ratio Display
current_ratio_label = tk.Label(root, text="Current Ratio: -")
current_ratio_label.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Ratio Update Section
tk.Label(root, text="New Ratio:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
new_ratio_entry = tk.Entry(root)
new_ratio_entry.grid(row=2, column=1, padx=10, pady=5)
update_ratio_button = tk.Button(root, text="Update Ratio", command=update_ratio)
update_ratio_button.grid(row=2, column=2, padx=10, pady=5)

# Carbohydrate Intake
tk.Label(root, text="Carbs (g):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
carbs_entry = tk.Entry(root)
carbs_entry.grid(row=3, column=1, padx=10, pady=5)

# Recent Insulin Dose
tk.Label(root, text="Recent Insulin Dose (last 90 mins):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
recent_insulin_var = tk.StringVar(value="no")
tk.Radiobutton(root, text="Yes", variable=recent_insulin_var, value="yes").grid(row=4, column=1, sticky="w")
tk.Radiobutton(root, text="No", variable=recent_insulin_var, value="no").grid(row=4, column=1, sticky="e")

# Blood Sugar Level
tk.Label(root, text="Current Blood Sugar (mmol/L):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
blood_sugar_entry = tk.Entry(root)
blood_sugar_entry.grid(row=5, column=1, padx=10, pady=5)

# Calculate Button
calculate_button = tk.Button(root, text="Calculate Dose", command=calculate_dose)
calculate_button.grid(row=6, column=0, columnspan=3, pady=10)

# Run the GUI loop
root.mainloop()