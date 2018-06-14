from flask import Flask, jsonify, render_templates
app = Flask(_name_)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pie")
def bioDiversity():
    labels, values = zip(*XXX.items())
    data = [{
        "labels": labels,
        "values": values,
        "type": "pie"}]

    return jsonify (data)

if _name_ == "_main_":
    app.run(debug=True)     