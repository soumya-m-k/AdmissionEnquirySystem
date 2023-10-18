from flask import *
import mysql.connector as mysql
import pdfkit
import os
import pandas as pd
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
app.config['DEBUG'] = True

#uploader folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key='hello'
#home page first page
@app.route('/')
def homepage():
    return render_template('homepage.html')
#admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminwork')
def adminwork():
    return render_template('adminwork.html')

#admin register form
@app.route('/admin_register')
def admin_register():
    return render_template('admin_register.html')


#admin register insertion
@app.route('/enter7',methods=['POST'])
def enter7():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    passwd=request.form['pass']
    mnumber=request.form['mnumber']
    con=mysql.connect(host="localhost",user="root",password="",database="admission_enquiry")
    cur=con.cursor()
    cur.execute('insert into admin_register values(%s,%s,%s,%s,%s)',(fname,lname,email,passwd,mnumber))
    con.commit()
    con.close()
    flash('data saved')
    return render_template('admin_register.html')

@app.route('/checkuser1',methods=['POST'])
def checkuser1():
    fname=request.form['fname']
    passwd= request.form['pass']
    con=mysql.connect(host='localhost',user='root',password='',database='admission_enquiry')
    cur=con.cursor()
    cur.execute('select * from admin_register where fname=%s and pass=%s',(fname,passwd))
    result=cur.fetchall()
    if(len(result)==0):
        flash('invalid username or password')
        return render_template('admin.html')
    else:
        session['username']=fname
        return render_template('adminwork.html')
    
 #to logout admin   
@app.route('/logout1')
def logout1():
    session.pop('username')
    return redirect('/admin')

#admin upload student csv html file
@app.route('/iddetail')
def iddetail():
    return render_template('stud_detail.html')

#logic to insert csv file
con=mysql.connect(host='localhost',user='root',password='',database='admission_enquiry')
cur=con.cursor()
@app.route('/studfile', methods = ['POST'])
def uploadfiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],uploaded_file.filename)
        uploaded_file.save(file_path)
        parsecsv(file_path)
        return redirect(url_for('iddetail'))
    
def parsecsv(filePath):
    col_names = ['regno','Student_Name','course']
    csvdata = pd.read_csv(filePath,names=col_names,header=None)
    for i,row in csvdata.iterrows():
        sql='INSERT INTO stud_idcard(regno,Student_Name,course) VALUES (%s,%s,%s)'
        value = (row['regno'],row['Student_Name'],row['course'])
        cur.execute(sql,value)
        con.commit()

#enquiry details form filling by admin
@app.route('/enquirydetail')
def enquirydetail():
    return render_template("admin_enquiry_form.html")

#admin insert enquiry details into database
@app.route('/fillform',methods=['POST'])
def fillform():
    course=request.form['course']
    gm_boys=request.form['gm_boys']
    gm_girls=request.form['gm_girls']
    scst_boys=request.form['scst_boys']
    scst_girls=request.form['scst_girls']
    contacts=request.form['contacts']
    contact_number=request.form['contact_number']
    con=mysql.connect(host="localhost",user="root",password="",database="admission_enquiry")
    cur=con.cursor()
    cur.execute('insert into enquiry_details values(%s,%s,%s,%s,%s,%s,%s)',(course,gm_boys,gm_girls,scst_boys,scst_girls,contacts,contact_number))
    con.commit()
    con.close()
    flash('data saved')
    return render_template('admin_enquiry_form.html')


    

# aboutus page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
#register page html
@app.route('/register')
def register():
    return render_template('register.html')
#login html page
@app.route('/login')
def login():
    return render_template('login.html')
#register insertion
@app.route('/enter',methods=['POST'])
def enter():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    passwd=request.form['pass']
    mnumber=request.form['mnumber']
    con=mysql.connect(host="localhost",user="root",password="",database="admission_enquiry")
    cur=con.cursor()
    cur.execute('insert into register values(%s,%s,%s,%s,%s)',(fname,lname,email,passwd,mnumber))
    con.commit()
    con.close()
    flash('data saved')
    return render_template('register.html')
#login selection
@app.route('/checkuser',methods=['POST'])
def checkuser():
    fname=request.form['fname']
    passwd= request.form['pass']
    con=mysql.connect(host='localhost',user='root',password='',database='admission_enquiry')
    cur=con.cursor()
    cur.execute('select * from register where fname=%s and pass=%s',(fname,passwd))
    result=cur.fetchall()
    if(len(result)==0):
        flash('invalid username or password')
        return render_template('login.html')
    else:
        session['username']=fname
        return render_template('navigation.html')
#navigation
@app.route('/navi')
def navi():
    return render_template('navigation.html')
#documents
@app.route('/doc')
def docs():
    return render_template('doc.html')
#logout
@app.route('/logout')
def logout():
    session.pop('username',None)
   # Response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return redirect('/login')
#fees structure
@app.route("/fees")
def fees():
    return render_template('fees.html')
@app.route("/ba")
def ba():
    return render_template('ba.html')
@app.route("/bcom")
def bcom():
    return render_template('bcom.html')
@app.route("/bsc")
def bsc():
    return render_template('bsc.html')
@app.route("/bba")
def bba():
    return render_template('bba.html')
@app.route("/bca")
def bca():
    return render_template('bca.html')

#course html page
@app.route("/course")
def course():
    return render_template('course.html')


#id card user information
@app.route("/idcard")
def idcard():
    return render_template('idcard.html')
#id card display
@app.route("/display")
def display():
    return render_template('display.html')
    

