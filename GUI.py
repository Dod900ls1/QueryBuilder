import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('1440x900')
        self.bg_color = '#333333'  # Dark theme background color
        self.fg_color = 'white'  # Dark theme foreground color

        self.root.configure(bg=self.bg_color)

        # Variables for checkboxes and text widget
        self.checkboxes = []  # List to store checkboxes and their associated IntVars
        self.columns_text = None  # Text widget to display generated SQL query
        self.output_dropdown = None  # Dropdown for selecting the output column
        self.model_label = None  # Label for selecting the regression model
        self.model_dropdown = None  # Dropdown for selecting the model type
        self.submit_button = None  # Button to generate SQL query
        self.selected_output = tk.StringVar()  # Variable to store the selected output column
        self.selected_model = tk.StringVar(
            value="Select an option")  # Variable to store the selected model option with default value

        # Create a button to browse for a file (visible initially)
        self.browse_button = tk.Button(self.root, text="Browse", command=self.create_widgets, bg=self.bg_color,
                                       fg=self.fg_color)
        self.browse_button.pack(pady=10, padx=10)

        self.root.mainloop()

    def reload_widgets(self):
        # Remove existing widgets for checkboxes, text widget, and dropdowns
        for checkbox in self.checkboxes:
            checkbox[0].destroy()
        self.columns_text.destroy()
        self.output_label.destroy()
        self.output_dropdown.destroy()
        self.column_names_label.destroy()
        self.checkbox_frame.destroy()
        self.submit_button.destroy()
        self.model_dropdown.destroy()
        self.model_label.destroy()

        # Recreate the widgets with the new data from the CSV file.
        self.create_widgets()

    def create_widgets(self):
        # Open a file dialog to select a CSV file
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=[("CSV files", "*.csv")])
        try:
            self.file = pd.read_csv(self.filename, encoding='utf-8')
        except UnicodeDecodeError:
            messagebox.showerror("Error",
                                 "Unable to read the selected file. Please ensure it is in the correct format.")
            return

        # Set background and text color for newly created widgets
        bg_color = self.bg_color
        fg_color = self.fg_color

        # Configure the browse button to call the reload_widgets function
        self.browse_button.config(command=lambda: self.reload_widgets())

        # Create a label for selecting the output column
        self.output_label = tk.Label(self.root, text="Select the Output Column:", bg=bg_color, fg=fg_color)
        self.output_label.pack(padx=10, pady=10, anchor=tk.SW)

        # Create a dropdown for selecting the output column
        self.output_dropdown = tk.OptionMenu(self.root, self.selected_output, *self.file.columns)
        self.output_dropdown.config(bg=bg_color, fg=fg_color)

        # Style the option menu options
        self.output_dropdown['menu'].config(bg=bg_color, fg=fg_color)

        self.output_dropdown.pack(padx=10, pady=10, anchor=tk.SW)

        # Create a label for selecting input columns
        self.column_names_label = tk.Label(self.root, text="Select Input Columns:", bg=bg_color, fg=fg_color)
        self.column_names_label.pack(pady=10, padx=10, anchor=tk.NW)

        # Create a frame to hold the checkboxes using the grid geometry manager
        self.checkbox_frame = tk.Frame(self.root, bg=bg_color)
        self.checkbox_frame.pack(pady=10, padx=10, anchor=tk.NW)

        # Create checkboxes for each column within the checkbox frame
        for i, j in enumerate(self.file.columns):
            var_input = tk.IntVar()  # Variable to store the checkbox state for input columns

            checkbox_input = tk.Checkbutton(self.checkbox_frame, text=j, variable=var_input, bg=bg_color, fg=fg_color,
                                            selectcolor=bg_color)
            checkbox_input.grid(row=0, column=i, padx=10, pady=10)  # Place all checkboxes in the same row (row=0)

            self.checkboxes.append((checkbox_input, var_input))  # Store checkboxes and their associated IntVars

        # Create a text widget for displaying columns
        self.columns_text = tk.Text(self.root, height=15, width=90, bg=bg_color, fg=fg_color)
        self.columns_text.pack(pady=10)
        self.columns_text.insert(tk.END, "Generated SQL Query will appear here.")

        # Create a dropdown for selecting a model and place it in the left-bottom
        self.model_label = tk.Label(self.root, text="Select the Regression Model:", bg=bg_color, fg=fg_color)
        self.model_label.pack(padx=10, pady=10, anchor=tk.NW)
        model_options = ["Linear Regression Model", "Logistic Regression Model"]
        self.model_dropdown = tk.OptionMenu(self.root, self.selected_model, *model_options)
        self.model_dropdown.config(bg=bg_color, fg=fg_color)

        # Style the option menu options
        self.model_dropdown['menu'].config(bg=bg_color, fg=fg_color)

        self.model_dropdown.pack(padx=10, pady=10, anchor=tk.NW)

        # Create the submit button and place it directly under the model_dropdown
        self.submit_button = tk.Button(self.root, text="Submit", command=self.process_selection, bg=bg_color,
                                       fg=fg_color)
        self.submit_button.pack(pady=10, padx=10, anchor=tk.NW)

        # Update the text widget with the generated SQL query
        self.columns_text.delete('1.0', tk.END)
        self.columns_text.insert(tk.END, "Generated SQL Query will appear here.")

    def process_selection(self):
        global model_type
        selected_input_columns = [checkbox.cget("text") for checkbox, input_var in self.checkboxes if
                                  input_var.get() == 1]
        selected_output_column = self.selected_output.get()
        selected_model = self.selected_model.get()

        if selected_model == "Logistic Regression Model":
            model_type = "logistic_reg"
        elif selected_model == "Linear Regression Model":
            model_type = "linear_reg"

        if selected_input_columns and selected_output_column and selected_model != "Select an option":
            # Generate SQL query based on user selections
            sql_query = f"""
CREATE OR REPLACE MODEL `your_dataset_id.your_model_id`
OPTIONS(
    model_type='{model_type}',
    labels=['{selected_output_column}'],
    HPARAM_TUNING_OBJECTIVES = ['F1_SCORE'],
    NUM_TRIALS=1
    ) AS
SELECT
    {', '.join(selected_input_columns)}
FROM
    `your_project_id.your_dataset_id.your_training_data`;
"""
            # Update the text widget with the generated SQL query
            self.columns_text.delete('1.0', tk.END)
            self.columns_text.insert(tk.END, sql_query)
        else:
            # Display an error message if input is incomplete
            message = "Error: Please select input columns, an output column, and a model type"
            messagebox.showerror("Error", message)
