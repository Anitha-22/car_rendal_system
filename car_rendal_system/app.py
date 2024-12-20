from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Booking and Contact Excel Paths
booking_file = "booking_details.xlsx"
contact_file = "contact_details.xlsx"

# Routes
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/explore')
def explore():
    return render_template("explore.html")

@app.route('/services')
def services():
    return render_template("services.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # Save to Excel
        data = {"Name": [name], "Email": [email], "Message": [message]}
        if not os.path.exists(contact_file):
            df = pd.DataFrame(data)
            df.to_excel(contact_file, index=False)
        else:
            df = pd.read_excel(contact_file)
            new_data = pd.DataFrame(data)
            updated_df = pd.concat([df, new_data])
            updated_df.to_excel(contact_file, index=False)
        flash("Thank you for reaching out! We will get back to you soon.")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route('/book', methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        car_model = request.form["car"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Save to Excel
        data = {
            "Name": [name],
            "Email": [email],
            "Car Model": [car_model],
            "Start Date": [start_date],
            "End Date": [end_date],
        }
        if not os.path.exists(booking_file):
            df = pd.DataFrame(data)
            df.to_excel(booking_file, index=False)
        else:
            df = pd.read_excel(booking_file)
            new_data = pd.DataFrame(data)
            updated_df = pd.concat([df, new_data])
            updated_df.to_excel(booking_file, index=False)

        flash(f"Successfully booked {car_model} from {start_date} to {end_date}.")
        return redirect(url_for("home"))

    return render_template("booking.html")

if __name__ == "__main__":
    app.run(debug=True)
