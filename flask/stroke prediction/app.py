import pickle
import os
from flask import *

with open(os.getcwd()+'/model/predict', 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)
# Create your views here.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict',  methods=['POST'])
def predict():
    if (request.method == 'POST'):
        print(request.form)
        d = request.form
        age = int(d['age'])
        gender = 1 if d['gender'] == "male" else 0
        cardiac = 1 if d['cardiac'] == "yes" else 0
        marriage = 1 if d['marriage'] == "yes" else 0
        residence = 1 if d['residence'] == "city" else 0
        glucose = int(d['glucose'])
        height = float(d['height'])/100
        weight = int(d['weight'])
        hyper = 1 if d['hyper'] == "yes" else 0
        bmi = float(weight/(height*height))
        if(d['work'] == 'Unemployed'):
            govt = 0
            never = 0
            priva = 0
            selfe = 0
            unem = 1
        elif(d['work'] == 'Private'):
            govt = 0
            never = 0
            priva = 1
            selfe = 0
            unem = 0
        elif(d['work'] == 'SelfEmployed'):
            govt = 0
            never = 0
            priva = 0
            selfe = 1
            unem = 0
        elif(d['work'] == 'Government'):
            govt = 1
            never = 0
            priva = 0
            selfe = 0
            unem = 0
        elif(d['work'] == 'Neverworked'):
            govt = 0
            never = 1
            priva = 0
            selfe = 0
            unem = 0
        if(d['smoke'] == "never"):
            nevers = 1
            form = 0
            smok = 0
        elif(d['smoke'] == "formerly"):
            nevers = 0
            form = 1
            smok = 0
        else:
            nevers = 0
            form = 0
            smok = 1
        children = 1 if d['children'] == "yes" else 0
        print(d)
        row = [[age, hyper, cardiac, glucose, bmi, gender, marriage,
                residence, govt, never, priva, selfe, children, form, nevers, smok]]
        y = model.predict(row)
        print(y)
        if(y == 1):
            return render_template('bad.html', name=d['name'])
        else:
            return render_template('good.html', name=d['name'])


if __name__ == '__main__':
    app.run(debug=True)
