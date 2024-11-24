from flask import Flask
from flask import redirect,url_for,render_template, request, flash,session,jsonify,send_file,send_from_directory
import json, requests
from datetime import datetime,date, timedelta
from werkzeug.utils import secure_filename
import os
from urllib.parse import urlparse
from pathlib import Path

app = Flask(__name__)

app.config["SECRET_KEY"]='3e15976f74727374875a04f995324cc214fa3723ded4d9fee5ab6dc4d35e5206'

"doctor app url: doctors.inticure.com"

base_url = "https://api.inticure.online/"
app.permanent_session_lifetime = timedelta(days=90)

# api urls
admin_login_api="api/administrator/sign_in"
appointment_list_api="api/doctor/appointment_list"
appointment_detail_api="api/doctor/appointment_detail"
follow_up_api="api/analysis/followup_booking"
# prescription file upload api
prescription_api="api/doctor/prescriptions"
prescription_text_api="api/doctor/prescriptions_text"
prescription_edit_api="api/doctor/prescriptions_text_viewset/"
delete_prescription_api="api/doctor/prescriptions_text_viewset/"
analysis_text_api="api/doctor/analysis_info"
file_upload_api="api/doctor/common_file/"
# add observation api
observations_api="api/doctor/observations"
edit_observation_api="api/doctor/observations_viewset/"
delete_observation_api="api/doctor/observations_viewset/"
customer_edit_api="api/customer/customer_crud"
customer_list_api="api/customer/customer_crud"
doctor_listing_api="api/administrator/doc_list"
escalate_api="api/doctor/escalate_appointment"
order_accept_api="api/doctor/order_accept"
specialization_filter_api="api/doctor/doctor_specialization"
payout_list_api="api/administrator/payout_list"
dashboard_api="api/doctor/doctor_dashboard"
invoice_detail_api="api/analysis/invoice_detail"
invoice_list_api="api/analysis/invoice_list"
logout_api="api/administrator/logout"
doctor_profile_api="api/doctor/doctor_profile"
language_api="api/administrator/languages_viewset"
specialization_list_api="api/doctor/specialization_list"
add_doctor_api="api/administrator/doc_create"
doctor_update_api="api/administrator/doctor_profile_edit"
transfer_api="api/doctor/senior_doctor_transfer"
junior_doctor_transfer_api="api/doctor/junior_doctor_transfer"
report_customer_api="api/administrator/report_customer"

# jr doc time slots api
time_slot_api="api/doctor/available_slots"
# senior doc time slots api
senior_timeslot_api="api/doctor/specialization_time_slot"

create_followup_reminder_api="api/doctor/create_followup_reminder"
followup_reminder_list_api="api/doctor/followup_reminder_list"
discussion_list_api="api/doctor/discussion_list"
create_discussion_api="api/doctor/create_discussion"
# working hours and calendar apis
working_hours_api="api/doctor/working_hours"
working_hours_list_api="api/doctor/working_hours_list"
time_slot_list_api="api/doctor/time_slot_list"
calendar_view_api="api/doctor/calender_view"
calendar_edit_api="api/doctor/calender_edit"
calendar_add_api="api/doctor/calender_add"

add_rating_api="api/customer/appointment_ratings"
change_password_api="api/administrator/password_change"
forgot_password_api="api/administrator/forgot_password"
sign_in_otp_api="api/administrator/sign_in_otp"
reschedule_api="api/doctor/appointment_schedule"
patient_history_api="/api/doctor/appointment_patient_history"
locations_api="api/administrator/locations_viewset"
complete_api="api/doctor/   d"


# """"""" BASE DIRECTORY """"""""
BASE_DIR = Path(__file__).resolve().parent

# app.config['UPLOAD_FOLDER'] = 'static/files'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.template_filter('datetime')
# def date_format(value):
#     months = ('Enero','Febrero',"Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre")
#     month = months[value.month-1]
#     hora = str(value.hour).zfill(2)
#     minutos = str(value.minute).zfill(2)
#     return "{} de {} del {} a las {}:{}hs".format(value.day, month, value.year)
    # return "{} de {} del {} a las {}:{}hs".format(value.day, month, value.year, hora, minutos)


# # # ------- Template Filter ------- # # #

@app.template_filter()
def date_format(date_string):
    # here date string (format:yyyy-mm-dd) from api is converted first to datetime object then to desired date string format
    
    try:
        date_object=datetime.strptime(date_string,f'%Y-%m-%d')
        formatted_string = date_object.strftime('%d %b %Y')
        return formatted_string
    except:
        pass

@app.template_filter()
def time_format(value):
    # dtm_obj = datetime.strptime(timing, f'%Y-%m-%dT%H:%M:%S.%f%z')
    # here date string object from api is converted to datetime or time object 
    date_object=datetime.strptime(value,f'%H:%M:%S.%f')
    # datetime object is converted to date string format:HH:MM AM/PM , %p for AM/PM %I for 12 hr time 
    formatted_string = date_object.strftime('%I:%M %p')
    return formatted_string

# this filter is for splitting time slot to the first value (Eg 10AM - 11AM to 10AM)
@app.template_filter()
def time_slot_format(value):
    try:
        time_strip=value.split("-")
        time=str(time_strip[0])
        return time
    except:
        pass
# # # ---------- Views ---------- # # #

def get_country(ip_address):
    try:
        response = requests.get("http://ip-api.com/json/{}".format(ip_address))
        js = response.json()
        country = js['countryCode']
        return country
    except Exception as e:
        print(e)
        return "Unknown"

@app.route("/",methods=['POST','GET'])
def login_phone():
    print('login')
    session.clear()
    try:
        headers = {
                "Content-Type":"application/json"
            }
        # fetching location
        ip_address = request.remote_addr
        country = get_country(ip_address)
        print("country",country)
        session['country']=country
        if country in ('IN','IND'):
            print("phone login")
            if request.method == 'POST':
                mobile_num=request.form['phone']
                session['mobile_num']=mobile_num
                print(mobile_num)
                # "Dr Kiran"
                if mobile_num == '8945623416':
                    print("kiran")
                    return redirect(url_for('phone_otp'))
                # "Dr Srikesh"
                if mobile_num == '7886532112':
                    print("srikesh")
                    return redirect(url_for('phone_otp'))
                data={
                    "mobile_num":mobile_num

                }
                api_data=json.dumps(data)
                otp_req=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)
                print(otp_req.status_code)
                otp_generate=json.loads(otp_req.text)
                print(otp_generate)
                if otp_generate['response_code']==200:
                    return redirect(url_for('phone_otp'))
                else:
                    flash("Invalid phone number","error")
                    return redirect(url_for('login_phone'))
        else:
            return redirect(url_for('login'))
        return render_template("sign_in_phone.html")
    except Exception as e:
        print(e)
        flash("something went wrong","error")
        return render_template("sign_in_phone.html")
    return render_template("sign_in_phone.html")

@app.route("/phone_otp",methods=['POST','GET'])
def phone_otp():
    try:
        headers = {
                "Content-Type":"application/json"
            }
        if 'mobile_num' in session:
            mobile_num=session['mobile_num']

            

        if request.method == 'POST':

            # "" Dr Kiran Kumar ""
            if mobile_num == '8945623416':
                print("mobile")
                if request.form['otp'] == '8480':
                    print("otp correct")
                    otp = 8480
                else :
                    print("wrong otp")
                    flash("Wrong otp","error")
                    return redirect(url_for('phone_otp'))
                otp = 8480
                doctor_flag = 2
                session['doctor_flag']=doctor_flag
                user_id=42
                session['user_id']=user_id
                # calling doc profile api
                payload={
                        "doctor_id":user_id
                    }
                                    
                api_data=json.dumps(payload)
                doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                print(doctor_profile_request)
                doctor_profile_response=json.loads(doctor_profile_request.text)
                print(doctor_profile_response,'   line 227')
                doctor_profile1=doctor_profile_response['data1']
                doctor_profile2=doctor_profile_response['data2']
                language=doctor_profile2['language_known']
                doctor_first_name = doctor_profile1['first_name']
                session['doctor_first_name'] = doctor_first_name
                doctor_last_name = doctor_profile1['last_name']
                session['doctor_last_name'] = doctor_last_name
                doctor_email = doctor_profile1['email']
                session['doctor_email'] = doctor_email
                print(doctor_first_name,doctor_last_name,doctor_email)
                profile_pic=doctor_profile2['profile_pic']
                session['profile_pic'] = profile_pic
                signature=doctor_profile2['signature']
                session['signature'] = signature
                session.permanent = True
                return redirect(url_for("dashboard"))

            # "" Dr Srikesh Lal""
            if mobile_num == '7886532112':
                if request.form['otp'] == '8480':
                    print("otp correct")
                    otp = 8480
                else :
                    print("wrong otp")
                    flash("Wrong otp","error")
                    return redirect(url_for('phone_otp'))
                doctor_flag = 1
                session['doctor_flag']=doctor_flag
                user_id=39
                session['user_id']=user_id
                # calling doc profile api
                payload={
                        "doctor_id":user_id
                    }
                                    
                api_data=json.dumps(payload)
                doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                doctor_profile_response=json.loads(doctor_profile_request.text)
                doctor_profile1=doctor_profile_response['data1']
                doctor_profile2=doctor_profile_response['data2']
                language=doctor_profile2['language_known']
                doctor_first_name = doctor_profile1['first_name']
                session['doctor_first_name'] = doctor_first_name
                doctor_last_name = doctor_profile1['last_name']
                session['doctor_last_name'] = doctor_last_name
                doctor_email = doctor_profile1['email']
                session['doctor_email'] = doctor_email
                print(doctor_first_name,doctor_last_name,doctor_email)
                profile_pic=doctor_profile2['profile_pic']
                session['profile_pic'] = profile_pic
                signature=doctor_profile2['signature']
                session['signature'] = signature
                return redirect(url_for("dashboard"))    

            # "" All Doctors ""
            # login for all other jr and snr doctors
            if request.form['form_type']=="next":

                otp=request.form['otp']
                # otp=request.form['otp']
                data={
                        "mobile_num":mobile_num,
                        "otp":otp

                    }
                api_data=json.dumps(data)
                otp_req=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)
                print(otp_req.status_code)
                otp_generate=json.loads(otp_req.text)
                print(otp_generate)
                # flash("Invalid OTP","error")
                if otp_req.status_code == 200:
                #storing doctor flag key from login response in doctor flag variable
                    doctor_flag=otp_generate['doctor_flag']
                    #storing doctor flag variable as doctor flag key in session
                    session['doctor_flag']=doctor_flag
                    print("doc",doctor_flag)
                    # if doctor_flag == 0:

                    #storing user id in session 
                    user_id=otp_generate['user_id']
                    session['user_id']=user_id
                    print("user id",user_id)

                    # gender=otp_generate['gender']
                    # session['gender']=gender
                    # print("gender",gender)

                    # languages_known=otp_generate['languages_known']
                    # session['languages_known']=languages_known
                    # print("languages_known",languages_known)
                # if admin_login_response.status_code == 200:
                    print("200")
                    payload={
                            "doctor_id":user_id
                        }
                        
                        
                    api_data=json.dumps(payload)
                    doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                    doctor_profile_response=json.loads(doctor_profile_request.text)
                    doctor_profile1=doctor_profile_response['data1']
                    doctor_profile2=doctor_profile_response['data2']
                    language=doctor_profile2['language_known']
                    doctor_first_name = doctor_profile1['first_name']
                    session['doctor_first_name'] = doctor_first_name
                    doctor_last_name = doctor_profile1['last_name']
                    session['doctor_last_name'] = doctor_last_name
                    doctor_email = doctor_profile1['email']
                    session['doctor_email'] = doctor_email
                    print(doctor_first_name,doctor_last_name,doctor_email)
                    profile_pic=doctor_profile2['profile_pic']
                    session['profile_pic'] = profile_pic
                    signature=doctor_profile2['signature']
                    session['signature'] = signature

                    # doctor_listing=requests.post(base_url+doctor_listing_api, headers=headers)
                    # doctor_list_response=json.loads(doctor_listing.text)
                    # print(doctor_listing.status_code)
                    # doctor_list = doctor_list_response['data']
                    # for doctor in doctor_list:
                    #     if doctor['user_id'] == user_id:
                    #         doctor_first_name = doctor['user_fname']
                    #         session['doctor_first_name'] = doctor_first_name
                    #         doctor_last_name = doctor['user_lname']
                    #         session['doctor_last_name'] = doctor_last_name
                    #         doctor_email = doctor['user_mail']
                    #         session['doctor_email'] = doctor_email
                    #         print(doctor_first_name,doctor_last_name,doctor_email)

                    return redirect(url_for("dashboard"))
                else:
                    flash("Incorrect otp","error")
                    return redirect(url_for('phone_otp'))
                    # return redirect(url_for("login_phone"))  

                #   Resend OTP
            if request.form['form_type']=="resend":
                data={
                    "mobile_num":mobile_num

                }
                api_data=json.dumps(data)
                otp_req=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)
                print(otp_req.status_code)
                otp_generate=json.loads(otp_req.text)
                print(otp_generate)
                if otp_generate['response_code']==400:
                    flash("Something went wrong","error")
                    return redirect(url_for('phone_otp'))
                return redirect(url_for('phone_otp'))

        return render_template("sign_in_otp.html")
    except Exception as e:
        print(e)
        flash("Something went wrong","error")
        return render_template("sign_in_otp.html")
        
    return render_template("sign_in_otp.html")

@app.route("/login_from_admin",methods=['GET','POST'])
def login_from_admin():
    headers = {
        "Content-Type":"application/json"
    }
    doctor_email = request.args.get('doctor_email')
    print(doctor_email)
    login_from_admin_request = requests.post('https://api.inticure.online/api/doctor/login_from_admin/',data=json.dumps({"doctor_email":doctor_email}),headers=headers)
    login_from_admin_response = json.loads(login_from_admin_request.text)
    print(login_from_admin_response)
    if login_from_admin_response['response_code'] == 400:
        return redirect(request.referrer)
    session['username'] = doctor_email
    return redirect(url_for('email_otp'))

