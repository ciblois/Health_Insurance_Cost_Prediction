from flask import Flask, render_template, request
# to initialize a flask app we need untitled:Untitled-2 to run a specific command
import numpy as np
import pandas as pd
import pickle

# we are just telling Python that from here downwards we have a flask app
application = app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

#with open("model.pkl","rb") as f:
#    model = pickle.load(f)
    
# we have to define the different routes that our app has

# when we define a route we have to state the route path

@application.route('/', methods = ['POST','GET'])

#def home():
#    return render_template('main.html')
    
#@app.route('/predict', methods = ['POST','GET'])

# within each route we have to code what python logic 
#must be executed when the route is called

def predict():
    '''
    For rendering results on HTML GUI
    '''
    # this line of code is storing in a variable
    # what the user inputed 

    user_dict = {'age':0, 'bmi':0, 'children':0, 'sex_female':0, 'sex_male':0, 'smoker_No':0,'smoker_Yes':0, 'region_northeast':0, 'region_northwest':0, 'region_southeast':0, 'region_southwest':0}

    if request.method == 'POST':
        if request.form['smoker'] == 'Yes':
            user_dict['smoker_No'] = 0
            user_dict['smoker_Yes'] = 1
        else:
            user_dict['smoker_No'] = 1
            user_dict['smoker_Yes'] = 0

        if request.form['sex']=='Female':
            user_dict['sex_female'] = 1
            user_dict['sex_male'] = 0
        else:
            user_dict['sex_female'] = 0
            user_dict['sex_male'] = 1

        if request.form['region']=='region_northeast':
            user_dict['region_northeast'] = 1
            user_dict['region_northwest'] = 0
            user_dict['region_southeast'] = 0
            user_dict['region_southwest'] = 0
        elif request.form['region']=='region_northwest':
            user_dict['region_northeast'] = 0
            user_dict['region_northwest'] = 1
            user_dict['region_southeast'] = 0
            user_dict['region_southwest'] = 0
        elif request.form['region']=='region_southeast':
            user_dict['region_northeast'] = 0
            user_dict['region_northwest'] = 0
            user_dict['region_southeast'] = 1
            user_dict['region_southwest'] = 0
        else:
            user_dict['region_northeast'] = 0
            user_dict['region_northwest'] = 0
            user_dict['region_southeast'] = 0
            user_dict['region_southwest'] = 1

        user_dict['age'] = request.form['age']
        user_dict['bmi'] = request.form['bmi']
        user_dict['children'] = request.form['children']

        prediction = pd.DataFrame.from_dict(user_dict.values()).T
        price = model.predict(prediction)

        output = round(price[0],2)
        return render_template('main.html', result = 'The predicted charges is ${0}'.format(output))

    else:
        return render_template('main.html')

if __name__ == "__main__":
    app.run(debug = True)