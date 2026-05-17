
import tkinter as tk
import pandas as pd
from tkinter import messagebox

# Load the datasets using pandas
def load_data():
    try:
        # Load the disease and precaution CSV files into pandas DataFrames
        diseases_df = pd.read_csv(r'Z:\Datasets\dataset.csv')
        precautions_df = pd.read_csv(r'Z:\Datasets\symptom_precaution.csv')
        return diseases_df, precautions_df
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Dataset not found: {e.filename}")
        return None, None

# Function to get disease and precaution advice based on symptoms
def get_advice_from_dataset(symptoms):
    advice_output = ""
    diseases_df, precautions_df = load_data()

    if diseases_df is not None and precautions_df is not None:
        # Iterate through each symptom and check if it exists in the dataset
        for _, row in diseases_df.iterrows():
            # Use correct column names for symptoms
            row_symptoms = {row['Symptom_1'].strip().lower(), row['Symptom_2'].strip().lower(), row['Symptom_3'].strip().lower()}
            if set(symptoms).issubset(row_symptoms):
                # If symptoms match, retrieve the disease
                disease = row['Disease']

                # Get precautions for the identified disease
                precautions = []
                # Extract Precaution_1, Precaution_2, etc. for the identified disease
                for i in range(1, 6):  # Assume there are 5 precautions
                    precaution_column = f'Precaution_{i}'
                    if precaution_column in precautions_df.columns:
                        precaution = precautions_df.loc[precautions_df['Disease'] == disease, precaution_column].values
                        if len(precaution) > 0:
                            precautions.append(precaution[0])

                # Show up to 2 precautions
                precautions_text = "\n".join(precautions[:2]) if precautions else "No precautions available."

                # Append disease and precautions to the output
                advice_output += f"Disease: {disease}\nPrecautions: {precautions_text}\n\n"
                break

        if advice_output.strip() == "":
            advice_output = "No matching symptoms found. Please try again."

    return advice_output

# Function to handle button click and display results in the Text widget
def check_symptoms():
    symptoms_input = entry_symptoms.get().lower().split(",")  # Input can be comma-separated symptoms
    symptoms_input = [symptom.strip() for symptom in symptoms_input]  # Remove extra whitespace
    advice_output = get_advice_from_dataset(symptoms_input)

    # Update the text widget with the advice
    text_advice.config(state=tk.NORMAL)  # Enable text widget for editing
    text_advice.delete(1.0, tk.END)  # Clear previous content
    text_advice.insert(tk.END, advice_output)  # Insert new advice
    text_advice.config(state=tk.DISABLED)  # Disable text widget for editing

# Create the main window
root = tk.Tk()
root.title("Health Monitoring System")
root.geometry("600x500")

# Add a label for the symptoms input
label_symptoms = tk.Label(root, text="Enter Symptoms (comma separated):")
label_symptoms.pack(pady=10)

# Entry widget for entering symptoms
entry_symptoms = tk.Entry(root, width=50)
entry_symptoms.pack(pady=5)

# Button to check symptoms and provide advice
button_check = tk.Button(root, text="Check Symptoms", command=check_symptoms)
button_check.pack(pady=10)

# Text widget to display the advice based on symptoms
text_advice = tk.Text(root, height=12, width=70, wrap=tk.WORD, state=tk.DISABLED)
text_advice.pack(pady=10)

# Add a quit button to close the application
button_quit = tk.Button(root, text="Quit", command=root.quit)
button_quit.pack(pady=10)

# Run the main loop
root.mainloop()

