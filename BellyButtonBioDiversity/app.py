# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
# Dependencies
import pandas as pd
import os
import numpy as np
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

from flask_sqlalchemy import SQLAlchemy

# Create engine using the `demographics.sqlite` database file
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
print(Base.classes.keys())

# Assign the dow class to a variable called `Dow`
samples = Base.classes.samples
otu = Base.classes.otu
samples_metadata = Base.classes.samples_metadata

# Create a session
session = Session(engine)

sample_names = samples.__table__.columns.keys()
sample_names.pop(0)

# Display the row's columns and data in dictionary format
# first_row = session.query(samples).first()
# print(first_row.__dict__)

list_of_sample_names =[]
# # Use the session to query Dow table and display the first 5 trade volumes
for row in session.query(samples).all():
    list_of_sample_names.append(row)


list_of_otu_description =[]
# # Use the session to query Dow table and display the first 5 trade volumes
for row in session.query(otu.lowest_taxonomic_unit_found).all():
    list_of_otu_description.append(row[0])


filtered_sample = []
for row in session.query(samples_metadata.AGE, samples_metadata.ETHNICITY,samples_metadata.GENDER, samples_metadata.BBTYPE, samples_metadata.LOCATION, samples_metadata.SAMPLEID).filter(samples_metadata.SAMPLEID == 940).all():
    filtered_dictionary = {
        "AGE": row[0],
        "BBTYPE": row[1],
        "ETHNICITY": row[2],
        "GENDER": row[3],
        "LOCATION": row[4],
        "SAMPLEID": row[5],
              
    }
    filtered_sample.append(filtered_dictionary)
print(filtered_sample)

weekly_WFREQ = []
for row in session.query(samples_metadata.WFREQ).filter(samples_metadata.SAMPLEID == 940).all():
    filtered_WFREQ = {
        "WFREQ": row[0],
         
    }
    weekly_WFREQ.append(filtered_WFREQ)

otu_id_and_sample_values = []
otu_id = []
sample_values = []

otu_id_and_sample_values_dic ={
    "otu_id": otu_id,
    "sample_values":sample_values
}

otu_id_and_sample_values.append(otu_id_and_sample_values_dic)
for row in session.query(samples.otu_id,samples.BB_940).filter(samples_metadata.SAMPLEID == 940).order_by(samples.BB_940.desc()).all():
    otu_id.append(row[0])
    sample_values.append(row[1])


# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def home():
   return render_template("index.html", sample_names= sample_names)
 
@app.route("/names")
def names():
    return jsonify(sample_names)

@app.route("/otu")
def otu():
    return jsonify(list_of_otu_description)

@app.route("/metadata")
def metadata():
    return jsonify(filtered_sample)

@app.route('/wfreq')
def wfreq():
    return jsonify(weekly_WFREQ)

@app.route('/samples')
def samples():
    return jsonify(otu_id_and_sample_values)

#run the app
if __name__ == '__main__':
    app.run(debug=True)