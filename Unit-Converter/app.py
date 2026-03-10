from flask import Flask, render_template, request

# Defining routes
app = Flask(__name__)

@app.route("/")
def home():
    unit = request.args.get("unit")
    return render_template("unit_converter_frontend.html", unit=unit)

@app.route("/length") 
def length():
    base_unit = request.args.get("base_unit")
    base_amt = request.args.get("base_amt")
    conversion_unit = request.args.get("conversion_unit")
    return render_template("length.html", base_unit=base_unit, base_amt=base_amt, conversion_unit=conversion_unit)
    
@app.route("/weight") 
def weight():
    base_unit = request.args.get("base_unit")
    base_amt = request.args.get("base_amt")
    conversion_unit = request.args.get("conversion_unit")
    return render_template("weight.html", base_unit=base_unit, base_amt=base_amt, conversion_unit=conversion_unit)
    
@app.route("/temperature") 
def temperature():
    base_unit = request.args.get("base_unit")
    base_amt = request.args.get("base_amt")
    conversion_unit = request.args.get("conversion_unit")
    return render_template("temperature.html", base_unit=base_unit, base_amt=base_amt, conversion_unit=conversion_unit)
    
@app.route("/process", methods=["get"])
def process():
    if len(request.form) == 1:
        correct_unit = request.form.get("correct_unit")
    elif len(request.form) == 3:
        base_unit = request.form.get("base_unit")
        base_amt = request.form.get("base_amt")
        conversion_unit = request.form.get("conversion_unit")
    else:
        raise ValueError("PANIC")


if __name__ == "__main__":
    app.run(debug=True)
