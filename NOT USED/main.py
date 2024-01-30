import webbrowser
from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

template = """
<!doctype html>
<html>
    <head>
        <title>LED Blink</title>
        <style>
            #led {
                width: 100px;
                height: 100px;
                border-radius: 50%;
            }
        </style>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>
            $(document).ready(function(){
                setInterval(function(){
                    $.get("/state", function(data, status){
                        document.getElementById('led').style.backgroundColor = data.color;
                        document.getElementById('state').innerHTML = "LED is " + data.state;
                    });
                }, 1000);
            });
        </script>
    </head>
    <body>
        <div id="led"></div>
        <p id="state"></p>
    </body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(template)

@app.route('/state')
def state():
    second = datetime.now().second
    if second % 2 == 0:
        return {'color': 'red', 'state': 'ON'}
    else:
        return {'color': 'black', 'state': 'OFF'}


if __name__ == '__main__':
    webbrowser.open("http://localhost:5001")
    app.run(debug=True,port=5001)
