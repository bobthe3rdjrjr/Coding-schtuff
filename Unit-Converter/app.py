from flask import Flask, render_template, request
from unit_validity_check import validity_check
from unit_converter_backend import ConvertUnit

# Defining routes
app = Flask(__name__)


unit_options = {
    "length": ["milimeter", "centimeter", "meter", "kliometer", "inch", "foot", "yard", "mile"],
    "weight": ["miligram", "gram", "kilogram", "ounce", "pound"],
    "temperature": ["celsius", "fahrenheit", "kelvin"],
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
    error_num = 0
    if len(request.args) != 4:
        raise Exception("lil bro why are you here???:", request.args, len(request.args))
    
    else:
        correct_unit = request.args.get("correct_unit")
        base_unit = request.args.get("base_unit")
        base_amt = request.args.get("base_amt")
        conversion_unit = request.args.get("conversion_unit")
        
        valid = validity_check(correct_unit, base_unit, base_amt, conversion_unit)
        if valid != 0:
            error_num = 1
            return render_template("converter.html", error_num=error_num)

        new_unit = ConvertUnit(base_unit, int(base_amt), conversion_unit)

        return render_template("converter.html", new_unit=new_unit)
        
    
    



if __name__ == "__main__":
    app.run(debug=True)
