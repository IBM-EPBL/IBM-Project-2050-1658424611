from flask import Flask,render_template,request
#import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "v6zXMCaTXBv8fJlMVEucGxo5uWRpDfXWGxqBpPn2P_Xy"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#model=pickle.load(open('CKDmodel.pkl','rb'))
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

    total = [[v1,v3,v2,v4,v5,v6,v8,v9,v7,v10]]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [["sg", "ab","su", "pot", "hemo", "pcv", "ht", "dm","ap", "ae"]],
                                       "values": total}]}
    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2abfa46a-b72d-4d9c-8165-8a20f83abe0d/predictions?version=2022-11-20',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    d = {0: "Negative", 1: "Positive"}
    pred=response_scoring.json()
    res=pred['predictions'][0]['values'][0][0]
    print(d[int(res)])
    return render_template('report.html', res=d[int(res)], pname=name)
    '''
    #prediction
    result=model.predict(np.array([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10]).reshape(1,10))
    d={0:"Negative",1:"Positive"}
    prediction_result=d[result[0]]
    return render_template('report.html',res=prediction_result,pname=name)
    '''

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)