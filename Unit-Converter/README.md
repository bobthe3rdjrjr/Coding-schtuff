# Unit Converter
Unit converter is a program that uses python, html, & flask to run an html app that you can use to return various length, weight, and temperature units.  

## Requirements: 
blinker - 1.9.0        
click - 8.3.1         
colorama - 0.4.6   
Flask - 3.1.3    
itsdangerous - 2.2.0     
Jinja2 - 3.1.6       
MarkupSafe - 3.0.3       
Python - 3.14        
Werkzeug - 3.1.6

## Installing 
1. First clone this repo:
    * In your chosen folder, run: git clone https://github.com/bobthe3rdjrjr/Coding-schtuff.git
    * Then: cd Coding-schtuff
    
2. Install Dependencies
    * (listed under requirements, just installing flask and python should be fine as flask installs the rest as dependencies)

3. Run it 
    * Run: python app.py 

4. Open it
    * Open the localhost linked in terminal 
    * (Typically http://localhost:5000)


### Running Backend by itself
If you wish to run the backend by itself, you'll need to run it in terminal.

1. First clone this repo:
    * In your chosen folder, run: git clone https://github.com/bobthe3rdjrjr/Coding-schtuff.git
    * Then: cd Coding-schtuff

2. Install Dependencies
    * You only need to install python from the official website

3. Run:
    * python unit_converter_backend.py <base_unit>, <base_amt>, <conversion_unit>
    * Explanation
        * base_unit is the unit you are converting from 
        * base_amt is the amount of that unit
        * conversion_unit is the unit you are converting to 

    * Errors
    