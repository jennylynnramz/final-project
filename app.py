# Dependencies
from flask import Flask, render_template, request, redirect
import pandas as pd
import the_magic
import time
import os


# Create instance of Flask app
app = Flask(__name__)

# Database Setup
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')
# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Connects to the database using the app config
db = SQLAlchemy(app)

from models.py import Input_Results
print(Input_Results)

# Route that renders the welcome page and receives user inputs
@app.route("/", methods=["GET", "POST"])
def user_inputs():
    app.logger.debug('user_inputs() called.')

    if request.method == "POST":
        post_start_time = time.perf_counter()
        app.logger.debug('POST request received.')

        req = request.form

        summer_temp = req["summer-temp"]
        winter_temp = req["winter-temp"]
        city_size = req["city-size"]
        house_size = req["house-size"]
        budget = req["budget"]
        bedrooms = req["bedrooms"]
        bathrooms = req["bathrooms"]
        yard = req["yard"]
        # Array of user inputs
        input_array = [summer_temp, winter_temp, city_size, house_size, budget, bedrooms, bathrooms, yard]
        print(
            f"""
            Form submitted:\n
            Summer Temp: {summer_temp}\n
            Winter Temp: {winter_temp}\n
            City Size: {city_size}\n
            House Size: {house_size}\n
            Budget: {budget}\n
            Bedrooms: {bedrooms}\n
            Bathrooms: {bathrooms}\n
            Yard: {yard}\n 
            """)

        if input_array[2] == "Small Town":
            input_array[2] = 0
        elif input_array[2] == "Medium City":
            input_array[2] = 1
        else:
            input_array[2] = 2

        # Yard Size
        if input_array[7] == "Yes":
            input_array[7] = 1
        else:
            input_array[7] = 0
            
        print(
            f"""
            Hot Coded array:\n
            Summer Temp: {input_array[0]}\n
            Winter Temp: {input_array[1]}\n
            City Size: {input_array[2]}\n
            House Size: {input_array[3]}\n
            Budget: {input_array[4]}\n
            Bedrooms: {input_array[5]}\n
            Bathrooms: {input_array[6]}\n
            Yard: {input_array[7]}\n 
            """)

        
        get_table_data = the_magic.make_prediction(input_array)
        mytable = get_table_data.to_html(classes="results table table-striped")
        
        # TIMER TO TRACK EFFICIENCY
        post_end_time = time.perf_counter()
        time_spent_processing_post_request = post_end_time - post_start_time
        app.logger.debug("Spent " + str(time_spent_processing_post_request) + " seconds processing POST.")

        # DATABASE
        input_results = Input_Results(user_input=input_array, results=mytable)
        db.session.add(input_results)
        db.session.commit()


        return render_template('display_results.html',  table=mytable , titles=get_table_data.columns.values)
        
       
    return render_template("index.html")


    
    
#     return render_template('simple.html',  tables=[results_df.to_html(classes="results")], titles=results_df.columns.values)

if __name__ == "__main__":
    app.run(debug=True)