@app.route("/email_login",methods=['GET','POST'])
def login():
    try:
        admin_login_api="api/administrator/sign_in"
        headers={
            "Content-Type":"application/json"
        }
        if request.method == 'POST':
            print("post")
            username = request.form.get('username')
            session['username']=username
            session.permanent = True
            if username == "kiran@inticure.com":
                print("kiran doc")
                return redirect(url_for('email_otp'))
            if username == "srikesh@inticure.com":
                print("srikesh doc")
                return redirect(url_for('email_otp'))
            # password = request.form.get('password')
            # data={
            #     "username":username,
            #     "password":password,
            #     "login_flag":"doctor"
            # }
            print(username)
            if '@' in username:
                data={
                    "email":username
                }
            else:
                data={
                    "mobile_num":username
                }
            api_data=json.dumps(data)
            print(api_data)
            # admin_login_response=requests.post(base_url+admin_login_api,data=api_data,headers=headers)
            admin_login_response=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)
            print("login",admin_login_response.status_code)
            admin_login=json.loads(admin_login_response.text)
            print(admin_login)
            if 'email' in admin_login:
                session['username'] = admin_login['email']
            if admin_login['response_code']==200:
                return redirect(url_for('email_otp'))
            if admin_login['message'] == "User Banned":
                session.clear()
                flash("User is not allowed to login, Contact our team to continue the journey with us.","warning")
                return redirect(url_for('login'))
            else:
                flash("Invalid email","error")
                session.clear()
                return redirect(url_for('login'))
            # return redirect(url_for('email_otp'))
        return render_template("login.html")
    except Exception as e:
        #printing error
        print(e)
        flash("Server Error","error")
        return render_template('login.html')
    return render_template('login.html')

@app.route("/email_otp",methods=['GET','POST'])
def email_otp():
    try:
        admin_login_api="api/administrator/sign_in"
        headers={
            "Content-Type":"application/json"
        }
        if 'username' in session:
            username=session['username']
            print(username)
        if request.method == 'POST':

            print("post otp")

            # login for jr doc kiran
            if username == "kiran@inticure.com":
                print("dr kiran")
                otp = request.form['otp']
                print("otp",otp)
                if otp == '8480':
                    print("8480")
                    otp = 8480
                else:
                    print("wrong otp")
                    flash("Wrong otp","error")
                    return redirect(url_for('login'))
                otp = '8480'
                doctor_flag = 2
                session['doctor_flag']=doctor_flag
                user_id=42
                session['user_id']=user_id
                # calling doc profile api
                payload={
                        "doctor_id":user_id
                    }
                api_data=json.dumps(payload)
                doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                doctor_profile_response=json.loads(doctor_profile_request.text)
                doctor_profile1=doctor_profile_response['data1']
                doctor_profile2=doctor_profile_response['data2']
                language=doctor_profile2['language_known']
                doctor_first_name = doctor_profile1['first_name']
                session['doctor_first_name'] = doctor_first_name
                doctor_last_name = doctor_profile1['last_name']
                session['doctor_last_name'] = doctor_last_name
                doctor_email = doctor_profile1['email']
                session['doctor_email'] = doctor_email
                print(doctor_first_name,doctor_last_name,doctor_email)
                profile_pic=doctor_profile2['profile_pic']
                session['profile_pic'] = profile_pic
                signature=doctor_profile2['signature']
                session['signature'] = signature
                return redirect(url_for("dashboard"))

                # login for snr doc srikesh
            if username == "srikesh@inticure.com":
                print("dr srikesh")
                otp = request.form['otp']
                print("otp",otp)
                if otp == '8480':
                    print("8480")
                    otp = 8480
                else:
                    print("wrong otp")
                    flash("Wrong otp","error")
                    return redirect(url_for('login'))
                otp = '8480'
                doctor_flag = 1
                session['doctor_flag']=doctor_flag
                user_id=39
                session['user_id']=user_id
                # calling doc profile api
                payload={
                        "doctor_id":user_id
                    }
                    
                api_data=json.dumps(payload)
                doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                doctor_profile_response=json.loads(doctor_profile_request.text)
                doctor_profile1=doctor_profile_response['data1']
                doctor_profile2=doctor_profile_response['data2']
                language=doctor_profile2['language_known']
                doctor_first_name = doctor_profile1['first_name']
                session['doctor_first_name'] = doctor_first_name
                doctor_last_name = doctor_profile1['last_name']
                session['doctor_last_name'] = doctor_last_name
                doctor_email = doctor_profile1['email']
                session['doctor_email'] = doctor_email
                print(doctor_first_name,doctor_last_name,doctor_email)
                profile_pic=doctor_profile2['profile_pic']
                session['profile_pic'] = profile_pic
                signature=doctor_profile2['signature']
                session['signature'] = signature
                return redirect(url_for("dashboard"))

                # login for all other jr and snr doctors
            if request.form['form_type']=="next":
                otp = request.form.get('otp')
                if 'username' in session:
                    username=session['username']
                
                print(username)
                data={
                    "email":username,
                    "otp":otp
                }
                api_data=json.dumps(data)
                print(api_data)
                admin_login_response=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)

                print("login",admin_login_response.status_code)
                admin_login=json.loads(admin_login_response.text)
                print(admin_login)
                if admin_login_response.status_code == 200:
                    doctor_flag=admin_login['doctor_flag']
                    session['doctor_flag']=doctor_flag
                    print("doc",doctor_flag)

                    user_id=admin_login['user_id']
                    session['user_id']=user_id
                    print("user id",user_id)

                    print("200")
                    
                    payload={
                        "doctor_id":user_id
                    }
                    
                    api_data=json.dumps(payload)
                    doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
                    doctor_profile_response=json.loads(doctor_profile_request.text)
                    doctor_profile1=doctor_profile_response['data1']
                    doctor_profile2=doctor_profile_response['data2']
                    language=doctor_profile2['language_known']
                    doctor_first_name = doctor_profile1['first_name']
                    session['doctor_first_name'] = doctor_first_name
                    doctor_last_name = doctor_profile1['last_name']
                    session['doctor_last_name'] = doctor_last_name
                    doctor_email = doctor_profile1['email']
                    session['doctor_email'] = doctor_email
                    print(doctor_first_name,doctor_last_name,doctor_email)
                    profile_pic=doctor_profile2['profile_pic']
                    session['profile_pic'] = profile_pic
                    signature=doctor_profile2['signature']
                    session['signature'] = signature

                    return redirect(url_for("dashboard"))
                else:
                    flash("Invalid Email/OTP","error")
                    return redirect(url_for('email_otp'))

                #Resend otp 
            elif request.form['form_type']=="resend":
                data={
                "email":username
                }
                api_data=json.dumps(data)
                print(api_data)
                # admin_login_response=requests.post(base_url+admin_login_api,data=api_data,headers=headers)
                admin_login_response=requests.post(base_url+sign_in_otp_api, data=api_data, headers=headers)
                print("login",admin_login_response.status_code)
                admin_login=json.loads(admin_login_response.text)
                print(admin_login)
                return redirect(url_for('email_otp'))

        return render_template("login_otp.html")
    except Exception as e:
        #printing error
        print(e)
        flash("Server Error","error")
        return redirect(url_for('login'))
    return render_template('login_otp.html')

@app.route("/logout")
def logout():
    try:
        headers = {
            "Content-Type":"application/json"
        }
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login_phone'))
        payload={
            "user_id":doctor_id
        }
        api_data=json.dumps(payload)
        logout_request=requests.post(base_url+logout_api, data=api_data, headers=headers)
        logout_response=json.loads(logout_request.text)
        print(logout_response)
        session.clear()
        print("session cleared")
        return redirect(url_for('login_phone'))
    except Exception as e:
        print(e)
    return redirect(url_for('login_phone'))

@app.route('/uploads/<filename>')
def upload(filename):
    cwd = os.getcwd()+'/'
    print(cwd)
    if 'temp' not in os.listdir(cwd):
        os.mkdir(cwd + 'temp')
    # address_file.save(os.path.join(cwd + 'temp', filename))
    return send_from_directory(cwd + 'temp', filename)
    # return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route('/user_download/<int:appointment_id>')
def user_download(appointment_id):
    try:
        file_path=request.args.get('file_path')
        print(file_path)
        print("download")
        print(file_path)
        print(appointment_id)
        url=file_path
        # url="http://"+file_path 
        # print(url)
        r = requests.get(url)
        # r = requests.get(url)
        print("error")
        # this removes http and website part from url
        url_split_1 = urlparse(url)
        print(url_split_1)
        #this will split rest of the path from file name
        file_name=os.path.basename(url_split_1.path)
        print("filename",file_name)

        # cwd = os.getcwd()+'/'
        # print(cwd)
        # if 'temp' not in os.listdir(cwd):
        #     os.mkdir(cwd + 'temp')
        # #saving file in flask app
        # file_temp_save=open(cwd + 'temp/'+ file_name, "wb").write(r.content)
        # print("saved in temp")

        print("Base dir: ", BASE_DIR)
        if 'temp' not in os.listdir(BASE_DIR):
            os.mkdir(str(BASE_DIR) + 'temp')
        # """""saving file in flask app"""""
        file_temp_save=open(str(BASE_DIR) + '/' + 'temp/'+ file_name, "wb").write(r.content)
        print("saved in temp")

        # file_temp_save=open(f"{file_name}", "wb").write(r.content)

        #send file and as attachment downloads the file to desktop
        response=send_file(f"{str(BASE_DIR) + '/' + 'temp/'+ file_name}", as_attachment=True)
        # return send_file(f"{str(BASE_DIR) + '/' + 'temp/'+ file_name}", as_attachment=True)
        # delete the file from the temporary directory
        file_path = f"{str(BASE_DIR)}/temp/{file_name}"
        if os.path.exists(file_path):
            os.remove(file_path)
        return response
        # return send_file(f"{cwd + 'temp/'+ file_name}", as_attachment=True)
        
        # write to a file in the app's instance folder
        # come up with a better file name
        # with app.open_instance_resource('downloaded_file', 'wb') as f:
        #     f.write(r.content)
        # return redirect(url_for('order_details',appointment_id=appointment_id))
    except Exception as e:
        print(e)
        flash("Sorry.. Could not download the file","error")
        return redirect(url_for("order_detail",id=appointment_id))

