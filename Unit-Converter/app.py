from flask import Flask, render_template, request

# Defining routes
app = Flask(__name__)


unit_options = {
    "length": ["milimeter", "centimeter", "meter", "kliometer", "inch", "foot", "yard", "mile"],
    "weight": ["miligram", "gram", "kilogram", "ounce", "pound"],
    "temperature": ["celisus", "fahrenheit", "kelvin"],
}

@app.route("/")
def home():
    unit = request.args.get("unit")
    return render_template("unit_converter_frontend.html", unit=unit)

@app.route("/converter/<unit>") 
def converter(unit):
    base_unit = request.args.get("base_unit")
    base_amt = request.args.get("base_amt")
    conversion_unit = request.args.get("conversion_unit")
    return render_template("converter.html", base_unit=base_unit, base_amt=base_amt, conversion_unit=conversion_unit, options=unit_options, unit=unit)
    
@app.route("/process", methods=["get"])
def process():
    if len(request.form) == 4:
        correct_unit = request.form.get("correct_unit")
        base_unit = request.form.get("base_unit")
        base_amt = request.form.get("base_amt")
        conversion_unit = request.form.get("conversion_unit")
    else:
        raise ValueError("lil bro why are you here", request.form)
    
    



if __name__ == "__main__":
    app.run(debug=True)