#id card creation logic
@app.route('/getid',methods=['POST'])
def getid():
    regno=request.form['regno']
    course= request.form['course']
    con=mysql.connect(host='localhost',user='root',password='',database='admission_enquiry')
    cur=con.cursor()
    cur.execute('select regno,Student_Name,course from stud_idcard where regno=%s and course=%s',(regno,course))
    result=cur.fetchall()
    if(len(result)==0):
        flash("Student information not found")
        return render_template("idcard.html")
    else:
    #if(course=='B.A'):
       # cur.execute('select regno,Student_Name,course from ba_idcard where regno=%s',(regno,))
       # result=cur.fetchall()
        html = render_template("display.html",result=result)
        pdf = pdfkit.from_string(html, options={"enable-local-file-access": ""})
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response
  
    


        
#user information
@app.route('/eform')
def eform():
    return render_template('eform.html')
#gettting stored information of user for enquiry
@app.route('/getinfo',methods=['POST'])
def getinfo():
    fname=request.form['fname']
    mname=request.form['mname']
    sname=request.form['sname']
    course=request.form['course']
    email=request.form['email']
    mnumber=request.form['mnumber']
    con=mysql.connect(host="localhost",user="root",password="",database="admission_enquiry")
    cur=con.cursor()
    cur.execute('insert into eform values(%s,%s,%s,%s,%s,%s)',(fname,mname,sname,course,email,mnumber))
    flash('data saved')
    return render_template('details.html')
#getting enquiry details using email
@app.route('/detail')
def detail():
    return render_template('details.html')

#enquiry details sending to email logic
@app.route('/enquirysend',methods=['POST'])
def enquirysend():
    gender=request.form['gender']
    course= request.form['course']
    cast=request.form['cast']
    enqueries=request.form['enqueries']
    con=mysql.connect(host='localhost',user='root',password='',database='admission_enquiry')
    cur=con.cursor()

    # for ba course changing the gender as male for gm category
    if course=='B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
        
    elif course=='B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for ba course changing the gender as male for sc/st category
    elif course=='B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)

    
    # for ba course changing the gender as female for gm category
    elif course=='B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
     # for ba course changing the gender as female for sc/st category
    elif course=='B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        #pdf = pdfkit.from_string(html, options={"enable-local-file-access": ""})
        #response = make_response(pdf)
        #response.headers["Content-Type"] = "application/pdf"
        #response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        #return response
    

    # for bcom course enquiry
    # for b.com course changing the gender as male for gm category
    elif course=='B.Com' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Com' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Com' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for b.com course changing the gender as male for sc/st category
    elif course=='B.Com' and gender=='Male' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Com' and gender=='Male' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Com' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.Com course changing the gender as female for gm category
    elif course=='B.Com' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Com' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Com' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
     # for B.Com course changing the gender as female for sc/st category
    elif course=='B.Com' and gender=='Female' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Com' and gender=='Female' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Com' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    

    # for B.Sc course enquiry
    # for B.Sc course changing the gender as male for gm category
    elif course=='B.Sc' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Sc' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Sc' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.Sc course changing the gender as male for sc/st category
    elif course=='B.Sc' and gender=='Male' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Sc' and gender=='Male' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Sc' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.Sc course changing the gender as female for gm category
    elif course=='B.Sc' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Sc' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Sc' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
     # for B.Sc course changing the gender as female for sc/st category
    elif course=='B.Sc' and gender=='Female' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.Sc' and gender=='Female' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.Sc' and gender=='Female' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    

    # for B.B.A course enquiry
    # for B.B.A course changing the gender as male for gm category
    elif course=='B.B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.B.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.B.A course changing the gender as male for sc/st category
    elif course=='B.B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.B.A' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.B.A course changing the gender as female for gm category
    elif course=='B.B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.B.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
# for B.B.A course changing the gender as female for sc/st category
    elif course=='B.B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.B.A' and gender=='Female' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    

    # for B.C.A course enquiry
    # for B.C.A course changing the gender as male for gm category
    elif course=='B.C.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.C.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.C.A' and gender=='Male' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.C.A course changing the gender as male for sc/st category
    elif course=='B.C.A' and gender=='Male' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.C.A' and gender=='Male' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_boys from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.C.A' and gender=='Male' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    # for B.C.A course changing the gender as female for gm category
    elif course=='B.C.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.C.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='FEES' :
        cur.execute('select course ,gm_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.C.A' and gender=='Female' and cast=='GM/OBC/CAT 1' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
# for B.C.A course changing the gender as female for sc/st category
    elif course=='B.C.A' and gender=='Female' and cast=='SC/ST' and enqueries=='DOCUMENTS' :
        return render_template('doc.html')
    elif course=='B.C.A' and gender=='Female' and cast=='SC/ST' and enqueries=='FEES' :
        cur.execute('select course ,scst_girls from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("help.html",gender=gender,cast=cast,result=result)
        
    elif course=='B.C.A' and gender=='Female' and cast=='SC/ST' and enqueries=='CONTACTS' :
        cur.execute('select course ,contacts,contact_number from enquiry_details where course=%s',(course,))
        result=cur.fetchall()
        return render_template("contact.html",gender=gender,cast=cast,result=result)
        
    
    else:
        return redirect('/detail')
    
@app.route('/help')
def help():
    return render_template('help.html') 
@app.route('/contact')
def contact():
    return render_template('contact.html')
#adding new eform page
@app.route('/add')
def add():
    return render_template('eform.html')

@app.route("/facility")
def facility():
    return render_template("facilities.html")
@app.route("/hostel")
def hostel():
    return render_template("hostel.html")
@app.route("/library")
def library():
    return render_template("library.html")
@app.route("/labs")
def labs():
    return render_template("labs.html")
@app.route("/sports")
def sports():
    return render_template("sports.html")

