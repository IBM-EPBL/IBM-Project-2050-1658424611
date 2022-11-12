from flask import Flask,render_template,request
import pickle
import numpy as np

model=pickle.load(open('CKDmodel.pkl','rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict_satisfaction():
    v1=float(request.form.get('sg'))
    v2=int(request.form.get('su'))
    v3=int(request.form.get('ab'))
    v4=float(request.form.get('pot'))
    v5=float(request.form.get('hemo'))
    v6=int(request.form.get('pcv'))
    v7=request.form.get('ap')
    v7 = 0 if 'Good' else 1
    v8=request.form.get('ht')
    v8 = 0 if 'No' else 1
    v9=request.form.get('dm')
    v9=0 if 'No' else 1
    v10=request.form.get('ae')
    v10=0 if 'No' else 1
    name=request.form.get('name')
    #prediction
    result=model.predict(np.array([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10]).reshape(1,10))
    d={0:"Negative",1:"Positive"}
    prediction_result=d[result[0]]
    return render_template('report.html',res=prediction_result,pname=name)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)
