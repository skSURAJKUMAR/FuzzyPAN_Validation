from flask import Flask, render_template, request, jsonify
import requests
from fuzzywuzzy import fuzz
import json
URL=r"https://panuatapi.sudlife.in/api/PanValidation/PANValidate"
dummy={
                "Pan_Number": "",
                "Application_Number": "00000000",
                "Application_Name": "",
                "FName": "",
                "LName": "",
                "Login_Name": "x",
                "RequestType": "2"
            }
app = Flask(__name__)
@app.route("/")
def home():
    return "Hi SURAJ KUMAR, This is PAN Validation API in IIS"

@app.route("/PanValidationWeb")
def index():
    return render_template('index.html')


def PanWEB(Pan_Number,Fname,Lname,Application_Name):
    try:
        dummy["Pan_Number"]=Pan_Number
        dummy["FName"]=Fname
        dummy["LName"]=Lname
        dummy["Application_Name"]=Application_Name
        dataa= json.dumps(dummy)
        print("REQUEST: "+str(dataa))
        headers = {
                'Content-Type': 'application/json',
            }
        r=requests.post(URL,data=dataa,headers=headers)
        response= r.json()        
        print("RESPONSE: "+str(response)+"\n")
        # return response
        print(response['NSDL_Response'])
        fname=response['NSDL_Response'].split("^")[4]
        mname=response['NSDL_Response'].split("^")[5]
        lname=response['NSDL_Response'].split("^")[3]
        if(mname!=""):
            Fullname=fname+" "+mname+" "+lname
        else:
            Fullname=fname+" "+lname
        # remarks=""
        # Fullname=response['NSDL_Response'].split("^")[4]+" "+response['NSDL_Response'].split("^")[5]+" "+response['NSDL_Response'].split("^")[3]
        weightage= fuzz.token_sort_ratio(Fullname,Fname+" "+Lname)
        AadharLink_Status=response['NSDL_Response'].split("^")[9]
        if(weightage==0):
            remarks="Invalid PAN -->FAIL"
        elif(weightage>0 and weightage<75):
            remarks="FAIL"
        elif(weightage>=75):
            remarks="PASS"
        ress=jsonify(Remarks=remarks ,
                    Weightage=weightage,
                    PAN_Name=Fullname,
                    AadharLink_Status=AadharLink_Status
                        )
        print(ress)
        return ress.json
    except Exception as e:
        ress=jsonify(Remarks=str(e),
                        Weightage=0,
                        PAN_Name="",
                        AadharLink_Status="")
        print(ress)
        return ress

@app.route('/PanValidation',methods=['GET','POST'])
def process():
    data = request.json
    # print(data)
    PAN_No=data["Pan_Number"]
    FName=data["FName"]
    LName=data["LName"]
    Application_Name=data["Application_Name"]
    response=PanWEB(PAN_No,FName,LName,Application_Name)
    return response

inputs = []
@app.route('/PanValidationWebValidate', methods=['GET', 'POST'])
def PanValidationWebValidate():
    if request.method == 'POST':
        try:
            dummy["Pan_Number"]=request.json['panNumber']
            dummy["FName"]=request.json['fName']
            dummy["LName"]=request.json['lName']
            dataa= json.dumps(dummy)
            print("REQUEST: "+str(dataa))
            headers = {
                    'Content-Type': 'application/json',
                }
            r=requests.post(URL,data=dataa,headers=headers)
            response= r.json()       
            Result=response['Result'] 
            print("RESPONSE: "+str(response)+"\n")
            # return response
            print(response['NSDL_Response'])
            fname=response['NSDL_Response'].split("^")[4]
            mname=response['NSDL_Response'].split("^")[5]
            lname=response['NSDL_Response'].split("^")[3]
            if(mname!=""):
                Fullname=fname+" "+mname+" "+lname
            else:
                Fullname=fname+" "+lname
            # remarks=""
            # Fullname=response['NSDL_Response'].split("^")[4]+" "+response['NSDL_Response'].split("^")[5]+" "+response['NSDL_Response'].split("^")[3]
            weightage= fuzz.token_sort_ratio(Fullname,request.json['fName']+" "+request.json['lName'])
            
            AadharLink_Status=response['NSDL_Response'].split("^")[9]
            if(weightage==0):
                remarks="Invalid PAN -->FAIL"
            elif(weightage>0 and weightage<75):
                remarks="FAIL"
            elif(weightage>=75):
                remarks="PASS"
            responseData=jsonify(Remarks=remarks ,
                        Weightage=weightage,
                        PAN_Name=Fullname,
                        AadharLink_Status=AadharLink_Status
                            )
        except Exception as e:
            # if(str(e)=="'NoneType' object has no attribute 'split'"):
            #     resresponseData=jsonify(Remarks=Result,
            #                 Weightage=0,
            #                 PAN_Name="",
            #                 AadharLink_Status="")
            responseData=jsonify(Remarks=str(e),
                            Weightage=0,
                            PAN_Name="",
                            AadharLink_Status="")
        print("bdshvcdhbvfbdhjbvcdsdc"+str(responseData))
        return responseData
    #     return render_template('index.html', inputs=ress)
    # return render_template('index.html', inputs=None)

if __name__ == '__main__':
    app.run(debug=True)


# def PanValidation(PAN_No,FName,LName):
#     try:
#         app.app_context()
#         dummy={
#                 "Pan_Number": "",
#                 "Application_Number": "00000000",
#                 "Application_Name": "x",
#                 "FName": "",
#                 "LName": "",
#                 "Login_Name": "x",
#                 "RequestType": "2"
#             }
#         URL=r"https://panuatapi.sudlife.in/api/PanValidation/PANValidate"
#         # data = request.json
#         # print(data)
#         dummy["Pan_Number"]=PAN_No
#         dummy["FName"]=FName
#         dummy["LName"]=LName
#         r=requests.post(URL,data=dummy)
#         response=r.json()
#         print(response['NSDL_Response'])
#         fname=response['NSDL_Response'].split("^")[4]
#         mname=response['NSDL_Response'].split("^")[5]
#         lname=response['NSDL_Response'].split("^")[3]
#         if(mname!=""):
#             Fullname=fname+" "+mname+" "+lname
#         else:
#             Fullname=fname+" "+lname
#         # remarks=""
#         # Fullname=response['NSDL_Response'].split("^")[4]+" "+response['NSDL_Response'].split("^")[5]+" "+response['NSDL_Response'].split("^")[3]
#         weightage= fuzz.token_sort_ratio(Fullname,FName+" "+LName)
#         AadharLink_Status=response['NSDL_Response'].split("^")[9]
#         if(weightage==0):
#             remarks="Invalid PAN -->FAIL"
#         elif(weightage>0 and weightage<75):
#             remarks="FAIL"
#         elif(weightage>=75):
#             remarks="PASS"
#         return jsonify(Remarks=remarks ,
#                     Weightage=weightage,
#                     PAN_Name=Fullname,
#                     AadharLink_Status=AadharLink_Status
#                         )
#     except Exception as e:
#         return jsonify(Remarks=str(e),
#                        Weightage=0,
#                        PAN_Name="",
#                        AadharLink_Status="")