@app.route("/add_doctor",methods=['GET','POST'])
def add_doctor():
    try:
        headers={
            "Content-Type":"application/json"
        }
        # language api call
        language_api_request=requests.get(base_url+language_api,headers=headers)
        print("language api",language_api_request.status_code)
        language_api_response=json.loads(language_api_request.text)
        languages=language_api_response['data']
        #specializations list api call
        specialization_request=requests.get(base_url+specialization_list_api, headers=headers)
        specialization_response=json.loads(specialization_request.text)
        print("specialization list api",specialization_request.status_code)
        specializations=specialization_response['data']
        # print(specializations)
        # locations api call
        location_req=requests.get(base_url+locations_api, headers=headers)
        print("locations",location_req.status_code)
        location_resp=json.loads(location_req.text)
        print(location_req.status_code)
        print(location_resp)
        locations=location_resp['data']
        file_headers={
                'files' : 'multipart/form-data'
            }
        # cwd = os.getcwd()+'/'
        # files = os.listdir(cwd + 'temp')
        print("something")
        if request.method == 'POST':
            print("post")
            
           

            if request.form['form_type'] == "add_doctor":
                print("add doctor")

                # ******* FILE UPLOADS ********

                # """""" ADDRESS PROOF UPLOAD """"""
                address_file = request.files["address_proof_file"]
                addressFileName = secure_filename(address_file.filename)
                print(addressFileName)
                if addressFileName:
                    print("BASE_DIR : ",BASE_DIR)
                    if 'temp' not in os.listdir(BASE_DIR):
                        os.mkdir(str(BASE_DIR) + '/' + 'temp')
                    address_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', addressFileName))

                    file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ addressFileName)
                    # print(file_stats)
                    address_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                    print(address_file_size)    
                    print(f'{file_stats.st_size / (1024)} KB')
                    print(f'{file_stats.st_size / (1024 * 1024)} MB')

                    with open(str(BASE_DIR) + '/' + 'temp/'+ addressFileName, 'rb') as f:
                    
                        data_file = {
                            "common_file":(addressFileName, f)
                        }
                        print(data_file)
                        file_uploader_api=base_url+file_upload_api
                        file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                        print(file_upload_submit.status_code)                    
                        file_upload_response=json.loads(file_upload_submit.text)
                        print(file_upload_response)
                        print(file_upload_submit.status_code)
                        address_file_path=file_upload_response['common_file']
                        print(address_file_path)
                        if file_upload_response['common_file']:
                            flash(f"{addressFileName} uploaded","success")
                            # delete the photo file from the temporary directory
                            # os.remove(os.path.join(str(BASE_DIR) +"/" + 'temp', addressFileName))
                        else:
                            flash("Address file is unable to upload","error")
                else:
                    addressFileName = ""
                    address_file_size = ""
                    address_file_path = ""

                # """ CERTIFICATE FILE UPLOAD"""
                certificate_file = request.files["certificate_file"]
                certificateFileName = secure_filename(certificate_file.filename)
                print(certificateFileName)
                
                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                certificate_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', certificateFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ certificateFileName)
                # print(file_stats)
                certificate_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(certificate_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ certificateFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(certificateFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(certificateFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    certificate_file_path=file_upload_response['common_file']
                    if file_upload_response['common_file']:
                        flash(f"{certificateFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        # os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', certificateFileName))
                    else:
                        flash("Certificate is unable to upload","error")

                # """ PHOTO UPLOAD """
                photo_file = request.files["photo_file"]
                photoFileName = secure_filename(photo_file.filename)
                print(photoFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # photo_file.save(os.path.join(cwd + 'temp', photoFileName))

                # with open(cwd + 'temp/'+ photoFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(photoFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(photoFileName, f)
                #     }

                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                photo_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', photoFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ photoFileName)
                # print(file_stats)
                photo_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(photo_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ photoFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(photoFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(photoFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    photo_file_path=file_upload_response['common_file']
                    if file_upload_response['common_file']:
                        flash(f"{photoFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        # os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', photoFileName))
                    else:
                        flash("Profile photo is unable to upload","error")

                # """" SIGNATURE FILE UPLOAD """"
                signature_file = request.files["signature_file"]
                signatureFileName = secure_filename(signature_file.filename)
                print(signatureFileName)
                
                if signatureFileName:
                    print("BASE_DIR : ",BASE_DIR)
                    if 'temp' not in os.listdir(BASE_DIR):
                        os.mkdir(str(BASE_DIR) + '/' + 'temp')
                    signature_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', signatureFileName))

                    file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ signatureFileName)
                    # print(file_stats)
                    signature_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                    print(signature_file_size)
                    print(f'{file_stats.st_size / (1024)} KB')
                    print(f'{file_stats.st_size / (1024 * 1024)} MB')

                    with open(str(BASE_DIR) + '/' + 'temp/'+ signatureFileName, 'rb') as f:
                        # data_file = {
                        #     "common_file":(signatureFileName, 'rb')
                        # }
                        data_file = {
                            "common_file":(signatureFileName, f)
                        }
                        print(data_file)
                        file_uploader_api=base_url+file_upload_api
                        file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                        print(file_upload_submit.status_code)                    
                        file_upload_response=json.loads(file_upload_submit.text)
                        print(file_upload_response)
                        print(file_upload_submit.status_code)
                        signature_file_path=file_upload_response['common_file']
                        if file_upload_response['common_file']:
                            flash(f"{signatureFileName} uploaded","success")
                            # delete the photo file from the temporary directory
                            # os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', signatureFileName))
                        else:
                            flash("signature file is unable to upload","error")        
                else:
                    signatureFileName = ""
                    signature_file_size = ""
                    signature_file_path = ""
                # ******* FILE UPLOADS E ********

                first_name=request.form['first_name']
                last_name=request.form['last_name']
                email_address=request.form['email_address']
                phone_no=request.form['phone_no']
                # designation=request.form['designation']
                qualification = request.form['qualification']
                specialization=request.form['specialization']
                address=request.form['address']
                location=request.form['location']
                gender=request.form['gender']
                language=request.form.getlist('language')
                certificate_number=request.form['certificate_number']
                doctor_bio=request.form['doctor_bio']
                # certificate_nimber=request.files['certificate_file']
                # profile_photo=request.files['doc_profile_photo']

                # language=request.form['language']
                # from_date=request.form['from_date']
                # to_date=request.form['to_date']
                # from_time=request.form['from_time']
                # to_time=request.form['to_time']

                payload={
                        "new_user":1,
                        "user_id":"",
                        "doc_fname":first_name,
                        "doc_lname":last_name,
                        "email":email_address,
                        "specialization":specialization,
                        "location":location,
                        "mobile_num":phone_no,
                        
                        "language_known":language,
                        "gender":gender,
                        "qualification":qualification,
                        "address":address,
                        "certificate_no":certificate_number,
                        "doctor_bio":doctor_bio,

                        "address_proof":address_file_path,
                        "addr_file_name": addressFileName,
                        "addr_file_size": address_file_size,

                        "registration_certificate":certificate_file_path,
                        "reg_file_name": certificateFileName,
                        "reg_file_size": certificate_file_size,

                        "signature":signature_file_path,
                        "sign_file_name": signatureFileName,
                        "sign_file_size": signature_file_size,

                        "profile_pic":photo_file_path,
                        "profile_file_name":photoFileName,
                        "profile_file_size":photo_file_size

                        # "date_from":from_date,
                        # "date_to":to_date,
                        # "time_slot_from":from_time,
                        # "time_slot_to":to_time
                }
                    
                api_data=json.dumps(payload)
                print(api_data)
                add_doctor=requests.post(base_url+add_doctor_api,data=api_data, headers=headers)
                print("add doc:",add_doctor.status_code)
                add_doctor_response=json.loads(add_doctor.text)
                print(add_doctor_response)
                if add_doctor_response['response_code']==200:
                    print("doctor added")
                    return redirect(url_for("thank_you_add_doc"))
                elif add_doctor_response['response_code']==400 :
                    flash("Email is already used.","error")
                    return redirect(url_for('add_doctor'))
                else:
                    flash("something error","error")
                    return redirect(url_for('add_doctor'))
                return redirect(url_for('add_doctor'))
        return render_template("add_doctor_form.html",languages=languages,specializations=specializations,locations=locations)
    except Exception as e:
        print(e)
    return render_template("add_doctor_form.html")

@app.route("/thank_you_for_submitting")
def thank_you_add_doc():
    return render_template("thank_you_add_doc.html")

@app.route("/update_doctor",methods=['GET','POST'])
def update_doctor():
    try:
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        headers = {
                "Content-Type":"application/json"
            }
        payload={
            "doctor_id":doctor_id
        }
        api_data=json.dumps(payload)
        print(api_data)
        # doctor profile api call
        doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
        print(doctor_profile_request.status_code)
        doctor_profile_response=json.loads(doctor_profile_request.text)
        # print(doctor_profile_response)
        
        doctor_profile1=doctor_profile_response['data1']
        doctor_profile2=doctor_profile_response['data2']
         #language given as list must be separated
        language_list=doctor_profile2['language_known']
        # language_known=", ".join(language)
        # print(", ".join(language))
        # print(*language, sep = ', ')
        language_list_length=len(language_list)
        print("languages",language_list_length)

        # signature_url=doctor_profile2['signature']
        # r = requests.get(signature_url)
        # # r = requests.get(url)
        # print("error")
        # # this removes http and website part from url
        # url_split_1 = urlparse(url)
        # print(url_split_1)
        # #this will split rest of the path from file name
        # file_name=os.path.basename(url_split_1.path)
        # print("filename",file_name)

        # cwd = os.getcwd()+'/'
        # print(cwd)
        # if 'temp' not in os.listdir(cwd):
        #     os.mkdir(cwd + 'temp')
        # #saving file in flask app
        # file_temp_save=open(cwd + 'temp/'+ file_name, "wb").write(r.content)
        # print("saved in temp")

        # cwd = os.getcwd()+'/'
        # print(cwd)

        # not required to save the file
        # print("base dir:", BASE_DIR)
        # if 'temp' not in os.listdir(BASE_DIR):
        #     os.mkdir(str(BASE_DIR) + '/'+ 'temp')
        # #saving file in flask app
        # file_temp_save=open(str(BASE_DIR) + '/'+ 'temp/'+ file_name, "wb").write(r.content)
        # print("saved in temp")


        # language api call
        language_api_request=requests.get(base_url+language_api,headers=headers)
        print("language api",language_api_request.status_code)
        language_api_response=json.loads(language_api_request.text)
        languages=language_api_response['data']
        #specializations list api call
        specialization_request=requests.get(base_url+specialization_list_api, headers=headers)
        specialization_response=json.loads(specialization_request.text)
        print("specialization list api",specialization_request.status_code)
        specializations=specialization_response['data']
        # print(specializations)

        # work hour timeslot api call
        timeslot_list_request=requests.post(base_url+time_slot_list_api, data=api_data, headers=headers)
        timeslot_list_response=json.loads(timeslot_list_request.text)
        print(timeslot_list_request.status_code)
        timeslots = timeslot_list_response['data']
        days = timeslot_list_response['weekday']

        # working hours api call
        # working_hours_request=requests.post(base_url+working_hours_api, data=api_data, headers=headers)
        # working_hours_response=json.loads(working_hours_request.text)
        # print("working hours",working_hours_request.status_code)
        # working_hours=working_hours_response['data']

        

        if request.method == 'POST':
            print("post")       
            
            # file upload
            # ******* FILE UPLOADS ********
            address_file = request.files["address_proof_file"]
            if address_file.filename == '':
                address_file_path=''
                addressFileName=''
                address_file_size=''
            # if request.files["address_proof_file"] == '':
                print("no address file")
            else:
                # Format the time as microseconds
                microseconds = datetime.now().strftime("%f")
                
                address_file = request.files["address_proof_file"]
                print("address",address_file)

                addressFileName = f"{microseconds}_{secure_filename(address_file.filename)}"
                print("proof")
                print(addressFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # address_file.save(os.path.join(cwd + 'temp', addressFileName))

                # with open(cwd + 'temp/'+ addressFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(addressFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(addressFileName, f)
                #     }
                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    print("print line 1")
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                    print("print line 2")
                address_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', addressFileName))
                print("print line 3")

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ addressFileName)
                print("print line 4")
                # print(file_stats)
                address_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(address_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ addressFileName, 'rb') as f:
                    print("print line 5")
                    # data_file = {
                    #     "common_file":(addressFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(addressFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    address_file_path=file_upload_response['common_file']
                    print(address_file_path)
                    if file_upload_response['common_file']:
                        flash(f"{addressFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', addressFileName))
                    else:
                        flash("Something went wrong","error")

            certificate_file = request.files["certificate_file"]
            if certificate_file.filename == '':
                certificate_file_path=''
                certificateFileName=''
                certificate_file_size=''
                print("no certificate file")
            else:
                certificate_file = request.files["certificate_file"]
                certificateFileName =  f"{microseconds}_{secure_filename(certificate_file.filename)}"
                print(certificateFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # certificate_file.save(os.path.join(cwd + 'temp', certificateFileName))

                # with open(cwd + 'temp/'+ certificateFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(certificateFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(certificateFileName, f)
                #     }

                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                certificate_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', certificateFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ certificateFileName)
                # print(file_stats)
                certificate_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(certificate_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ certificateFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(certificateFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(certificateFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    certificate_file_path=file_upload_response['common_file']
                    if file_upload_response['common_file']:
                        flash(f"{certificateFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', certificateFileName))
                    else:
                        flash("Something went wrong","error")

            photo_file = request.files["photo_file"]
            if photo_file.filename == '':
                photo_file_path=''
                photoFileName=''
                photo_file_size=''
                print("no photo file")
            else:
                photo_file = request.files["photo_file"]
                photoFileName =  f"{microseconds}_{secure_filename(photo_file.filename)}"
                print(photoFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # photo_file.save(os.path.join(cwd + 'temp', photoFileName))

                # with open(cwd + 'temp/'+ photoFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(photoFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(photoFileName, f)
                #     }

                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                photo_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', photoFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ photoFileName)
                # print(file_stats)
                photo_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(photo_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ photoFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(photoFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(photoFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    photo_file_path=file_upload_response['common_file']
                    if file_upload_response['common_file']:
                        flash(f"{photoFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', photoFileName))
                    else:
                        flash("Something went wrong","error")

            signature_file = request.files["signature_file"]
            if signature_file.filename == '':
                signature_file_path=''
                signatureFileName=''
                signature_file_size=''
                print("no signature file")
            else:
                signature_file = request.files["signature_file"]
                signatureFileName = f"{microseconds}_{secure_filename(signature_file.filename)}"
                print(signatureFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # signature_file.save(os.path.join(cwd + 'temp', signatureFileName))

                # with open(cwd + 'temp/'+ signatureFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(signatureFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(signatureFileName, f)
                #     }

                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                signature_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', signatureFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ signatureFileName)
                # print(file_stats)
                signature_file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(signature_file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ signatureFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(signatureFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(signatureFileName, f)
                    }
                    print(data_file)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    print(file_upload_response)
                    print(file_upload_submit.status_code)
                    signature_file_path=file_upload_response['common_file']
                    if file_upload_response['common_file']:
                        flash(f"{signatureFileName} uploaded","success")
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', signatureFileName))
                    else:
                        flash("Something went wrong","error")        

                # ******* FILE UPLOADS E ********

            # other fields
            first_name=request.form['first_name']
            last_name=request.form['last_name']
            email_address=request.form['email_address']
            phone_no=request.form['phone_no']
            designation=request.form['designation']
            qualification = request.form['qualification']
            specialization=request.form['specialization']
            address=request.form['address']
            location=request.form['location']
            gender=request.form['gender']
            language=request.form.getlist('language')
            certificate_number=request.form['certificate_number']
            doctor_bio=request.form['doctor_bio']
            # from_date=request.form['from_date']
            # to_date=request.form['to_date']
            # from_time=request.form['from_time']
            # to_time=request.form['to_time']
            print("user_id",doctor_id)

            payload={
                "user_id":doctor_id,
                "user_fname":first_name,
                "user_lname":last_name,
                "gender":gender,
                "mobile_num":phone_no,
                "user_mail":email_address,
                "language_known": language,
                "location":location,
                "doctor_flag":designation,
                "specialization":specialization,

                "qualification":qualification,
                "address":address,
                "certificate_no":certificate_number,
                "doctor_bio":doctor_bio,

                "address_proof":address_file_path,
                "addr_file_name": addressFileName,
                "addr_file_size": address_file_size,

                "registration_certificate":certificate_file_path,
                "reg_file_name": certificateFileName,
                "reg_file_size": certificate_file_size,

                "signature":signature_file_path,
                "sign_file_name": signatureFileName,
                "sign_file_size": signature_file_size,

                "profile_pic":photo_file_path,
                "profile_file_name":photoFileName,
                "profile_file_size":photo_file_size,
                "operation_flag":"edit"

            }
                # "date_from":from_date,
                # "date_to":to_date,
                # "time_from":from_time,
                # "time_to":to_time

            # }
            
            
            api_data=json.dumps(payload)
            print(api_data)
            doctor_update_request=requests.post(base_url+doctor_update_api, data=api_data, headers=headers)
            print("update doctor",doctor_update_request.status_code)
            doctor_update_response=json.loads(doctor_update_request.text)
            print(doctor_update_response)
            if doctor_update_response['response_code']==200:
                flash("Doctor Profile Updated","success")
            else:
                flash("Something went wrong","error")
            # changing doctor name in session if profile is edited so name changes everywhere
            doctor_first_name = doctor_profile1['first_name']
            session['doctor_first_name'] = doctor_first_name
            doctor_last_name = doctor_profile1['last_name']
            session['doctor_last_name'] = doctor_last_name
            doctor_email = doctor_profile1['email']
            session['doctor_email'] = doctor_email

            # doctor_update=doctor_update_response["data"]

            # signature
            print("upload signature")
            # file_headers={
            #     'files' : 'multipart/form-data'
            # }
            # print("error 1")
            # assessment_file=request.files['customFile']
            # print("error2")
            # print(assessment_file)
            # filename=secure_filename(assessment_file.filename)
            # print("error3")
            # print(filename)
            # files={
            #     'common_file' : open(filename,'rb')
            # }
            # print(files)
            # data={
            #     'appointment_id': id,
            #     'file_flag':'analysis_info'
            # }
            # api_data=json.dumps(data)
            # file_upload_submit=requests.post(base_url+file_upload_api, files=files, data=api_data, headers=file_headers)
            # file_upload_response=json.loads(file_upload_submit.text)
            # print(file_upload_response)
            # print("file upload",file_upload_submit.status_code)
            return redirect(url_for('doctor_profile'))
        return render_template("update_doctor.html", doctor_profile1=doctor_profile1,doctor_profile2=doctor_profile2,
        languages=languages,specializations=specializations,language_list=language_list, timeslots=timeslots, days=days)
    except Exception as e:
        print(e)       
    return redirect('/profile')
 
    


@app.route("/profile",methods=['GET','POST'])
def doctor_profile():
    try:
        if 'user_id' in session:
                doctor_id=session['user_id']
                print("doctor_id",doctor_id)
        else:
            return redirect(url_for('login'))
        headers = {
                "Content-Type":"application/json"
            }
        payload={
            "doctor_id":doctor_id
        }
        
        
        api_data=json.dumps(payload)
        doctor_profile_request=requests.post(base_url+doctor_profile_api, data=api_data, headers=headers)
        doctor_profile_response=json.loads(doctor_profile_request.text)
        doctor_profile1=doctor_profile_response['data1']
        doctor_profile2=doctor_profile_response['data2']
        language=doctor_profile2['language_known']
        language_known=", ".join(language)
        print(", ".join(language))
        print(*language, sep = ', ')
        print(request.method,"method")
        
        payout_payload={
            "doctor_id":doctor_id,
            "payout_status":""
        }
        payout_json_data=json.dumps(payout_payload)
        payout_request=requests.post(base_url+payout_list_api, data=payout_json_data, headers=headers)
        print("payout",payout_request.status_code)
        payout_response=json.loads(payout_request.text)
        payouts=payout_response['data']
        print("payouts",payouts)
        print("error")
        payout_data=payouts['payouts']
        print("payouts list",payout_data)

        """ Upload Signature """
        
        if request.method == 'POST':
            if request.form['form_type'] == 'upload_signature':
                print("upload Signature")
                file_headers={
                    'files' : 'multipart/form-data'
                }
                print("error 1")
                uploaded_file=request.files['customFile']
                print("error2")
                print(uploaded_file)
                up_file=uploaded_file.filename
                print("upfile",up_file)
                #files=request.files['customFile']
                files={
                    'common_file' : open(up_file,'rb')
                }
                print(files)
                data={
                    'appointment_id': 1,
                    'file_flag':'doctor_signature'
                }
                api_data=json.dumps(data)
                file_upload_submit=requests.post(base_url+file_upload_api, files=files, data=api_data, headers=file_headers)
                file_upload_response=json.loads(file_upload_submit.text)
                print(file_upload_response)
                if file_upload_response['common_file']:
                    # delete the photo file from the temporary directory
                    os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', up_file))
                print(file_upload_submit.status_code)
                
            return redirect(url_for('profile', id=doctor_id))
        return render_template("doctor_profile.html",doctor_profile1=doctor_profile1,doctor_profile2=doctor_profile2,
        language_known=language_known,payouts=payout_data)
    except Exception as e:
        print(e)
        return render_template("doctor_profile.html")

@app.route("/dashboard/")
def dashboard():
    print(session)
    try:
        headers = {
            "Content-Type":"application/json"
        }
        if 'username' in session:
            check_user = requests.post(base_url+'/api/doctor/is_dr_blocked/', data=json.dumps({'email':session['username']}), headers=headers)
            res_check_user = json.loads(check_user.text)
            print('res_check_user',res_check_user)
            if res_check_user['status'] == 'blocked':
                session.clear()
                return redirect(url_for('login'))
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)
        
        dash_payload={
            "doctor_id":doctor_id,
            "doctor_flag":doctor_flag
        }
        dash_json=json.dumps(dash_payload)
        print(dash_json)
        dashboard_request=requests.post(base_url+dashboard_api,data=dash_json,headers=headers)
        's'
        print("dashboard code:",dashboard_request.status_code)
        dashboard_response=json.loads(dashboard_request.text)
        dashboard_data=dashboard_response['data']
        print(dashboard_data)

        # calling list api for all orders
        payload_a={
            "appointment_status" : "",
            "user_id":doctor_id,
            "doctor_flag":doctor_flag,
            "appointment_month":"",
            # "gender": gender,
            # "languages_known": languages_known
        }
        api_data=json.dumps(payload_a)
        print(api_data)
        
        all_orders=appointment_listing(api_data)
        total_orders=len(all_orders)
        print(total_orders)

        # upcoming & follow up appointments table
        # appointment api call for upcoming table
        payload1={
            "appointment_status" : [1,2,7],
            "user_id":doctor_id,
            "doctor_flag":doctor_flag,
            "appointment_month":""
        }
        api_data=json.dumps(payload1)
        print(api_data)    
        #calling appointment_listing function
        all_upcoming_orders=appointment_listing(api_data)
        new_order=len(all_upcoming_orders)
        print("new",len(all_upcoming_orders))
        if all_upcoming_orders:
            # if all_upcoming_orders['appointment_id']:
            upcoming_orders=all_upcoming_orders[0:10]
        else:
            upcoming_orders=[]
        # print(upcoming_orders)
        # appointment api call for follow up table
        payload2={
            "appointment_status" : [1,8],
            "user_id":doctor_id,
            "doctor_flag":doctor_flag,
            "appointment_month":""
        }
        api_data=json.dumps(payload2)
        print(api_data)    
        #calling appointment_listing function
        all_followup_orders=appointment_listing(api_data)
        if all_followup_orders:
            followup_orders=all_followup_orders[0:4]
        else:
            followup_orders=[]
        # print(followup_orders)

        # active orders
        payload7={
                    "appointment_status" : [1,2,7,11,12,8],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag,
                    # "gender": gender,
                    # "languages_known": languages_known
                }
        api_data=json.dumps(payload7)
        print(api_data)
        all_active_orders=appointment_listing(api_data)
        if all_active_orders:
            active_orders=all_active_orders[0:10]
        else:
            active_orders=[]

        # earnings api call
        payout_payload={
            "doctor_id":doctor_id,
            "payout_status":""
        }
        payout_json_data=json.dumps(payout_payload)
        payout_request=requests.post(base_url+payout_list_api, data=payout_json_data, headers=headers)
        print("payout",payout_request.status_code)
        payout_response=json.loads(payout_request.text)
        payouts=payout_response['data']
        # print("payouts",payouts)
        # print("error")
        payout_data=payouts['payouts']
        # print("payouts list",payout_data)

        return render_template('appointment_dashboard.html',upcoming_orders=upcoming_orders, followup_orders=followup_orders,
        dashboard_data=dashboard_data, active_orders=active_orders, total_orders=total_orders, new_order=new_order,payouts=payouts)
    except Exception as e:
        print(e)
    return render_template('appointment_dashboard.html')
    
# @app.route("/appointment_list_tabs/" , methods=['GET','POST'])

# function
def appointment_listing(api_data):
    print(api_data)
    headers = {
        "Content-Type":"application/json"
    }
    print(headers)
    appointment_response=requests.post(base_url+appointment_list_api,data=api_data,headers=headers)
    # print(base_url+appointment_list_api)
    print('appointment list api status code',appointment_response.status_code)
    appointment_data=json.loads(appointment_response.text)
    all_appointments=appointment_data['data']
    return all_appointments
    
@app.route("/doctor_dash", methods=['GET','POST'])
def doctor_dash():
    print(session)
    headers = {
        "Content-Type":"application/json"
    }  
    if 'username' in session:
        check_user = requests.post(base_url+'/api/doctor/is_dr_blocked/', data=json.dumps({'email':session['username']}), headers=headers)
        res_check_user = json.loads(check_user.text)
        print('res_check_user',res_check_user)
        if res_check_user['status'] == 'blocked':
            session.clear()
            return redirect(url_for('login'))
    appointment_list_api="api/doctor/appointment_list"
    if 'user_id' in session:
        doctor_id=session['user_id']
        print(doctor_id)
    else:
        return redirect(url_for('login'))
    if 'doctor_flag' in session:
        doctor_flag=session['doctor_flag']
        print(doctor_flag)
   

    if doctor_flag == 2: 
   
        payload1={
                    "appointment_status" : "",
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag,
                    "appointment_month":"",
                
                }
        api_data=json.dumps(payload1)
        print(api_data)
        # calling fuction appointment_listing
        all_orders=appointment_listing(api_data)
       
        payload2={
            "appointment_status" : [0,10],
            "user_id":doctor_id,
            "doctor_flag":"",
            "appointment_month":"",
        }
        api_data=json.dumps(payload2)
        print(api_data)
        new_orders=appointment_listing(api_data)
    
        payload3={
                    "appointment_status" : [1,7,8,10],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload3)
        print(api_data)
        upcoming_orders=appointment_listing(api_data)
        payload4={
                    "appointment_status" : [2],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload4)
        print(api_data)
        escalated_orders=appointment_listing(api_data)
        payload5={
                    "appointment_status" : [4,5,7],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload5)
        print(api_data)
        rescheduled_orders=appointment_listing(api_data)
        # completed(6) appointments
        payload6={
                    "appointment_status" : [6],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload6)
        print(api_data)
        completed_orders=appointment_listing(api_data)

        return render_template('appointment_list.html',appointment_list=all_orders,new_orders=new_orders,upcoming_orders=upcoming_orders,
            escalated_orders=escalated_orders,rescheduled_orders=rescheduled_orders,completed_orders=completed_orders)
    
    elif doctor_flag == 1:
    #senior doctor
    #active
    # escalated(2) and rescheduled(7) and senior_transfered(11) and new paid appointment(12) and followup(8) appointments
        payload7={
            "appointment_status" : [1,2,7,11,12],
            "user_id":doctor_id,
            "doctor_flag":doctor_flag,
            # "gender": gender,
            # "languages_known": languages_known
        }
        api_data=json.dumps(payload7)
        print(api_data)
        active_orders=appointment_listing(api_data)
    #rescheduled    
    # rescheduled by doctor(4) and rescheduled by customer(5) and rescheduled(7) appointments
        payload8={
                    "appointment_status" : [4,5,7],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload8)
        print(api_data)
        rescheduled_orders=appointment_listing(api_data)
    #completed    
    # completed(6) appointments
        payload9={
                    "appointment_status" : [6,3,9],
                    "user_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
        api_data=json.dumps(payload9)
        print(api_data)
        completed_orders=appointment_listing(api_data)

        return render_template('appointment_list.html',active_orders=active_orders,rescheduled_orders=rescheduled_orders,
                completed_orders=completed_orders)
    
    return render_template('appointment_list.html')

@app.route('/appointment_complete/<int:appointment_id>', methods=['GET'])
def appointment_complete(appointment_id):
    print(appointment_id)
    headers={
            "Content-Type":"application/json"
        }
    payload={
        "appointment_id":appointment_id,
    }
    api_data=json.dumps(payload)
    print(payload)
    complete_order=requests.post(base_url+complete_api,data=api_data,headers=headers)
    complete_order_response=json.loads(complete_order.text)
    print(complete_order.status_code)
    print(complete_order_response)
    return redirect(url_for('order_detail',id = complete_order_response['data']['appointment_id']))
  
@app.route("/dashboard/doctor_dash/<actions>/<int:appointment_id>",methods=['GET','POST'])
# actions:new=0, accept=1,reject/cancel=3,escalate=2, new paid = 12
# reschedule by doctor = 4, reschedule by customer = 5, rescheduled=7
# appointment closed = 6, follow up=8 no show=9 , transfer junior=10, transfer senior =11
def action_doctor(actions,appointment_id):
    appointent_status_api="api/doctor/appointment_status_update"
    if 'user_id' in session:
        doctor_id=session['user_id']
        print(doctor_id)
    headers={
            "Content-Type":"application/json"
        }
    print(appointment_id)
    print(actions)
    # if 'user_id' in session:
    #     user_id=session['user_id']
    #     print(user_id)
        
    if actions == '1':
        print("action1")
        payload={
            "doctor_id":doctor_id,
            "appointment_id":appointment_id,
            "appointment_status":actions
        }
        api_data=json.dumps(payload)
        print(payload)
        accept_order=requests.post(base_url+order_accept_api,data=api_data,headers=headers)
        accept_order_response=json.loads(accept_order.text)
        print(accept_order.status_code)
        print(accept_order_response)
        return redirect(url_for("doctor_dash"))

        # closing an appointment / appointment marked as done functionality
    elif actions == '6':
        print("action6")
        payload={
            "appointment_id":appointment_id,
            "appointment_status":actions,
            "doctor_id":doctor_id,
            "location_id":1
        }
        api_data=json.dumps(payload)
        close_appointment_request=requests.post(base_url+appointent_status_api,data=api_data,headers=headers)
        close_appointment_response=json.loads(close_appointment_request.text)
        print("close appointment",close_appointment_request.status_code)
        print(close_appointment_response)
        flash(f"Appointment closed","success")
        # return redirect(url_for('add_rating',appointment_id=appointment_id))
        # return redirect(url_for("doctor_dash"))
        return redirect(url_for('order_detail',id=appointment_id,active_tab='observation'))
        
    else:
        payload={
            'appointment_id':appointment_id,
            'appointment_status':actions
        }
        api_data=json.dumps(payload)
        print(api_data)
        action=requests.post(base_url+appointent_status_api,data=api_data,headers=headers)
        action_button_response=json.loads(action.text)
        print(action.status_code)
        print(action_button_response)
        return redirect(url_for("doctor_dash"))
    # return redirect(url_for("doctor_dash"))

@app.route("/dashboard/order_detail/<int:id>",methods=['GET','POST'])
def order_detail(id):
    id=id
    appointment_detail_api="api/doctor/appointment_detail"
    observations_api="api/doctor/observations"
    reschedule_api="api/doctor/appointment_schedule"
    prescription_api="api/doctor/prescriptions"
    try:
        active_tab=request.args.get('active_tab')
        # print("active",active_tab)

        if 'user_id' in session:
            doctor_id=session['user_id']
            # print("doc id",doctor_id)
        else:
            return redirect(url_for('login'))
        
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            session.permanent = True
            # print("doc flag",doctor_flag)

        headers={
                "Content-type":"application/json"
        }
        # print(id)
        payload={
            "appointment_id":id,
            "user_id":"",
            "file_flag":"",
            "doctor_id":doctor_id
        }
        api_data=json.dumps(payload)
        # print(api_data)
        appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
        # print("detail api :",appointment_detail.status_code)
        appointment_detail_response=json.loads(appointment_detail.text)
        appointment_details=appointment_detail_response['data']
        # print("detail api :",appointment_detail.status_code)
        user_id=appointment_details['user_id']
        # print(user_id)
        category_id=appointment_details['category_id']
        follow_ups = appointment_details['followup']
        observations=appointment_details['observations']
        prescript_text=appointment_details["prescript_text"]
        # doctor list api
        doctor_listing=requests.post(base_url+doctor_listing_api, headers=headers)
        doctor_list_response=json.loads(doctor_listing.text)
        # print("doctor_list",doctor_listing.status_code)
        doctor_list = doctor_list_response['data']
        
        # language api call
        language_api_request=requests.get(base_url+language_api,headers=headers)
        # print("language api",language_api_request.status_code)
        language_api_response=json.loads(language_api_request.text)
        languages=language_api_response['data']
        #specializations list api call
        specialization_request=requests.get(base_url+specialization_list_api, headers=headers)
        specialization_response=json.loads(specialization_request.text)
        # print("specialization list api",specialization_request.status_code)
        specializations=specialization_response['data']
        #specialization filter api for time slot 
        # timeslot_data={
        #     "specialization":""
        # }
        # api_timeslot_data=json.dumps(timeslot_data)
        # specialization_filter=requests.post(base_url+specialization_filter_api,data=api_timeslot_data,headers=headers)
        # specialization_filter_response=json.loads(specialization_filter.text)
        # print(specialization_filter.status_code)
        # timeslot = specialization_filter_response['time_slot']
        # doctor_specializations=specialization_filter_response['doctor']

        if request.method == 'POST':
            print("post")
            print(request.form['form_type'])

            if request.form['form_type'] == 'edit_customer_info': 
                print("edit_customer_info")     

                first_name=request.form['first_name']
                last_name=request.form['last_name']
                date_of_birth=request.form['date_of_birth']
                phone_number=request.form['phone_number']
                email_address=request.form['email_address']

                data={
                    "user_id":user_id,
                    "user_fname":first_name,
                    "user_lname":last_name,
                    "mobile_num":phone_number,
                    "dob":date_of_birth,
                    "user_mail":email_address,
                    "profile_pic":"",
                    "operation_flag":"edit"
                }
                json_data=json.dumps(data)
                # print(json_data)
                customer_edit_submit=requests.post(base_url+customer_edit_api, data=json_data, headers=headers)
                print(customer_edit_submit.status_code)
                customer_edit_submit_response=json.loads(customer_edit_submit.text)
                print("post response:",customer_edit_submit.status_code)
                # print(customer_edit_submit_response)

            if request.form['form_type'] == 'jr_assessment':
                print("junior doctor assessment")
                print(request.form)

                height = request.form['height']
                weight = request.form['weight']
                medical_history = request.form['medical_condition']
                prescription_history = request.form['medications']
                other_supplements = request.form['supplements']
                allergies = request.form['allergies']

                data={
                        "appointment_id":id, 
                        "doctor_flag": doctor_flag,
                        "doctor_id": doctor_id,
                        "height": height,
                        "weight": weight,
                        "is_allergic": allergies,
                        "medical_history":medical_history,
                        "prescription_history": prescription_history,
                        "other_suppliments_history":other_supplements
                    }
                payload = json.dumps(data)
                print("payload")
                cust_history = requests.post(base_url+patient_history_api, data=payload, headers=headers)
                'sss'
                # print("patient history api: ",cust_history.status_code)
                cust_hist_resp = json.loads(cust_history.text)
                # print(cust_hist_resp)
                if cust_hist_resp['response_code'] == 200:
                    flash(" Details added ", "success")
                    return redirect(url_for('order_detail',id=id))
                else:
                    flash(" Something went wrong.. Please try again ", "error")

            if request.form['form_type'] == 'reschedule':
                print("reschedule")
                if doctor_flag == 1:
                    # reschedule_date=request.form['reschedule_date']
                    # reschedule_time=request.form['reschedule_time']
                    reschedule_date=""
                    reschedule_time=""
                else :
                    # reschedule_date=request.form['reschedule_date_jr']
                    # reschedule_time=request.form['reschedule_time_jr']
                    reschedule_date=""
                    reschedule_time=""

                reschedule_data={
                    "appointment_id":id,
                    "appointment_date":reschedule_date,
                    "appointment_time":reschedule_time,
                    "appointment_status":4,
                    # "appointment_status":7,
                    "user_id": user_id,
                    "doctor_id":doctor_id,
                    "doctor_flag":doctor_flag
                }
                # print(reschedule_data)
                reschedule_data_json=json.dumps(reschedule_data)
                reschedule_submit=requests.post(base_url+reschedule_api, data=reschedule_data_json, headers=headers)
                reschedule_submit_response=json.loads(reschedule_submit.text)
                # print(reschedule_submit_response)
                # print(reschedule_submit.status_code)
                # if reschedule_submit_response['message'] == 'Time Slot not Available':
                #     flash("This time slot is not available","error")
                if reschedule_submit_response['response_code'] == 400:
                    flash("Something went wrong try again","error")
                if reschedule_submit_response['response_code'] == 200:
                    flash("Reschedule requested","success")

            if request.form['form_type'] == 'observation': 
                # print("observation") 
                active_tab="observation"
                observations=request.form['observations']
                data={
                    "appointment_id":id,
                    "observations":observations,
                    "doctor_id":doctor_id
                }
                json_data=json.dumps(data)
                print('json_data')
                observation_submit=requests.post(base_url+observations_api, data=json_data, headers=headers)
                observation_submit_response=json.loads(observation_submit.text)
                # print("add observation response:",observation_submit.status_code)
                # print(observation_submit_response)
                if observation_submit_response['response_code'] == 200 :
                    flash("Observation added", "success")
                else:
                    flash("Something went wrong please try again..", "error")
                return redirect(url_for('order_detail', id=id, active_tab="observation",active="observation"))

            if request.form['form_type'] == 'edit_observation':
                # print("edit_observation")
                active_tab="observation"
                observation_id=request.form['observation_id']
                observe_id=f'{observation_id}/'
                # print(observe_id)
                edit_api=base_url+edit_observation_api+observe_id
                # print(edit_api)
                # for observation in observe:
                    
                edit_observation=request.form['edit_observation']
                payload={
                    "observe":edit_observation
                }
                api_data=json.dumps(payload)
                # print('api_data',api_data)
                edit_observation_submit=requests.patch(base_url+edit_observation_api+observe_id, data=api_data, headers=headers)
                edit_observation_response=json.loads(edit_observation_submit.text)
                # print(edit_observation_submit.status_code)
                # print(edit_observation_response)
                if edit_observation_submit.status_code == 200 :
                    flash("Observation updated", "success")
                else:
                    flash("Something went wrong please try again..", "error")

            if request.form['form_type'] == 'delete_observation':
                # print("delete_observation")
                active_tab="observation"
                observation_id=request.form['observation_id']
                observe_id=f'{observation_id}/'
                # print(observe_id)
                # del_api=base_url+delete_observation_api+observe_id
                # print(del_api)
                delete_observation_submit=requests.delete(base_url+delete_observation_api+observe_id, headers=headers)
                # print(delete_observation_submit.status_code)
                # del_obs = delete_observation_submit.json()
                # print(delete_observation_submit.text)
                if (delete_observation_submit.status_code == 200) or (delete_observation_submit.status_code == 204) :
                    flash("Observation deleted", "success")
                else:
                    flash("Something went wrong please try again..", "error")

            if request.form['form_type'] == 'upload_prescription':
                active_tab="prescription"
                # print(active_tab)
                # print("upload prescription")
                file_headers={
                    'files' : 'multipart/form-data'
                }
                prescription_file = request.files["prescription_file"]
                sourceFileName = secure_filename(prescription_file.filename)
                # print(sourceFileName)
                # cwd = os.getcwd()+'/'
                # print(cwd)
                # if 'temp' not in os.listdir(cwd):
                #     os.mkdir(cwd + 'temp')
                # prescription_file.save(os.path.join(cwd + 'temp', sourceFileName))

                # with open(cwd + 'temp/'+ sourceFileName, 'rb') as f:
                #     # data_file = {
                #     #     "common_file":(sourceFileName, 'rb')
                #     # }
                #     data_file = {
                #         "common_file":(sourceFileName, f)
                #     }

                print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                prescription_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', sourceFileName))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ sourceFileName)
                # print(file_stats)
                file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                print(file_size)
                print(f'{file_stats.st_size / (1024)} KB')
                print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ sourceFileName, 'rb') as f:
                    # data_file = {
                    #     "common_file":(sourceFileName, 'rb')
                    # }
                    data_file = {
                        "common_file":(sourceFileName, f)
                    }
                    print(data_file)
                    data={
                    'appointment_id': id,
                    }
                    # print(data)
                    api_data=json.dumps(data)
                    file_uploader_api=base_url+file_upload_api
                    # print(file_uploader_api)
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    # print(file_upload_submit.status_code)                    
                    file_upload_response=json.loads(file_upload_submit.text)
                    # print(file_upload_response)
                    if file_upload_response['common_file']:
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', sourceFileName))
                    # print(file_upload_submit.status_code)
                    # ""  Fetching File Path From Response and Passing it to Prescription API  ""
                    prescription_path=file_upload_response['common_file']
                    # print(prescription_path)
                    # print(base_url+prescription_api)
                    data={
                        "appointment_id":id,
                        "prescription":str(prescription_path),
                        "file_size":file_size,
                        "file_name":sourceFileName,
                        
                    }
                    api_data=json.dumps(data)
                    # print(api_data)
                    prescription_submit=requests.post(base_url+prescription_api,data=api_data,headers=headers)
                    # print(prescription_submit.status_code)
                    prescription_response=json.loads(prescription_submit.text)
                    # print(prescription_response)

                # print("upload prescription")
                # file_headers={
                #     'files' : 'multipart/form-data'
                # }
                # print("error 1")
                # prescription_file=request.files['customFile']
                # print("error2")
                # print(prescription_file)
                # # prescription_file.save(secure_filename(prescription_file.filename))
                # filename=(secure_filename(prescription_file.filename))
                # # path=prescription_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # # print("",path)
                # print("error3")
                # print(filename)
                # data={
                #     'appointment_id': id,
                # }
                # print(data)
                # api_data=json.dumps(data)
                # files={
                #     'document' : open(filename,'rb'),
                # }
                # # jfile=json.dumps(jfile)
                # # print(jfile)
                # print("files :",files)
                
                # prescription_submit=requests.post(base_url+prescription_api, files=files, data=api_data, headers=file_headers)
                # prescription_submit_response=json.loads(prescription_submit.text)
                # print(prescription_submit.status_code)
                # print(prescription_submit_response)
                # print(prescription_submit.status_code)

            if request.form['form_type'] == 'prescription': 
                active_tab="prescription"
                print(active_tab)
                print("prescription")       
                # prescription=request.form['prescription']
                # data={
                #     "appointment_id":id,
                #     "prescriptions_text":prescription,
                #     "doctor_id":doctor_id
                # }
                try:
                    remarks=request.form['prescription_remarks']
                    tests=request.form['tests']
                    counts=request.form['count']
                    # print("counts",counts)
                    medication_list=[]
                    medication_dict={}
                    print(request.form['prescription_remarks'])
                    # can_substitute=request.form.get('can_substitute_1')
                    # print("sub",can_substitute)
                    
                    # * here dynamic elements value is fetched by for loop *
                    # * count is the number of prescription rows added in the pop up *
                    print(counts)
                    for count in range(1,int(counts)+1):
                        print("count",count)
                        print(f'medicine{count}')                
                        # medication_dict['medicine']=request.form[f'medicine{count}']            
                        # medication_dict['duration_number']=request.form[f'number{count}']           
                        # print(medicine)
                        # print(duration_number)
                        can_sub_checkbox=request.form.get(f'can_substitute_{count}')
                        print(can_sub_checkbox)
                        
                        if can_sub_checkbox=='1':
                            # medication_dict['can_substitute'] = 1
                            can_substitute = 1
                        else:
                            can_substitute = 0
                        print("can sub",can_substitute)
                            # medication_dict['can_substitute'] = 0
                        try:
                            print("d",medication_dict['can_substitute'])
                        except Exception as e:
                            print(e)
                        try:
                            medication_dict={
                                "medicine":request.form[f'medicine{count}'] ,
                                "duration_number":request.form[f'number{count}'],
                                "duration":request.form[f'dosage_duration{count}'],
                                "side_effects":request.form[f'side_effects{count}'],
                                "consumption_detail":request.form[f'when_{count}'],
                                "consumption_time":request.form.getlist(f'medicine_time_{count}'),
                                "can_substitute":can_substitute,
                            
                                # "is_substitute":request.form.get(f'can_substitute_{count}')
                            }
                            medication_list.append(medication_dict)
                        except Exception as e:
                            print(e)
                        print(medication_list)
                    print("medication list",medication_list)
                    print(counts)
                    data={
                        "appointment_id":id,
                        "prescriptions_text":remarks,
                        "doctor_id":doctor_id,
                        "tests_to_be_done":tests,
                        "medications":medication_list,
                        "prescription_validation":request.form['prescription_validation']
                    }
                    json_data=json.dumps(data)
                    print("prescription request :", json_data)
                    try:
                        prescription_text_submit=requests.post(base_url+prescription_text_api, data=json_data, headers=headers)
                        prescription_text_submit_response=json.loads(prescription_text_submit.text)
                        print(prescription_text_submit_response)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                # print(prescription_text_submit.status_code)

            if request.form['form_type'] == 'edit_prescription':
                # print("edit_prescription")
                active_tab="prescription"
                # print(active_tab)
                prescription_id=request.form['prescription_id']
                prescript_id=f'{prescription_id}/'
                # print(prescript_id)
                edit_api=base_url+prescription_edit_api+prescript_id
                # print(edit_api)
                # for prescription in prescript_text:
                    
                # edit_prescription=request.form['edit_prescription']
                # payload={
                #     "prescriptions_text":edit_prescription
                #   }
                edit_remarks=request.form[f'edit_prescription_remarks{prescription_id}']
                edit_tests=request.form[f'edit_tests{prescription_id}']
                counts=request.form[f'edit_count{prescription_id}']
                edit_medication_list=[]
                edit_medication_dict={}
                # * here dynamic elements value is fetched by for loop *
                # * count is the number of prescription rows added in the pop up *
                for count in range(1,int(counts)+1):
                    # print("count",count)
                    can_sub_checkbox=request.form.get(f'edit_can_substitute_{prescription_id}_{count}')
                    # print(can_sub_checkbox)
                    
                    if can_sub_checkbox=='1':
                        # medication_dict['can_substitute'] = 1
                        can_substitute = 1
                    else:
                        can_substitute = 0
                    # print("can sub",can_substitute)
                    edit_medication_dict={
                        "medication_id":request.form[f'medication_id{prescription_id}_{count}'] ,
                        "prescription_id":prescription_id ,
                        "medicine":request.form[f'edit_medicine{prescription_id}_{count}'] ,
                        "duration_number":request.form[f'edit_number{prescription_id}_{count}'],
                        "duration":request.form[f'edit_dosage_duration{prescription_id}_{count}'],
                        "side_effects":request.form[f'edit_side_effects{prescription_id}_{count}'],
                        "consumption_detail":request.form[f'edit_when_{prescription_id}_{count}'],
                        "consumption_time":request.form.getlist(f'edit_medicine_time_{prescription_id}_{count}'),
                        "can_substitute":can_substitute
                    }
                    edit_medication_list.append(edit_medication_dict)
                # print("edited medication list",edit_medication_list)
                # print(counts)
                payload={
                    "appointment_id":id,
                    "prescriptions_text":edit_remarks,
                    "doctor_id":doctor_id,
                    "tests_to_be_done":edit_tests,
                    "medications":edit_medication_list,
                }
                api_data=json.dumps(payload)
                # print('api_data',api_data)
                edit_prescription_submit=requests.patch(base_url+prescription_edit_api+prescript_id, data=api_data, headers=headers)
                edit_prescription_response=json.loads(edit_prescription_submit.text)
                # print(edit_prescription_submit.status_code)
                # print(edit_prescription_submit.text)

            if request.form['form_type'] == 'delete_prescription':
                # print("delete_prescription")
                active_tab="prescription"
                # print(active_tab)
                prescription_id=request.form['prescription_id']
                prescript_id=f'{prescription_id}/'
                # print(prescript_id)
                # del_api=base_url+prescription_api+prescript_id
                # print(del_api)
                delete_prescription_submit=requests.delete(base_url+delete_prescription_api+prescript_id, headers=headers)
                # print(delete_prescription_submit.status_code)
                # print(delete_prescription_submit.text)

            if request.form['form_type'] == 'follow_up':
                print("follow_up")
                active_tab="followup"
                # print(active_tab)
                if request.form['follow_up_reminder'] == 'doctor':
                    # print("create follow up")
                    appointment_date=request.form['follow_up_date']
                    appointment_time=request.form['follow_up_time']
                    # print(appointment_time)
                    remarks=request.form['remarks']
                    # remarks=""
                    # for another speciality doctor
                    # if request.form['follow_up_type'] == 'another_doctor':
                    #     followup_doctor=request.form['followup_doctor']
                    # else :
                    #     followup_doctor = ""
                    followup_doctor = ""
                    payload={
                                "new_user":0,
                                "user_id":user_id,
                                "appointment_date":appointment_date,
                                "appointment_time":appointment_time,
                                "followup_id":id,
                                "category_id":category_id,
                                "type_booking":"followup",
                                "doctor_id":doctor_id,
                                "doctor_flag":doctor_flag,
                                "remarks":remarks,
                                "appointment_status":8,
                                "followup_created_by":"doctor",
                                "followup_created_doctor_id":doctor_id,
                                "followup_doctor":followup_doctor,
                                "specialization": "",
                                "language_pref":"",
                                "gender_pref":""
                    }
                    api_data=json.dumps(payload)
                    # print(api_data)
                    follow_up_submit=requests.post(base_url+follow_up_api, data=api_data, headers=headers)
                    follow_up_response=json.loads(follow_up_submit.text)
                    # print("followup",follow_up_submit.status_code)
                    # print(follow_up_response)
                    if follow_up_response['response_code'] == 200:
                        flash("Follow up appointment created","success")
                    else:
                        flash("Something went wrong.. Try again.","error")

                # reminder for the customer
                if request.form['follow_up_reminder'] == 'customer_reminder':
                    # print("create reminder")
                    
                    # follow_up_type=request.form['follow_up_type']
                    # remarks=request.form['remarks']
                    # followup_duration=request.form['followup_duration']
                    # reminder_payload={
                    #                 "appointment_id":id,
                    #                 "follow_up_for":follow_up_type,
                    #                 "remarks":remarks,
                    #                 "duration":followup_duration
                    #             }
                    follow_up_type="self"
                    remarks=request.form['remarks']
                    duration=request.form['duration_number']+" "+request.form['duration_time']
                    # duration_number=request.form['duration_number']
                    # duration=request.form['duration_time']
                    
                    reminder_payload={
                                    "appointment_id":id,
                                    "follow_up_for":follow_up_type,
                                    "remarks":remarks,
                                    "duration":duration
                                }
                    reminder_api_data=json.dumps(reminder_payload)
                    # print("reminder payload",reminder_api_data)
                    followup_reminder_request=requests.post(base_url+create_followup_reminder_api,data=reminder_api_data, headers=headers)
                    followup_reminder_response=json.loads(followup_reminder_request.text)
                    # print("followup reminder",followup_reminder_request.status_code)
                    # print(followup_reminder_response)
                    flash("Reminder sent to patient","success")

            # follow up appointment with another specialist
            if request.form['form_type'] == 'refer_another_specialist':
                print("refer another specialist")
                active_tab="followup"
                print(active_tab)
                # if request.form['follow_up_reminder'] == 'doctor':
                #     print("create follow up")
                appointment_date=request.form['refer_app_date']
                appointment_time=request.form['refer_time']
                print(appointment_time)
                remarks=request.form['refer_remarks']
                language=request.form['refer_language']
                gender=request.form['refer_doc_gender']
                specialization = request.form['refer_specialization']
                # for another speciality doctor
                # if request.form['follow_up_type'] == 'another_doctor':
                #     followup_doctor=request.form['followup_doctor']
                # else :
                #     followup_doctor = ""
                # followup_doctor = request.form['refer_doctor']
                followup_doctor=""
                payload={
                            "new_user":0,
                            "user_id":user_id,
                            "appointment_date":appointment_date,
                            "appointment_time":appointment_time,
                            "followup_id":id,
                            "category_id":category_id,
                            "type_booking":"followup",
                            "doctor_id":doctor_id,
                            "doctor_flag":doctor_flag,
                            "remarks":remarks,
                            "appointment_status":2,
                            "followup_created_by":"doctor",
                            "followup_created_doctor_id":doctor_id,
                            "followup_doctor":followup_doctor,
                            "specialization": specialization,
                            "language_pref":language,
                            "gender_pref":gender
                }
                api_data=json.dumps(payload)
                # print(api_data)
                follow_up_submit=requests.post(base_url+follow_up_api, data=api_data, headers=headers)
                follow_up_response=json.loads(follow_up_submit.text)
                print("followup",follow_up_submit.status_code)
                # print(follow_up_response)
                if follow_up_response['response_code'] == 200:
                    flash("Follow up appointment created","success")
                else:
                    flash("Something went wrong.. Try again.","error")

            # reminder for appointment with another specialist
            if request.form['form_type'] == 'refer_another_reminder':
                print("refer another reminder")
                
                # follow_up_type=request.form['follow_up_type']
                # remarks=request.form['remarks']
                # followup_duration=request.form['followup_duration']
                # reminder_payload={
                #                 "appointment_id":id,
                #                 "follow_up_for":follow_up_type,
                #                 "remarks":remarks,
                #                 "duration":followup_duration
                #             }
                follow_up_type="another_doctor"
                remarks=request.form['reminder_remarks']
                duration=request.form['refer_duration_number']+" "+request.form['refer_duration_time']
                specialization=request.form['refer_specialization']
                # duration_number=request.form['duration_number']
                # duration=request.form['duration_time']
                
                reminder_payload={
                                "appointment_id":id,
                                "follow_up_for":follow_up_type,
                                "remarks":remarks,
                                "duration":duration,
                                # "specialization":specialization
                            }
                reminder_api_data=json.dumps(reminder_payload)
                # print("reminder payload",reminder_api_data)
                followup_reminder_request=requests.post(base_url+create_followup_reminder_api,data=reminder_api_data, headers=headers)
                followup_reminder_response=json.loads(followup_reminder_request.text)
                print("followup reminder",followup_reminder_request.status_code)
                # print(followup_reminder_response)
                if followup_reminder_response['response_code']==200:
                    flash("Reminder sent to patient","success")
                else:
                    flash("Something went wrong.. Please try again.","error")

            if request.form['form_type'] == 'analysis': 
                print("analysis")       
                # active_tab="attachment"
                analysis_text=request.form['analysis']
                data={
                    "appointment_id":id,
                    "analysis_text":analysis_text,
                    "doctor_id":doctor_id
                }
                json_data=json.dumps(data)
                # print(json_data)
                analysis_text_submit=requests.post(base_url+analysis_text_api, data=json_data, headers=headers)
                analysis_text_submit_response=json.loads(analysis_text_submit.text)
                # print(analysis_text_submit_response)
                # print(analysis_text_submit.status_code)

            if request.form['form_type'] == 'upload_assessment':
                # print("upload assessment")
                active_tab="attachment"
                file_headers={
                    'files' : 'multipart/form-data'
                }
                assessment_file=request.files['customFile']
                # print(assessment_file)
                # filename=secure_filename(assessment_file.filename)            
                up_file=secure_filename(assessment_file.filename)
                # print("upfile",up_file)
                # files={
                #     'common_file' : open(filename,'rb')
                # }
                # files={
                #     'common_file' : open(up_file,'rb')
                # }
                # print(files)
                # data={
                #     'appointment_id': id,
                #     'file_flag':'analysis_info'
                # }

                # print("BASE_DIR : ",BASE_DIR)
                if 'temp' not in os.listdir(BASE_DIR):
                    os.mkdir(str(BASE_DIR) + '/' + 'temp')
                assessment_file.save(os.path.join(str(BASE_DIR) +'/' + 'temp', up_file))

                file_stats = os.stat(str(BASE_DIR) + '/' + 'temp/'+ up_file)
                # print(file_stats)
                file_size=f'{round(file_stats.st_size / (1024 * 1024),2)} MB'
                # print(file_size)
                # print(f'{file_stats.st_size / (1024)} KB')
                # print(f'{file_stats.st_size / (1024 * 1024)} MB')

                with open(str(BASE_DIR) + '/' + 'temp/'+ up_file, 'rb') as f:    
                    data_file = {
                        "common_file":(up_file, f)
                    }
                    # api_data=json.dumps(data)
                    file_uploader_api=base_url+file_upload_api
                    file_upload_submit = requests.post(file_uploader_api,files=data_file,)
                    file_upload_response=json.loads(file_upload_submit.text)
                    # print(file_upload_response)
                    if file_upload_response['common_file']:
                        # delete the photo file from the temporary directory
                        os.remove(os.path.join(str(BASE_DIR) +'/' + 'temp', up_file))
                    # print(file_upload_submit.status_code)

                    # ""  Fetching File Path From Response and Passing it to Analysis info API  ""
                    analysis_path=file_upload_response['common_file']
                    # print(analysis_path)
                    # print(base_url+analysis_text_api)
                    data={
                        "appointment_id":id,
                        "doctor_id":user_id,
                        "analysis_path":str(analysis_path),
                        "file_size":file_size,
                        "file_name":up_file,
                        "operation_flag":"file"
                    }
                    api_data=json.dumps(data)
                    # print(api_data)
                    assessment_submit=requests.post(base_url+analysis_text_api,data=api_data,headers=headers)
                    # print(assessment_submit.status_code)
                    assessment_response=json.loads(assessment_submit.text)
                    # print(assessment_response)

            if request.form['form_type'] == 'escalate': 
                print("escalate")       

                specialization=request.form['specialization']
                # doctor=request.form['doctor']
                appointment_date=request.form['appointment_date']
                appointment_time=request.form['appointment_time_1']
                # print(appointment_time)
                language=request.form['language']
                doc_gender=request.form['doc_gender']
                session_type=request.form['session_type']

                data={
                    # "doctor_id":doctor,
                    "appointment_id":id,
                    "appointment_status":2,
                    "appointment_date":appointment_date,
                    "time_slot":appointment_time,
                    "language_pref":language,
                    "gender_pref":doc_gender,
                    "user_id":user_id,
                    "specialization":specialization,
                    "session_type":session_type                  
                }
                
                json_data=json.dumps(data)
                print(json_data)
                escalate_submit=requests.post(base_url+escalate_api, data=json_data, headers=headers)
                escalate_submit_response=json.loads(escalate_submit.text)
                's'
                # print(escalate_submit_response)
                # print(escalate_submit.status_code)
                if escalate_submit_response['message'] == 'Order Escalated':
                    flash("Order Referred","success")
                else:
                    flash("Something went wrong","error")

            # senior doctor transfer
            if request.form['form_type'] == 'transfer': 
                # print("transfer")       

                # specialization=request.form['doctor_specialization']
                # doctor=request.form['transfer_doctor']
                appointment_date=request.form['transfer_app_date']
                appointment_time=request.form['transfer_app_time']
                # language=request.form['doctor_language']
                # doc_gender=request.form['doctor_gender']

                data={
                    # "new_doctor_id":doctor,
                    "doctor_id":doctor_id,
                    "appointment_id":id,
                    "appointment_status":11,
                    "appointment_date":appointment_date,
                    "time_slot":appointment_time,
                    
                    # "language_pref":language,
                    # "gender_pref":doc_gender
                }
                
                json_data=json.dumps(data)
                # print(json_data)
                transfer_submit=requests.post(base_url+transfer_api, data=json_data, headers=headers)
                transfer_submit_response=json.loads(transfer_submit.text)
                # print(transfer_submit_response)
                # print(transfer_submit.status_code)
                if transfer_submit_response['message'] == 'No Doctors Available':
                    flash("No available doctors","error")
                else:
                    flash("Patient transferred","success")

            if request.form['form_type'] == 'junior_doctor_transfer': 
                # print("transfer")       

                # specialization=request.form['doctor_specialization']
                # doctor=request.form['transfer_doctor']
                # appointment_date=request.form['date']
                # appointment_time=request.form['time']
                # language=request.form['doctor_language']
                # doc_gender=request.form['doctor_gender']

                data={
                    # "new_doctor_id":doctor,
                    "doctor_id":doctor_id,
                    "appointment_id":id,
                    "appointment_status":10,
                    "appointment_date":appointment_details['appointment_date'],
                    "appointment_time":appointment_details['appointment_time_slot_id'],               
                    "language_pref":appointment_details['language_pref'],
                    "gender_pref":appointment_details['gender_pref']
                }
                
                json_data=json.dumps(data)
                # print(json_data)
                transfer_submit=requests.post(base_url+junior_doctor_transfer_api, data=json_data, headers=headers)
                # print(transfer_submit.status_code)
                transfer_submit_response=json.loads(transfer_submit.text)
                # print(transfer_submit_response)
                if transfer_submit_response['response_code'] == 400:
                    flash("No available doctors","error")   
                else:
                    flash("Patient transferred","success")            

            return redirect(url_for('order_detail', id=id, active_tab=active_tab))
        print('2916 ',appointment_details)
        return render_template('appointment_details.html',appointment_details=appointment_details,follow_ups=follow_ups,
        observations=observations,doctors=doctor_list,languages=languages,specializations=specializations,active_tab=active_tab)
    except Exception as e:
        print("Exception :",e)
        return redirect(url_for('doctor_dash'))


# @app.route("/delete_prescription/<int:id_to_delete>")
# def delete_prescription(id_to_delete):
#     return redirect(url_for('order_detail',))

@app.route("/add_observation/<int:appointment_id>",methods=['GET','POST'])
def add_observation(appointment_id):
    if 'user_id' in session:
        doctor_id=session['user_id']
        print("doc id",doctor_id)
    else:
        return redirect(url_for('login'))
    
    if 'doctor_flag' in session:
        doctor_flag=session['doctor_flag']
        print(doctor_flag)

    headers={
            "Content-type":"application/json"
    }
    print(appointment_id)
    payload={
        "appointment_id":appointment_id,
        "user_id":"",
        "file_flag":"",
        "doctor_id":doctor_id
    }
    api_data=json.dumps(payload)
    print(api_data)
    appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
    appointment_detail_response=json.loads(appointment_detail.text)
    appointment_details=appointment_detail_response['data']
    print("detail api :",appointment_detail.status_code)
    user_id=appointment_details['user_id']
    print(user_id)
    if request.method == 'POST':
        print("observation")       
        observations=request.form['observations']
        data={
                "appointment_id":appointment_id,
                "observations":observations,
                "doctor_id":doctor_id
        }
        json_data=json.dumps(data)
        print(json_data)
        observation_submit=requests.post(base_url+observations_api, data=json_data, headers=headers)
        observation_submit_response=json.loads(observation_submit.text)
        print("post response:",observation_submit.status_code)
        print(observation_submit_response)
        return redirect(url_for('action_doctor',actions=6,appointment_id=appointment_id))
    return render_template("add_observation.html", appointment_details=appointment_details)

@app.route("/new_appointment",methods=['GET','POST'])
def new_appointment():
    try:
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)
        headers = {
            "Content-Type":"application/json"
        }
        # customer list api call
        payload={
            "operation_flag":"view"
        }
        api_data=json.dumps(payload)
        customer_list_request=requests.post(base_url+customer_list_api, data=api_data, headers=headers)
        customer_list_response=json.loads(customer_list_request.text)
        print(customer_list_request.status_code)
        customers=customer_list_response['data']
        # doctor list api call
        doctor_listing=requests.post(base_url+doctor_listing_api, headers=headers)
        doctor_list_response=json.loads(doctor_listing.text)
        print(doctor_listing.status_code)
        doctors = doctor_list_response['data']
       
        # language api call
        language_api_request=requests.get(base_url+language_api,headers=headers)
        print(language_api_request.status_code)
        language_api_response=json.loads(language_api_request.text)
        languages=language_api_response['data']
        #specializations list api call
        specialization_request=requests.get(base_url+specialization_list_api, headers=headers)
        specialization_response=json.loads(specialization_request.text)
        print(specialization_request.status_code)
        specializations=specialization_response['data']
        print(specializations)
        #specialization filter api call
        # payload2={}
        # specialization_filter = requests.post(base_url+specialization_filter_api,data=api_data2, headers=headers)
        # new appointment creation with follow up api
        if request.method == 'POST':
            print("post")
            customer_id=request.form['customer_id']
            category_id=request.form['category_id']
            specialization=request.form['specialization']
            appointment_date=request.form['date']
            appointment_time=request.form['time']
            doctor_gender=request.form['doc_gender']
            language=request.form['language']
            senior_doctor_id=request.form['doctor']
            # remarks=request.form['remarks']
            payload={
                        "new_user":0,
                        "user_id":customer_id,
                        "appointment_date":appointment_date,
                        "appointment_time":appointment_time,
                        "followup_id":"",
                        "category_id":category_id,
                        "type_booking":"regular",
                        "gender_pref":doctor_gender,
                        "language_pref":language,
                        "doctor_id":senior_doctor_id,
                        "doctor_flag":1,
                        "remarks":"",
                        "appointment_status":12,
                        "specialization": ""
            }
            api_data=json.dumps(payload)
            print(api_data)
            new_appointment_request=requests.post(base_url+follow_up_api, data=api_data, headers=headers)
            new_appointment_response=json.loads(new_appointment_request.text)
            print(new_appointment_request.status_code)
            print(new_appointment_response)
        return render_template("new_appointment.html",customers=customers,doctors=doctors,languages=languages,specializations=specializations)
    except Exception as e:
        print(e)
    return render_template("new_appointment.html")



@app.route("/earnings/")
def earnings():
    try:
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)
        headers = {
            "Content-Type":"application/json"
        }
        
        payload={
                    "appointment_status" : [12,8],
                    "user_id":"",
                    "doctor_flag":""
                }
        api_data=json.dumps(payload)
        print(api_data)  
        #calling appointment listing function  
        all_recent_orders=appointment_listing(api_data)
        if all_recent_orders:
        # selecting only first 4 recent orders to show in table
            recent_orders=all_recent_orders[0:4]
            print("recent orders",len(recent_orders))
        else:
            recent_orders=[]
        # print(recent_orders)
        payout_payload={
            "doctor_id":doctor_id,
            "payout_status":""
        }
        payout_json_data=json.dumps(payout_payload)
        payout_request=requests.post(base_url+payout_list_api, data=payout_json_data, headers=headers)
        print("payout",payout_request.status_code)
        payout_response=json.loads(payout_request.text)
        payouts=payout_response['data']
        print("payouts",payouts)
        # print("error")
        payout_data=payouts['payouts']
        print("payouts list",payout_data)
        if payouts['payouts']:
            print("no error")
            print("recent",payouts['payouts'])
            payouts_len=len(payout_data)
            print(payouts_len)
            recent_payouts=payout_data[0:4]
            print("4",recent_payouts)
        else:
            recent_payouts=[]
        return render_template('earnings.html',recent_orders=recent_orders,payouts=payouts,recent_payouts=recent_payouts,payout_data=payout_data)
    except Exception as e:
        print("earnings page error:",e)

    return render_template('earnings.html')

# def get_slot_time(time_slot,date= None):
#     try:
#         start_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[0].strip(), '%I%p').time())
#         end_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[1].strip(), '%I%p').time())
#         print("start time", start_time)
#         print("end time", end_time)
#         return  start_time,end_time
#     except Exception as e:
#         # return None,None
#         # """For testing Purpose """
#         print(e)
#         try:
#             start_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[0].strip(), '%I:%M%p').time())
#             end_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[1].strip(), '%I:%M%p').time())
#         except:
#             start_time = str(date)+"T"+str(datetime.strptime(time_slot,'%H').time())
#             end_time = str(date)+"T"+str(datetime.strptime(time_slot,'%H').time())
#         return start_time,start_time

def get_slot_time(time_slot, date=None):
    try:
        start_time = str(date) + "T" + str(datetime.strptime(time_slot.split('-')[0].strip(), '%I%p').time())
        end_time = str(date) + "T" + str(datetime.strptime(time_slot.split('-')[1].strip(), '%I%p').time())
        print("start time", start_time)
        print("end time", end_time)
        return start_time, end_time
    except ValueError as e:
        print("except",e)
        try:
            start_time = str(date) + "T" + str(datetime.strptime(time_slot.split('-')[0].strip(), '%I:%M%p').time())
            end_time = str(date) + "T" + str(datetime.strptime(time_slot.split('-')[1].strip(), '%I:%M%p').time())
        except ValueError:
            start_time = str(date) + "T" + str(datetime.strptime(time_slot, '%H:%M%p').time())
            end_time = str(date) + "T" + str(datetime.strptime(time_slot, '%H:%M%p').time())
        return start_time, end_time

def get_jr_dr_slot_time(time_slot,date= None):
    try:
        start_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[0].strip(), '%I%p').time())
        end_time = str(date)+"T"+str(datetime.strptime(time_slot.split('-')[1].strip(), '%I%p').time())
        print("start time", start_time)
        print("end time", end_time)
        return  start_time,end_time
    except Exception as e:
        # return None,None
        # """For testing Purpose """
        print(e)
        print("exception")
        start_time = str(date)+"T"+str(datetime.strptime(time_slot,'%H').time())
        end_time = str(date)+"T"+str(datetime.strptime(time_slot,'%H').time())
    return start_time,start_time

from datetime import datetime, timedelta

@app.route("/calendar",methods=['POST','GET'])
def calendar():
    try:
        headers = {
            "Content-Type":"application/json"
        }  
        if 'username' in session:
            check_user = requests.post(base_url+'/api/doctor/is_dr_blocked/', data=json.dumps({'email':session['username']}), headers=headers)
            res_check_user = json.loads(check_user.text)
            print('res_check_user',res_check_user)
            if res_check_user['status'] == 'blocked':
                session.clear()
                return redirect(url_for('login'))
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)
            if doctor_flag == 1:
                appointment_status = [2,7,11,12,8]
            elif doctor_flag == 2:
                appointment_status = [1,7,8,10]
            else:
                appointment_status = None
        else:
            doctor_flag = None
            appointment_status = None
        headers = {
            "Content-Type":"application/json"
        }
        
        print('session ',session)
        payload={
            "doctor_id":doctor_id,
            "doctor_flag":doctor_flag
        }
        api_data=json.dumps(payload)
        print(api_data)
        print('asdfasdfasdfasdfasdf')
        # work hour timeslot api call
        timeslot_list_request=requests.post(base_url+time_slot_list_api, data=api_data, headers=headers)
        timeslot_list_response=json.loads(timeslot_list_request.text)
        print(timeslot_list_response)
        timeslots = timeslot_list_response['data']
        days = timeslot_list_response['weekday']

        event_list = []
        if doctor_flag and appointment_status:
            payload1={
                        "appointment_status" : appointment_status,
                        "user_id":doctor_id,
                        "doctor_flag":doctor_flag,
                        }
            api_data=json.dumps(payload1)

            orders=appointment_listing(api_data)
            #print(orders)
            for order in orders:
                event_dict = {}
                if doctor_flag == 1:
                    print("here")
                    start,end = order['time_slot'],order['appointment_date']
                else:
                    print("jr doc")
                    start,end = order['time_slot'],order['appointment_date']

                event_dict['id'] = 'default-event-id-'+str(order['appointment_id'])
                event_dict['title'] = 'Appointment for'+' '+ str(order['user_fname']) + ' ' + str(order['user_lname'])
                event_dict["start"] = start
                event_dict["end"] = end
                event_dict["className"] = "fc-event-danger"
                event_dict["type"]="appointment"
                if order['meeting_link']:
                    event_dict["description"] = order['meeting_link']
                event_list.append(event_dict)
        
        work_hr_payload={
                "doctor_id":doctor_id
        }
        work_hr_json=json.dumps(work_hr_payload)
        work_hours_list_req=requests.post(base_url+calendar_view_api, data=work_hr_json, headers=headers)
        work_hours_list_resp=json.loads(work_hours_list_req.text)
        print(work_hours_list_resp)
        work_hours_list=work_hours_list_resp['data']
        doctors_working_hr=[]
        print(work_hours_list)
        if len(work_hours_list) > 0:
            for work_hour in work_hours_list:
                work_hour_dict = {}
                work_hour_dict['id'] = str(work_hour['id'])
                work_hour_dict['date'] = str(work_hour['date'])
                work_hour_dict['title'] = 'Work hours'
                work_hour_dict["className"] = "fc-event-info"
                work_hour_dict["type"]="working_hours"
                work_hour_dict['timeslots']=work_hour['time_slots'] if work_hour['time_slots'] else ''
                event_list.append(work_hour_dict)
        print(doctors_working_hr)

        if request.method =='POST':
            print("form")
            print('3276 ',request.data)
            if request.form['form_type']=="edit":
                print("edit")
                updated_slots = request.form.getlist('slots')
                print('line 3278 ',updated_slots)
                update_wh_payload={ 
                    "slots":updated_slots,
                    "doctor_id":doctor_id,
                    "date":request.form['date']
                }
                print(update_wh_payload)
                update_work_hr_json=json.dumps(update_wh_payload)      
                update_working_hours_request=requests.post(base_url+calendar_edit_api, data=update_work_hr_json, headers=headers)
                'ss'
                print(update_working_hours_request.status_code)
                update_working_hours_response=json.loads(update_working_hours_request.text)
                print(update_working_hours_response) 
                return redirect(url_for('calendar'))
            
            if request.form['form_type']=="add":
                print("add")
                date=request.form['wh_date']
                add_slots = request.form.getlist('add_slots')
                add_wh_payload={ 
                    "slots":add_slots,
                    "doctor_id":doctor_id,
                    "date":date
                }
                print(add_wh_payload)
                add_work_hr_json=json.dumps(add_wh_payload)   
                print(add_work_hr_json)   
                add_w_hr_req=requests.post(base_url+calendar_add_api, data=add_work_hr_json, headers=headers)
                print(add_w_hr_req.status_code)
                add_w_hr_resp=json.loads(add_w_hr_req.text) 
                print(add_w_hr_resp)
                return redirect(url_for('calendar'))

       

        return render_template('calendar.html',orders=orders,event_list=event_list ,work_hours_list=work_hours_list, timeslots=timeslots,doctors_working_hr=doctors_working_hr)
    except Exception as e:
        print(e)
        return render_template('calendar.html')

@app.route("/report_customer/<int:appointment_id>")
def report_customer(appointment_id):
    try:
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)
        headers = {
            "Content-Type":"application/json"
        }
        payload={
        "appointment_id":appointment_id,
        "user_id":"",
        "file_flag":"",
        "doctor_id":doctor_id
        }
        api_data=json.dumps(payload)
        print(api_data)
        appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
        appointment_detail_response=json.loads(appointment_detail.text)
        appointment_details=appointment_detail_response['data']
        print("detail api :",appointment_detail.status_code)
        user_id=appointment_details['user_id']
        data={
            "appointment_id":appointment_id,
            "customer_id":user_id,
            "doctor_id":doctor_id
        }
        api_data2=json.dumps(data)
        print(api_data2)
        report_customer_request=requests.post(base_url+report_customer_api,data=api_data2,headers=headers)
        print("report customer ",report_customer_request.status_code)
        report_customer_response=json.loads(report_customer_request.text)
        print("report customer :",report_customer_response)
        flash("Customer Reported","info")
        return redirect(url_for('order_detail',id=appointment_id))
    except Exception as e:
        print(e)
    return redirect(url_for('order_detail',id=appointment_id))

@app.route("/discussion/<int:appointment_id>", methods=['GET','POST'])
def discussion(appointment_id):
    try:
        if 'user_id' in session:
            doctor_id=session['user_id']
            print(doctor_id)
        else:
            return redirect(url_for('login'))
        headers={
        "Content-Type":"application/json"
        }
        # calling discussion list api
        payload={
            "appointment_id":appointment_id
        }
        api_data=json.dumps(payload)
        discussion_list_request=requests.post(base_url+discussion_list_api, data=api_data, headers=headers)
        discussion_list_response=json.loads(discussion_list_request.text)
        print("discussion list", discussion_list_request.status_code)
        discussion_list=discussion_list_response['data']
        limit = discussion_list_response['discussion_count']
        # print(discussion_list)

        # calling detail api:            
        if 'doctor_flag' in session:
            doctor_flag=session['doctor_flag']
            print(doctor_flag)

        payload={
            "appointment_id":appointment_id,
            "user_id":"",
            "file_flag":"",
            "doctor_id":doctor_id
        }
        api_data=json.dumps(payload)
        print(api_data)
        appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
        appointment_detail_response=json.loads(appointment_detail.text)
        appointment_details=appointment_detail_response['data']
        print("detail api :",appointment_detail.status_code)

        # calling create discussion api
        if request.method == 'POST' :
            # limit=request.form['form_type']
            # print(limit)
            if limit != 3:
                discuss_text=request.form['discuss_text']
                create_payload={
                        "appointment_id":appointment_id,
                        "content":discuss_text,
                        "is_query":0,
                        "is_reply":1,
                        "doctor_id":doctor_id
                    }
                create_api_data=json.dumps(create_payload)
                print("create discussion payload",create_api_data)
                create_discussion_request=requests.post(base_url+create_discussion_api, data=create_api_data, headers=headers)
                create_discussion_response=json.loads(create_discussion_request.text)
                print("create discussion", create_discussion_request.status_code)
                print(create_discussion_request.text)
                return redirect(url_for('discussion',appointment_id=appointment_id))
            else :
                flash("You have reached discussion limit","info")
        return render_template("discussion.html",discussion_list=discussion_list,appointment_details=appointment_details,
        limit=limit)
    except Exception as e:
        print(e)
    return render_template("discussion.html")

@app.route("/change_password/<string:encrypted_user_id>",methods=['GET','POST'])
def change_password(encrypted_user_id):
    headers={
        "Content-Type":"application/json"
        }
    if request.method == 'POST':
        new_password=request.form['new_password']
        payload={
                "user_id":encrypted_user_id,
                "password": new_password
            }
        api_data=json.dumps(payload)
        change_password_submit = requests.post(base_url+change_password_api, data=api_data, headers=headers)
        print("change password",change_password_submit.status_code)
        change_password_resp=json.loads(change_password_submit.text)
        print(change_password_resp)
        flash("Password changed","success")
        return redirect(url_for('login'))
    # change_password_api="administrator/change_password/<encrypted_user_id>"

    return render_template("change_password.html")

@app.route("/forgot_password",methods=['GET','POST'])
def forgot_password():
    headers={
        "Content-Type":"application/json"
        }
    if request.method == 'POST':
        email=request.form['email']
        payload={
            "email":email
        }
        api_data = json.dumps(payload)
        print(api_data)
        forgot_password_request=requests.post(base_url+forgot_password_api, data=api_data, headers=headers)
        forgot_password_response=json.loads(forgot_password_request.text)
        print("forgot password",forgot_password_request.status_code)
        print(forgot_password_response)
        return render_template("forgot_password_success.html")
    return render_template("forgot_password.html")

# @app.route("/pdfsample")
# def pdf_sample():
#     return render_template("pdf_sample.html")

@app.route("/prescription_pdf/<int:appointment_id>/<int:prescription_id>",methods=['GET','POST'])
def prescription_pdf(appointment_id,prescription_id):
    print(prescription_id)
    if 'user_id' in session:
        doctor_id=session['user_id']
        print("doc id",doctor_id)
    else:
        return redirect(url_for('login'))
    
    if 'doctor_flag' in session:
        doctor_flag=session['doctor_flag']
        print("doc flag",doctor_flag)

    headers={
            "Content-type":"application/json"
    }
    print(appointment_id)
    payload={
        "appointment_id":appointment_id,
        "user_id":"",
        "file_flag":"",
        "doctor_id":doctor_id
    }
    api_data=json.dumps(payload)
    print(api_data)
    appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
    appointment_detail_response=json.loads(appointment_detail.text)
    appointment_details=appointment_detail_response['data']
    print("detail api :",appointment_detail.status_code)
    user_id=appointment_details['user_id']
    print(user_id)
    category_id=appointment_details['category_id']
    follow_ups = appointment_details['followup']
    observations=appointment_details['observations']
    prescript_text=appointment_details["prescript_text"]
    for precription in prescript_text:
        if precription['id'] == prescription_id:
            precription ={
            "doctor_id":precription['doctor_id'],
            "uploaded_time":precription['uploaded_time'],
            "uploaded_date":precription['uploaded_date'],
            "prescriptions_text":precription['prescriptions_text'],
            "tests_to_be_done" : precription['tests_to_be_done'],
            "medicines" :precription['medicines'],
            "doctor_name" : precription['doctor_name'],
            }
    return render_template("prescription_pdf.html", appointment_details=appointment_details,prescript_text=prescript_text,prescription=precription)

@app.route("/add_working_hours", methods=['GET','POST'])
def add_working_hours():
    if 'user_id' in session:
        doctor_id=session['user_id']
        print(doctor_id)
    else:
        return redirect(url_for('login'))
    headers = {
                "Content-Type":"application/json"
            }
    payload={
            "doctor_id":doctor_id
        }
    api_data=json.dumps(payload)
    print(api_data)
    # work hour timeslot api call
    timeslot_list_request=requests.post(base_url+time_slot_list_api, data=api_data, headers=headers)
    timeslot_list_response=json.loads(timeslot_list_request.text)
    print("timeslot",timeslot_list_request.status_code)
    timeslots = timeslot_list_response['data']
    days = timeslot_list_response['weekday']

    #working hours list api call
    working_hours_list_request=requests.post(base_url+working_hours_list_api, data=api_data, headers=headers)
    working_hours_list_response=json.loads(working_hours_list_request.text)
    print("working hours",working_hours_list_request.status_code)
    working_hours=working_hours_list_response['data']

    # weeks
    # weeks=[
    #     {"week":"week1","day1":"Sunday","day2":"Monday"},{"week":"week2","day1":"Sunday","day2":"Monday"},{"week":"week3","day1":"Sunday","day2":"Monday","day2":"Tuesday"}
    #     ]
    # weeks=[
    #     {"week":"week1","days":[{"day":"Sunday","day":"Monday"}]},{"week":"week2","days":[{"day":"Sunday","day":"Monday"}]},{"week":"week3","days":[{"day":"Sunday","day":"Monday","day":"Tuesday"}]}
    #     ]
    week1=["Sunday","Monday","Tuesday"]
    week2=["Sunday","Monday","Tuesday"]
    week3=["Sunday","Monday","Tuesday"]
    week4=["Sunday","Monday","Tuesday"]
    days=[]
    # ,{"week2":{"day1":"Sunday","day2":"Monday"}},{"week3":{"day1":"Sunday","day2":"Monday"}}]
    if request.method == 'POST':
        print("post")
    # create 'working hours api' call
        days=request.form.getlist('day')
        print(days)
        sunday_slots = request.form.getlist('sundayslots')
        monday_slots = request.form.getlist('mondayslots')
        tuesday_slots = request.form.getlist('tuesdayslots')
        wednesday_slots = request.form.getlist('wednesdayslots')
        thursday_slots = request.form.getlist('thursdayslots')
        friday_slots = request.form.getlist('fridayslots')
        saturday_slots = request.form.getlist('saturdayslots')

        create_work_hour_payload={
                    "doctor_id": doctor_id,
                    "days":days,
                    "slots":[
                        {
                            "day":"Sunday",
                            "timeslots":sunday_slots,
                        },
                        {
                            "day":"Monday",
                            "timeslots":monday_slots,
                        },
                        {
                            "day":"Tuesday",
                            "timeslots":tuesday_slots,
                        },
                        {
                            "day":"Wednesday",
                            "timeslots":wednesday_slots,
                        },
                        {
                            "day":"Thursday",
                            "timeslots":thursday_slots,
                        },
                        {
                            "day":"Friday",
                            "timeslots":friday_slots,
                        },
                        {
                            "day":"Saturday",
                            "timeslots":saturday_slots,
                        }
                    ]

                }
        # converting payload to json format
        create_work_hr_json=json.dumps(create_work_hour_payload)                  
        print("work hours request",create_work_hr_json)
        # working hours api call
        working_hours_request=requests.post(base_url+working_hours_api, data=create_work_hr_json, headers=headers)
        working_hours_response=json.loads(working_hours_request.text)
        print("working hours",working_hours_request.status_code)
        print(working_hours_response)
        # create_working_hours=working_hours_response['data']
        return redirect(url_for("calendar"))
    
    return render_template("add_working_hours_copy.html", timeslots=timeslots, days=days, working_hours=working_hours,week1=week1,week2=week2,week3=week3,week4=week4)

@app.route("/add_rating/<int:appointment_id>", methods=['GET','POST'])
def add_rating(appointment_id):
    if 'user_id' in session:
        doctor_id=session['user_id']
        print(doctor_id)
    else:
        return redirect(url_for('login'))
    headers = {
                "Content-Type":"application/json"
            }
    payload={
        "appointment_id":appointment_id,
        "user_id":"",
        "file_flag":"",
        "doctor_id":doctor_id
    }
    api_data=json.dumps(payload)
    print(api_data)
    appointment_detail=requests.post(base_url+appointment_detail_api, data=api_data, headers=headers)
    appointment_detail_response=json.loads(appointment_detail.text)
    appointment_details=appointment_detail_response['data']
    print("detail api :",appointment_detail.status_code)
    user_id=appointment_details['user_id']
    print(user_id)
    # calling add ratings api
    if request.method == 'POST':
        app_rating=request.form['rate']
        customer_rating=request.form['customer_rate']
        rating_comments=request.form['comments']
        rating_payload={
            "appointment_id": appointment_id,
            "doctor_id":doctor_id,
            "user_id": user_id,
            "rating_comments": rating_comments,
            "rating": customer_rating,
            "app_rating": app_rating,
            "added_by": "doctor"
        }
        rating_data=json.dumps(rating_payload)
        print(rating_data)
        rating_submit=requests.post(base_url+add_rating_api,data=rating_data,headers=headers)
        submit_response=json.loads(rating_submit.text)
        print("add rating", rating_submit.status_code)
        print(submit_response)
        flash("Thank you for rating" , "success")
        return redirect(url_for('order_detail',id=appointment_id))

    return render_template("add_rating.html",appointment_details=appointment_details)

@app.route("/ratings")
def ratings():
    return render_template("ratings.html")

@app.route("/payment_success")
def payment_success():
    return render_template("payment_success.html")

@app.route("/payment_failed")
def payment_failed():
    return render_template("payment_failed.html")

if __name__ == '__main__':
    app.run(port=5001,debug = True)