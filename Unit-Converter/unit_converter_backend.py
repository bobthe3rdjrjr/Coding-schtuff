# Backend for Unit Converter Mini Project 
import sys

length_units = {
#    Unit: Length(m),    
    "milimeter": 0.001,
    "centimeter": 0.01,
    "meter": 1,
    "kilometer": 1000,
    "inch": 0.0254,
    "foot": 0.3048,
    "yard": 0.9144,
    "mile": 1609.34,
}

weight_units = {
#   Unit: weight(g)
    "miligram": 0.001,
    "gram": 1,
    "kilogram": 1000,
    "ounce": 28.3495,
    "pound": 453.592,
}

temperature_units = ["kelvin", "celsius", "fahrenheit"]

temperature_unit_formulas = {
#   "Unit"to"Unit": formula for unit to unit (t for temp) returns converted temperature
    "CtoF": lambda t : (t * 9/5) + 32,
    "FtoC": lambda t : (t - 32) * 5/9,
    "KtoC": lambda t : t - 273.15,
    "CtoK": lambda t : t + 273.15,
    "FtoK": lambda t : (t + 459.67) * 5/9,
    "KtoF": lambda t : (t * 9/5) - 459.67,
}

def Commandline_args():
    # Take in command line arguments
    argv = sys.argv
    if len(argv) != 4:
        raise TypeError(f"Usage: python unit_converter_backend.py <base_unit> <base_amt> <conversion_unit>")

    base_unit = argv[1].lower()
    conversion_unit = argv[3].lower()

    try:
        base_amt = float(argv[2])

    except ValueError:
        raise ValueError("base_amt is not a valid float:", base_amt)
    

    if not(
    base_unit not in length_units or
    base_unit not in weight_units or 
    base_unit not in temperature_units
    ):
        raise ValueError(f"First argument {base_unit} is neither a length, weight, or temperature.")

    elif not(
    conversion_unit not in length_units or
    conversion_unit not in weight_units or 
    conversion_unit not in temperature_units
    ):
        raise ValueError(f"Third argument {conversion_unit} is neither a length, weight, or temperature.")
    
    return base_unit, base_amt, conversion_unit,


def ConvertUnit(base_unit, base_amt, conversion_unit):
    # Convert unit based on predefined dictionaries
    new_unit = 0
    if base_unit in length_units:
        new_unit = (length_units.get(base_unit) * base_amt) / length_units.get(conversion_unit)

    elif base_unit in weight_units:
        new_unit = (weight_units.get(base_unit) * base_amt) / weight_units.get(conversion_unit)
        
    else:
        formula = temperature_unit_formulas.get(f"{base_unit[0].capitalize()}to{conversion_unit[0].capitalize()}")
        if not formula:
            raise KeyError(f"Couldn't find formula using .get(), key used: {f"{base_unit[0].capitalize()}to{conversion_unit[0].capitalize()}"}")

        new_unit = formula(base_amt)

    return new_unit

if __name__ == '__main__':
    base_unit, base_amt, conversion_unit = Commandline_args()
    result = ConvertUnit(base_unit, base_amt, conversion_unit)
    print(result, conversion_unit)