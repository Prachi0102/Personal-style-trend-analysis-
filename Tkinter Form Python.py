import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database setup (MySQL)
def setup_database():
    conn = mysql.connector.connect(
        host="localhost",  
        user="root",      
        password="Prachi@0102",  
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS survey_db;")
    conn.commit()
    conn.close()

    # Now, create the tables in the survey_db
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prachi@0102",  
        database="survey_db"
    )
    cursor = conn.cursor()

    # Create survey_responses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        age_group VARCHAR(50),
        gender VARCHAR(50),
        style VARCHAR(50),
        shopping_frequency VARCHAR(50),
        clothing_colors VARCHAR(50),
        favorite_outfit_elements VARCHAR(100),
        most_worn_clothing VARCHAR(100),
        satisfaction VARCHAR(100),
        purchasing_factors VARCHAR(100),
        monthly_spending VARCHAR(50),
        shopping_preference VARCHAR(50),
        confidence_frequency VARCHAR(50),
        personal_style_goal VARCHAR(100)
    );''')

    # Create users table with survey_filled column
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(255),
        survey_filled BOOLEAN DEFAULT FALSE  -- Add the survey_filled column
    );''')
    conn.commit()
    conn.close()

# Function to register the user
def register_user():
    username = username_entry_register.get()
    password = password_entry_register.get()
    confirm_password = confirm_password_entry.get()

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prachi@0102",  
        database="survey_db"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Username already exists!")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        register_window.destroy()
    conn.close()

