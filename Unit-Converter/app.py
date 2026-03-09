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
    
@app.route("/convert", methods=["get"])
def convert():
    pass    


if __name__ == "__main__":
    app.run(debug=True)
