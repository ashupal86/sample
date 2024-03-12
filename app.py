from flask import Flask, render_template

app = Flask(__name__)

head=["Name","Age"]
data1=[
    ("ashu",18),
    ("ASHU",19),
    ("Pradeep",19),
    ("Abhay",19)
]

@app.route('/')
def index():
    return render_template('index.html',heading=head,data=data1)

if __name__ == '__main__':  
    app.run(debug=True)
    