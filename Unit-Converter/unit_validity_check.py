from unit_converter_backend import length_units, weight_units, temperature_units

def validity_check(correct_unit, base_unit, base_amt, conversion_unit):
    # Check correct_unit
    if correct_unit == "length":
        correct_unit == length_units
    elif correct_unit == "weight":
        correct_unit = weight_units
    elif correct_unit == "temperature":
        correct_unit = temperature_units
    else:
        return 4
    
    # Check base & conversion unit
    if base_unit not in correct_unit:
        return 1
    elif conversion_unit not in correct_unit:
        return 3
    
    # Check base_amt
    try:
        float(base_amt)

    except ValueError:
        return 2
    
    return 0 