# Function to log in the user
def login():
    username = username_entry_login.get()
    password = password_entry_login.get()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prachi@0102",  
        database="survey_db"
    )
    cursor = conn.cursor()

    # Modify the query to select only the necessary columns (id and survey_filled)
    cursor.execute("SELECT id, survey_filled FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]  
        survey_filled = user[1]  
        if survey_filled:
            messagebox.showinfo("Welcome", "Welcome back! You have already filled the survey.")
        
        else:
            open_survey_page(user_id)  
    else:
        messagebox.showerror("Error", "Invalid username or password!")
    conn.close()


# Function to open the registration page
def open_register_page():
    global register_window, username_entry_register, password_entry_register, confirm_password_entry
    register_window = tk.Toplevel(root)
    register_window.title("Register")
    register_window.geometry("400x300")

    tk.Label(register_window, text="Register", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Username
    tk.Label(register_window, text="Username:", font=("Arial", 12)).pack(anchor="w", padx=20)
    username_entry_register = tk.Entry(register_window, font=("Arial", 12))
    username_entry_register.pack(padx=20, fill="x", pady=5)

    # Password
    tk.Label(register_window, text="Password:", font=("Arial", 12)).pack(anchor="w", padx=20)
    password_entry_register = tk.Entry(register_window, show="*", font=("Arial", 12))
    password_entry_register.pack(padx=20, fill="x", pady=5)

    # Confirm Password
    tk.Label(register_window, text="Confirm Password:", font=("Arial", 12)).pack(anchor="w", padx=20)
    confirm_password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
    confirm_password_entry.pack(padx=20, fill="x", pady=5)

    # Register Button
    tk.Button(register_window, text="Register", command=register_user, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)

# Function to open the survey page
def open_survey_page(user_id):
    global survey_window
    survey_window = tk.Toplevel(root)
    survey_window.title("Personal Style Trend Analysis Survey")
    survey_window.geometry("600x800")
    root.withdraw()  # Hide the main login window

    # Scrollable frame for the survey form
    canvas = tk.Canvas(survey_window)
    scrollbar = tk.Scrollbar(survey_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Survey Title
    tk.Label(scrollable_frame, text="Personal Style Trend Analysis Survey", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(scrollable_frame, text="Your responses are anonymous. Thank you for your participation!", wraplength=500, justify="center").pack(pady=10)

    # Question 1: Age Group
    tk.Label(scrollable_frame, text="What is your age_group?", font=("Arial", 12)).pack(anchor="w", padx=20)
    age_group_var = tk.StringVar()
    tk.Radiobutton(scrollable_frame, text="Under 18", variable=age_group_var, value="Under 18").pack(anchor="w", padx=40)
    tk.Radiobutton(scrollable_frame, text="18-25", variable=age_group_var, value="18-30").pack(anchor="w", padx=40)
    tk.Radiobutton(scrollable_frame, text="25-35", variable=age_group_var, value="31-50").pack(anchor="w", padx=40)
    tk.Radiobutton(scrollable_frame, text="35+", variable=age_group_var, value="51+").pack(anchor="w", padx=40)

    # Question 2: Gender
    tk.Label(scrollable_frame, text="What is your gender?", font=("Arial", 12)).pack(anchor="w", padx=20)
    gender_var = tk.StringVar()
    tk.Radiobutton(scrollable_frame, text="Male", variable=gender_var, value="Male").pack(anchor="w", padx=40)
    tk.Radiobutton(scrollable_frame, text="Female", variable=gender_var, value="Female").pack(anchor="w", padx=40)
    tk.Radiobutton(scrollable_frame, text="Other", variable=gender_var, value="Other").pack(anchor="w", padx=40)

    # Question 3: Favorite Clothing Style
    tk.Label(scrollable_frame, text="What is your favorite_outfit_elements?", font=("Arial", 12)).pack(anchor="w", padx=20)
    style_var = tk.StringVar()
    style_options = ["Casual", "Formal", "Sporty", "Trendy"]
    for option in style_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=style_var, value=option).pack(anchor="w", padx=40)

    # Question 4: How often do you shop for clothing?
    tk.Label(scrollable_frame, text="How often do you shopping_frequency?", font=("Arial", 12)).pack(anchor="w", padx=20)
    shopping_frequency_var = tk.StringVar()
    shopping_frequency_options = ["Weekly","Once a month", "Once every 2-3 months", "Once every 6 months", "Rarely"]
    for option in shopping_frequency_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=shopping_frequency_var, value=option).pack(anchor="w", padx=40)

    # Question 5: Favorite Clothing Colors
    tk.Label(scrollable_frame, text="What are your clothing_colors?", font=("Arial", 12)).pack(anchor="w", padx=20)
    colors_var = tk.StringVar()
    colors_options = ["Neutral","Brights","Dark Tones","Mixed Patterns","Pastels"]
    for option in colors_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=colors_var, value=option).pack(anchor="w", padx=40)

    #colors_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=colors_var)
    #colors_entry.pack(padx=40, pady=5, fill="x")

    # Question 6: Favorite Outfit Elements
    tk.Label(scrollable_frame, text="What are your favorite_outfit_elements?", font=("Arial", 12)).pack(anchor="w", padx=20)
    outfit_elements_var = tk.StringVar()
    outfit_elements_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=outfit_elements_var)
    outfit_elements_entry.pack(padx=40, pady=5, fill="x")

    # Question 7: Most Worn Clothing
    tk.Label(scrollable_frame, text="What is the most_worn_clothing item in your wardrobe?", font=("Arial", 12)).pack(anchor="w", padx=20)
    most_worn_var = tk.StringVar()
    most_worn_options = ["Jeans & T-shirts","Dresses or Skirts","Sarees","Shirt-Pant"]
    for option in most_worn_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=most_worn_var, value=option).pack(anchor="w", padx=40)

    
    #most_worn_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=most_worn_var)
    #most_worn_entry.pack(padx=40, pady=5, fill="x")

    # Question 8: Clothing Satisfaction
    tk.Label(scrollable_frame, text="How satisfied are you with your current clothing?", font=("Arial", 12)).pack(anchor="w", padx=20)
    satisfaction_var = tk.StringVar()
    satisfaction_options = ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    for option in satisfaction_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=satisfaction_var, value=option).pack(anchor="w", padx=40)

    # Question 9: Main Factors in Clothing Purchase
    tk.Label(scrollable_frame, text="What are the main factors influencing your purchasing_factors?", font=("Arial", 12)).pack(anchor="w", padx=20)
    purchase_factors_var = tk.StringVar()
    purchase_factors_options = ["Celebrity Style","Trendlines","Fit and Comfort","Color or Personal Style"]
    for option in purchase_factors_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=purchase_factors_var, value=option).pack(anchor="w", padx=40)

    #purchase_factors_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=purchase_factors_var)
    #purchase_factors_entry.pack(padx=40, pady=5, fill="x")

    # Question 10: Monthly Spending on Clothing
    tk.Label(scrollable_frame, text="How much do you monthly_spending?", font=("Arial", 12)).pack(anchor="w", padx=20)
    spending_var = tk.StringVar()
    spending_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=spending_var)
    spending_entry.pack(padx=40, pady=5, fill="x")

    # Question 11: Shopping Preference (Online or In-Store)
    tk.Label(scrollable_frame, text="Do you shopping_preference?", font=("Arial", 12)).pack(anchor="w", padx=20)
    shopping_preference_var = tk.StringVar()
    shopping_preference_options = ["Online", "In-store", "Both"]
    for option in shopping_preference_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=shopping_preference_var, value=option).pack(anchor="w", padx=40)

    # Question 12: Confidence in Fashion
    tk.Label(scrollable_frame, text="How often do you feel confidence_frequency?", font=("Arial", 12)).pack(anchor="w", padx=20)
    confidence_var = tk.StringVar()
    confidence_options = ["Always", "Often", "Sometimes", "Rarely", "Never"]
    for option in confidence_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=confidence_var, value=option).pack(anchor="w", padx=40)

    # Question 13: Personal Style Goals
    tk.Label(scrollable_frame, text="What is your personal_style_goal?", font=("Arial", 12)).pack(anchor="w", padx=20)
    style_goal_var = tk.StringVar()
    style_goal_options = ["To feel more confident in my appearance","To explore new trends","To focus on comfort and functionality","To better express my personality"]
    for option in style_goal_options:
        tk.Radiobutton(scrollable_frame, text=option, variable=style_goal_var, value=option).pack(anchor="w", padx=40)

    #style_goal_entry = tk.Entry(scrollable_frame, font=("Arial", 12), textvariable=style_goal_var)
    #style_goal_entry.pack(padx=40, pady=5, fill="x")

    # Submit Button for Survey
    def submit_survey():
        # Get all responses
        responses = {
            "age_group": age_group_var.get(),
            "gender": gender_var.get(),
            "style": style_var.get(),
            "shopping_frequency": shopping_frequency_var.get(),
            "clothing_colors": colors_var.get(),
            "favorite_outfit_elements": outfit_elements_var.get(),
            "most_worn_clothing": most_worn_var.get(),
            "satisfaction": satisfaction_var.get(),
            "purchasing_factors": purchase_factors_var.get(),
            "monthly_spending": spending_var.get(),
            "shopping_preference": shopping_preference_var.get(),
            "confidence_frequency": confidence_var.get(),
            "personal_style_goal": style_goal_var.get(),
        }

        # Insert survey responses into the database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Prachi@0102",
            database="survey_db"
        )
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO survey_responses 
                          (age_group, gender, style, shopping_frequency, clothing_colors, favorite_outfit_elements, 
                           satisfaction, purchasing_factors, monthly_spending, shopping_preference, most_worn_clothing,
                           confidence_frequency, personal_style_goal)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (responses["age_group"], responses["gender"], responses["style"], 
                        responses["shopping_frequency"], responses["clothing_colors"], responses["favorite_outfit_elements"], 
                        responses["most_worn_clothing"],responses["satisfaction"], responses["purchasing_factors"], 
                        responses["monthly_spending"], responses["shopping_preference"], responses["confidence_frequency"], 
                        responses["personal_style_goal"]))

        conn.commit()
        conn.close()

        # Update the user to indicate they've completed the survey
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Prachi@0102",
            database="survey_db"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET survey_filled = TRUE WHERE id = %s", (user_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Thank you for completing the survey!")
        survey_window.destroy()  # Close the survey window

    # Submit Button
    tk.Button(scrollable_frame, text="Submit Survey", command=submit_survey, bg="green", fg="white", font=("Arial", 12)).pack(pady=20)


# Main Login Window
def open_login_page():
    global root, username_entry_login, password_entry_login
    root = tk.Tk()  # Create the root window
    root.title("Login")
    root.geometry("400x300")

    tk.Label(root, text="Login", font=("Arial", 16, "bold")).pack(pady=20)
    
    # Username
    tk.Label(root, text="Username:", font=("Arial", 12)).pack(anchor="w", padx=20)
    username_entry_login = tk.Entry(root, font=("Arial", 12))
    username_entry_login.pack(pady=5, padx=20)
    
    # Password
    tk.Label(root, text="Password:", font=("Arial", 12)).pack(anchor="w", padx=20)
    password_entry_login = tk.Entry(root, show="*", font=("Arial", 12))
    password_entry_login.pack(pady=5, padx=20)

    # Login Button
    tk.Button(root, text="Login", command=login, bg="blue", fg="white", font=("Arial", 12)).pack(pady=20)

    # Register Button
    tk.Button(root, text="Register", command=open_register_page, bg="orange", fg="white", font=("Arial", 12)).pack(pady=10)

    root.mainloop()

# Run the setup and login page
setup_database()
open_login_page()
