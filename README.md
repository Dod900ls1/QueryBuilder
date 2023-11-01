# BigQuery Model Query Generator

**BigQuery Model Query Generator** is a Python program built using the tkinter library that provides a graphical user interface (GUI) for generating SQL queries to create machine learning models in Google BigQuery. 
This program simplifies the process of defining machine learning models and their input features based on CSV data files. The generated SQL queries can be directly executed in BigQuery to create and train machine learning models.

## Features

- GUI: The program has a user interface that allows users to select input columns, output columns, and the model type.
- Input Selection: Users can choose input columns to use as features in their machine learning model using checkboxes.
- Output Selection: Users can select the output column, which is the target variable for the regression model.
- Model Type: The program offers two types of regression models - Linear Regression and Logistic Regression, selectable from a dropdown menu.
- Query Generation: After choosing input columns, output columns, and the model type, the program generates the SQL query for creating and training the machine learning model in BigQuery.
- Query Display: The generated SQL query is presented in a text widget, facilitating copying and pasting it into BigQuery for execution.

## Usage

1. Launch the program by running the script.
2. Click the "Browse" button to select a CSV data file to work with.
3. Choose the output column, input columns, and the regression model type.
4. Click the "Submit" button to generate the SQL query.
5. The generated SQL query will be displayed in the text widget, ready for you to copy and use in Google BigQuery.

## Dependencies

- Python 3
- tkinter library for the GUI.
- pandas library for reading and processing CSV files.

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python and the required dependencies installed.
3. Run the program by executing the script.

## Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request.

## Author

<a href="https://github.com/Dod900ls1">Yehor Boiar</a>

## Design
<a href="https://github.com/Herobread">Alex Nazarenko</a>

