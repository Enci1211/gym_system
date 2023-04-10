import mysql.connector
from mysql.connector import FieldType
import datetime
import time
from datetime import date,timedelta
from decimal import Decimal
import connect_gym
from flask import Flask,render_template,request,redirect,url_for
from flask import session

from email.message import EmailMessage
import ssl
import smtplib

from flask import stream_with_context



app = Flask(__name__)
app.secret_key = '14'

# get current date and calculate the date 7 days from now
current_date = date.today()
current_date = current_date.replace(year=2023, month=3, day=20)

future_date = current_date + timedelta(days=7)
week_ago = current_date - timedelta(days=7)
current_time = time.strftime("%H:%M:%S")

# format dates for the query
current_date_str = current_date.strftime('%Y-%m-%d')
future_date_str =future_date.strftime('%Y-%m-%d')

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect_gym.dbuser, \
    password=connect_gym.dbpass, host=connect_gym.dbhost, \
    database=connect_gym.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn
def columnOutput(dbData,cols,formatStr):
    print(formatStr.format(*cols))
    for row in dbData:
        rowList=list(row)
        for index,item in enumerate(rowList):
            if item==None:      
                rowList[index]=""       
            elif type(item)==datetime.date or type(item)==datetime.datetime or type(item)==datetime.time or type(item)==datetime.timedelta:    
                rowList[index]=str(item)
        print(formatStr.format(*rowList)) 

# gym system for universal--------------------------------------------------------------


# home page for login (user can input userid or password to login since manager doen't have a email address so manager can only login by userid , member/train can use both userid and email )
@app.route("/", methods = ['POST','GET'])
def home():    
    if request.method == 'POST':
        userid_or_email = request.form['userid_or_email'] 
        password_input = request.form['password']

        cur = getCursor()  # fetch userid list of all memebers
        cur.execute("""SELECT userid FROM user where role = 'member';""") 
        dbOutput = cur.fetchall()
        memberList = [item for m in dbOutput for item in m]
        print(memberList)

        cur5 = getCursor()  # fetch email list of all memebers
        cur5.execute("""SELECT email FROM member;""") 
        dbOutput5 = cur5.fetchall()
        memberList_email = [item for m in dbOutput5 for item in m]
        print(memberList_email)

        cur2 = getCursor() # fetch userid list of all trainers
        cur2.execute("""SELECT userid FROM user where role = 'trainer';""")
        dbOutput2 = cur2.fetchall()
        trainerList = [item for a in dbOutput2 for item in a]
        print(trainerList)

        cur6 = getCursor()  # fetch email list of all trainers
        cur6.execute("""SELECT email FROM trainer;""") 
        dbOutput6 = cur6.fetchall()
        trainerList_email = [item for m in dbOutput6 for item in m]
        print(trainerList_email)

        cur3 = getCursor()  # fetch userid list of all managers
        cur3.execute("""SELECT userid FROM user where role = 'admin';""")
        dbOutput3 = cur3.fetchall()
        adminList = [item for a in dbOutput3 for item in a]
        print(adminList)

        cur4 = getCursor()  # fetch all the userid we have
        cur4.execute("""select userid from user;""")
        dbOutput4 = cur4.fetchall()
        userList = [item for u in dbOutput4 for item in u]

        try:           
           if int(userid_or_email) in userList:
              cur = getCursor()
              sql = """select password from user where userid = %s """
              parameter = (userid_or_email,)
              cur.execute(sql,parameter)
              dbOutput = cur.fetchall()
              userPassword = dbOutput[0][0]
              print(userPassword)
              if password_input == userPassword:
                  if int(userid_or_email) in memberList:  
                    return redirect(url_for('member',userid = userid_or_email))                                   
                  elif int(userid_or_email) in trainerList:
                    return redirect(url_for('trainer',userid = userid_or_email)) 
                  elif int(userid_or_email) in adminList:
                    return redirect(url_for('admin',userid = userid_or_email)) 
              else:
                return render_template("main/home.html", incorrect_password = "incorrect password, please try again!")
           return render_template("main/home.html", not_user = "please register first, thank you!") 
        except:

            if userid_or_email in memberList_email:
               cur = getCursor()
               sql = """SELECT password from user 
                    join member
                    on user.userid = member.userid where member.email = %s ; """
               parameter = (userid_or_email,)
               cur.execute(sql,parameter)
               dbOutput = cur.fetchall()
               userPassword = dbOutput[0][0]
               if password_input == userPassword:
                  cur = getCursor()
                  sql = ("""select userid from member where email = %s;""")
                  parameter =(userid_or_email,)
                  cur.execute(sql,parameter)
                  dbOutput = cur.fetchall()
                  userEmail = dbOutput[0]
                  return redirect(url_for('member',userid = userEmail))
               else:
                  return render_template("main/home.html", incorrect_password = "incorrect password, please try again!") 
            elif userid_or_email in trainerList_email:
               cur = getCursor()
               sql = """SELECT password from user 
                    join trainer
                    on user.userid = trainer.userid where trainer.email = %s ; """
               parameter = (userid_or_email,)
               cur.execute(sql,parameter)
               dbOutput = cur.fetchall()
               userPassword = dbOutput[0][0]
               if password_input == userPassword:
                  cur = getCursor()
                  sql = ("""select userid from trainer where email = %s;""")
                  parameter =(userid_or_email,)
                  cur.execute(sql,parameter)
                  dbOutput = cur.fetchall()
                  userEmail = dbOutput[0]
                  return redirect(url_for('trainer',userid = userEmail)) 
               else:
                  return render_template("main/home.html", incorrect_password = "incorrect password, please try again!")  
            else:
              return render_template("main/home.html", not_user = "please register first, thank you!")         
    else:
        return render_template("main/home.html")

# member's home page after login
@app.route("/member/",methods = ['POST','GET'])
def member():
    userid = request.args.get("userid")  
    cur=getCursor()
    sql=("""select first_name, last_name from member where userid=%s""")
    parameter=(userid,)
    cur.execute(sql,parameter)
    dbOutput=cur.fetchall() 
    first_name=dbOutput[0][0]
    last_name=dbOutput[0][1] 
    return render_template("member/member.html",userid = userid,first_name=first_name,last_name=last_name)

# trainer's home page after login
@app.route("/trainer/",methods = ['POST','GET'])
def trainer():
    userid = request.args.get("userid")    
    return render_template("trainer/trainer.html",userid = userid)

# admin's home page after login
@app.route("/admin/",methods = ['POST','GET'])
def admin():
    userid = request.args.get("userid")    
    return render_template("admin/admin.html",admin_userid = userid)



# gym system for trainer------------------------------------------------------------------
# a1 trainer-view own profile
@app.route("/trainer/profile/",methods = ['POST','GET'])
def trainerprofile():
    userid = request.args.get("userid")
    updated = request.args.get("updated")
    
    cur = getCursor()
    dbsql = ("""SELECT * FROM trainer
                    where userid = %s;""")    #fetch the specific trainer's info
    parameter = (userid,)
    cur.execute(dbsql,parameter)
    dbOutput = cur.fetchall()
    return render_template("trainer/trainerProfile.html", staff = dbOutput, updated = updated,userid=userid)

# a2 trainer-update profile
@app.route("/trainer/profile/update/",methods = ['POST','GET'])
def trainerprofile_update():
    

    if request.method == 'POST':

        trainer_profile_now = request.form
        print(trainer_profile_now)

        email_new = trainer_profile_now['email']
        
        phone_new = trainer_profile_now['phone']
        address_new = trainer_profile_now['address']
        specialties_new = trainer_profile_now['specialties']
        userid = trainer_profile_now['userid']     # fetch the userid from form to this varieble

        cur = getCursor()   #update the new details into the db 
        dbsql = """update trainer
                   set email=%s,phone=%s,address=%s,specialties=%s
                   where userid = %s;"""
        parameters = (email_new,phone_new,address_new,specialties_new,userid)
        cur.execute(dbsql,parameters) 
        connection.commit()

        return redirect(url_for('trainerprofile', userid = userid, updated = 'yes'))
    else:
        userid = request.args.get("userid") #fetch userid from url

        cur=getCursor()
        sql=("""select * from trainer where userid = %s""")
        parameter=(userid,)
        cur.execute(sql,parameter)
        dbOutput=cur.fetchall()
        print(dbOutput)
    
        first_name = dbOutput[0][2]
        last_name = dbOutput[0][3]
        email = dbOutput[0][4]
        phone = dbOutput[0][5]
        address = dbOutput[0][6]
        dateBirth = dbOutput[0][7]
        specialties = dbOutput[0][8]
    return render_template("trainer/trainerprofile_update.html",userid =userid,first_name=first_name,last_name=last_name,email=email,phone=phone,address=address,dateBirth=dateBirth,specialties=specialties) # pass userid to form in front-end


#trainer view trainee profile
@app.route("/trainer/trainee/")
def traineeprofile():
    userid = request.args.get("userid")
    cur = getCursor()
    dbsql = ("""SELECT ts.sessions_id, concat(m.first_name,' ',m.last_name ) as Trainee, m.email, m.phone, b.date, time
            FROM trainer_sessions as ts
	        LEFT JOIN booking as b
                on ts.sessions_id = b.session_id
		        JOIN member as m
                    on b.member_id = m.userid
            Where ts.session_status = "booked"
            Order by b.date, ts.time; """)    #fetch all the members' info
    cur.execute(dbsql)
    dbOutput = cur.fetchall()
    return render_template("trainer/trainee.html", member = dbOutput , userid = userid)


        

# gym system for member-----------------------------------------------------------------
# b1-1 member-view trainer
@app.route("/member/viewtrainer/")
def trainername():
    userid = request.args.get("userid")
    cur = getCursor()
    dbsql = "SELECT * FROM trainer;"    
    cur.execute(dbsql)
    dbOutput = cur.fetchall()
    return render_template("/member/viewtrainer.html", trainername = dbOutput,userid = userid)

# b1-2 member ---view training session 
@app.route("/member/viewtrainer/session/")
def trainer_session():
    userid = request.args.get("userid")
    trainerUserid = request.args.get("traineruserid")    

    cur = getCursor()   # fetch all the sessions under this trainer in the future
    dbsql = ("""SELECT sessions_id, date, time, fee, session_status
                from trainer_sessions
                where session_status = 'available' and staff_id = %s and date between %s and %s ;""")     
    parameter = (trainerUserid,current_date_str,future_date_str)
    
    cur.execute(dbsql,parameter)
    dbOutput = cur.fetchall()

    if not dbOutput:    
       return render_template('member/trainer_session.html')
    else:
       return render_template('member/trainer_session.html',session = dbOutput,userid = userid, trainerUserid = trainerUserid)
# b1-3 member---book trainer session
@app.route("/member/viewtrainer/session/book/",methods = ['POST','GET'])
def book_trainer_session():
    userid = request.args.get("userid")

    cur6=getCursor()  # check if this member is active
    sql6=("""select subscription_status from member where userid = %s""")
    parameters6= (userid,)
    cur6.execute(sql6,parameters6)
    dbOutput6=cur6.fetchall()

    if dbOutput6[0][0]:
        traineruserid = request.args.get("traineruserid")
        sessionid = request.args.get("sessionid")
        print(userid,traineruserid,sessionid)
        
        cur = getCursor()
        dbsql = ("""select first_name, last_name from trainer where userid = %s""")
        parameter = (traineruserid,)
        cur.execute(dbsql,parameter)
        dbOutput = cur.fetchall()
        print(dbOutput)

        staff_full_name = dbOutput[0][0] + dbOutput[0][1] 
        print(staff_full_name)

        cur2 = getCursor()
        dbsql2 = ("""select date, time, fee from trainer_sessions where sessions_id = %s""")
        parameter2 = (sessionid,)
        cur2.execute(dbsql2,parameter2)
        dbOutput2 = cur2.fetchall()  
        print(dbOutput2)
        session_date = dbOutput2[0][0]
        session_time = dbOutput2[0][1]
        session_fee = dbOutput2[0][2]
        
        return render_template('member/book_trainer_session.html',dbOutput6=dbOutput6,userid = userid,staff_full_name = staff_full_name,session_date = session_date,session_time=session_time,session_fee =session_fee,sessionid=sessionid,traineruserid =traineruserid)
    else:
        inactive='sorry , you need to pay off your outstanding balance first.'
        return render_template("member/book_trainer_session.html",inactive=inactive,dbOutput6=dbOutput6,userid=userid)
# b1-4 member --- pay for trainer session
@app.route("/member/viewtrainer/session/book/booked/")
def book_trainer_session_booked():
    userid = request.args.get("userid")
    traineruserid = request.args.get("traineruserid")
    sessionid = request.args.get("sessionid")

    cur = getCursor()  # fetch trainer's name
    dbsql = ("""select first_name, last_name from trainer where userid = %s""")
    parameter = (traineruserid,)
    cur.execute(dbsql,parameter)
    dbOutput = cur.fetchall()
    print(dbOutput)

    staff_full_name = dbOutput[0][0] + dbOutput[0][1]

    cur2 = getCursor()  # fetch session details
    dbsql2 = ("""select date, time, fee from trainer_sessions where sessions_id = %s""")
    parameter2 = (sessionid,)
    cur2.execute(dbsql2,parameter2)
    dbOutput2 = cur2.fetchall()  
    print(dbOutput2)
    session_date = dbOutput2[0][0]
    session_time = dbOutput2[0][1]
    session_fee = dbOutput2[0][2]

    cur3 = getCursor()      # update trainer_session table,status column
    dbsql3 = ("""update trainer_sessions set session_status = 'booked' where sessions_id = %s and date = %s""") # change the session status to booked after someone booked it
    parameter3 = (sessionid,session_date)
    cur3.execute(dbsql3,parameter3)
    connection.commit()

    cur4 = getCursor()   # update booking table ,add a new data
    dbsql4 = ("""insert into booking (session_id, date, booking_status, member_id)
                 values (%s,%s,'booked',%s)""")
    parameter4 = (sessionid,session_date,userid)
    cur4.execute(dbsql4,parameter4)
    connection.commit()

    cur5 = getCursor()  #update payment table, add a new data
    dbsql5 = ("""insert into payment (member_id,amount,date,time,type,status)
                  value (%s,%s,%s,%s,'personal training session','pending')""")
    parameters5 = (userid,(Decimal(session_fee)/Decimal(1.0)),current_date_str,current_time)
    cur5.execute(dbsql5,parameters5)
    connection.commit()

    
    return render_template('member/book_trainer_session_booked.html',userid = userid,staff_full_name = staff_full_name,session_date = session_date,session_time=session_time,session_fee =session_fee,sessionid=sessionid,traineruserid =traineruserid)


   
# b2 member- view own profile
@app.route("/member/profile/", methods = ['GET'])
def memberviewprofile():
    userid = request.args.get("userid")    
    updated = request.args.get("updated")

    cur = getCursor()
    dbsql = ("""SELECT * FROM member
                        where userid = %s;""")    
    parameter = (userid,)
    cur.execute(dbsql,parameter)
    dbOutput = cur.fetchall()
    return render_template("member/memberviewprofile.html", member = dbOutput,userid=userid ,updated=updated)
    

    




# # b3 member-change own profile
@app.route("/member/profile/edit/", methods = ['GET','POST'])
def memberupdatemember():
    
    if request.method == 'POST':

        member_profile_now = request.form
        print(member_profile_now)
        email_new = member_profile_now['email']        
        phone_new = member_profile_now['phone']
        address_new = member_profile_now['address']
        userid = member_profile_now['userid']     # fetch the userid from form to this varieble
        print(userid)
        cur = getCursor()   #update the new details into the db 
        dbsql = """update member
                   set email=%s,phone=%s,address=%s 
                   where userid = %s;"""
        parameters = (email_new,phone_new,address_new,userid)
        cur.execute(dbsql,parameters) 
        connection.commit()

        return redirect(url_for('memberviewprofile', userid = userid, updated = 'yes'))
    else:
        userid = request.args.get("userid") #fetch userid from url

        cur=getCursor()
        sql=("""select * from member where userid = %s""")
        parameter=(userid,)
        cur.execute(sql,parameter)
        dbOutput=cur.fetchall()
        print(dbOutput)
    
        first_name = dbOutput[0][2]
        last_name = dbOutput[0][3]
        email = dbOutput[0][4]
        phone = dbOutput[0][5]
        address = dbOutput[0][6]
        date_of_birth = dbOutput[0][7]
    
    return render_template("member/edit.html",email=email,phone=phone,address=address,userid=userid,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth)
   




# b4-1 member-view group class timetable
@app.route("/member/groupclass/", methods = ['POST','GET'])
def groupclass():
    userid = request.args.get("userid")
    tomorrow = current_date + timedelta(days=1)
    after_2_days = current_date + timedelta(days=2)
    after_3_days =current_date + timedelta(days=3)
    after_4_days=current_date + timedelta(days=4)
    after_5_days=current_date + timedelta(days=5)
    after_6_days=current_date + timedelta(days=6)

    today_week = current_date.strftime("%A")
    tomorrow_week = tomorrow.strftime("%A")
    after_2_days_week =after_2_days.strftime("%A")
    after_3_days_week = after_3_days.strftime("%A")
    after_4_days_week =after_4_days.strftime("%A")
    after_5_days_week =after_5_days.strftime("%A")
    after_6_days_week =after_6_days.strftime("%A")

    
    

    cur1 = getCursor()  # fetch 09:00:00 classes in 7 days
    sql1=("""SELECT g.class_name, concat(book_space,'/',max_space),g.class_id,t.first_name,g.book_space
            from group_class as g
            join trainer as t
            on g.userid = t.userid
            where g.time = '09:00:00' and g.date >=%s  and g.date <%s ;""")
    parameter1 = (current_date,future_date)
    cur1.execute(sql1,parameter1)
    class_9am = cur1.fetchall()
    print(class_9am)

    cur2 = getCursor()  # fetch 10:00:00 classes in 7 days
    sql2=("""SELECT g.class_name, concat(book_space,'/',max_space),g.class_id,t.first_name,g.book_space
            from group_class as g
            join trainer as t
            on g.userid = t.userid
            where g.time = '10:00:00' and g.date >=%s  and g.date < %s;""")
    parameter2 = (current_date,future_date)
    cur2.execute(sql2,parameter2)
    class_10am = cur2.fetchall()

    cur3 = getCursor()  # fetch 11:00:00 classes in 7 days
    sql3=("""SELECT g.class_name, concat(book_space,'/',max_space),g.class_id,t.first_name,g.book_space
            from group_class as g
            join trainer as t
            on g.userid = t.userid
            where g.time = '11:00:00' and g.date >=%s  and g.date < %s;""")
    parameter3 = (current_date,future_date)
    cur3.execute(sql3,parameter3)
    class_11am = cur3.fetchall()

    cur4 = getCursor()  # fetch 11:00:00 classes in 7 days
    sql4=("""SELECT g.class_name, concat(book_space,'/',max_space),g.class_id,t.first_name,g.book_space
            from group_class as g
            join trainer as t
            on g.userid = t.userid
            where g.time = '12:00:00' and g.date >=%s  and g.date < %s;""")
    parameter4 = (current_date,future_date)
    cur4.execute(sql4,parameter4)
    class_12pm = cur4.fetchall()

    cur5 = getCursor()  # fetch 13:00:00 classes in 7 days
    sql5=("""SELECT g.class_name, concat(book_space,'/',max_space),g.class_id,t.first_name,g.book_space
            from group_class as g
            join trainer as t
            on g.userid = t.userid
            where g.time = '13:00:00' and g.date >=%s  and g.date < %s;""")
    parameter5 = (current_date,future_date)
    cur5.execute(sql5,parameter5)
    class_13pm = cur5.fetchall()

    return render_template("member/view_group_class.html",userid = userid,class_9am=class_9am,class_10am=class_10am,
    class_11am=class_11am,class_12pm=class_12pm,class_13pm=class_13pm,today=current_date,tomorrow=tomorrow,after_2_days=after_2_days,after_3_days=after_3_days,
    after_4_days=after_4_days,after_5_days=after_5_days,after_6_days=after_6_days,today_week=today_week,tomorrow_week=tomorrow_week, after_2_days_week= after_2_days_week,
    after_3_days_week= after_3_days_week,after_4_days_week=after_4_days_week,after_5_days_week=after_5_days_week,after_6_days_week=after_6_days_week )
    
# b4-2 member--book a group class
@app.route("/member/groupclass/book/")
def groupclass_book():
    userid = request.args.get("userid")  
    classid = request.args.get("classid")

    cur7=getCursor()  # check if this class has bee fully booked
    sql7=("""select book_space from group_class where class_id = %s""")
    parameters7= (classid,)
    cur7.execute(sql7,parameters7)
    dbOutput7=cur7.fetchall()
    print(dbOutput7)

    if dbOutput7[0][0] == 30:
       full = 1
       return render_template("member/groupclass_book.html",full=full,userid=userid)
    else:
        cur6=getCursor()  # check if this member is active
        sql6=("""select subscription_status from member where userid = %s""")
        parameters6= (userid,)
        cur6.execute(sql6,parameters6)
        dbOutput6=cur6.fetchall()

        if dbOutput6[0][0]:

            cur5=getCursor()  # check if this member have already booked this class
            sql5=("""select booking_id from booking where class_id = %s and member_id = %s;""")
            parameters5= (classid,userid)
            cur5.execute(sql5,parameters5)
            dbOutput5=cur5.fetchall()
            print(dbOutput5)
            if dbOutput5 :
                return render_template("member/groupclass_book.html",dbOutput5=dbOutput5,dbOutput6=dbOutput6,userid=userid)
            else:

                cur= getCursor() # fetch the related datails of the class member booked, and show member
                sql=("""select g.class_name, g.date, g.time, t.first_name, t.last_name 
                    from group_class as g
                    join trainer as t
                    on g.userid = t.userid where g.class_id = %s;""")
                parameter = (classid,)
                cur.execute(sql,parameter)
                dbOutput = cur.fetchall()
                print(dbOutput)
                class_name = dbOutput[0][0]
                class_date = dbOutput[0][1]
                class_time = dbOutput[0][2]
                first_name = dbOutput[0][3]
                last_name =dbOutput[0][4]

                cur2=getCursor() # update the booking table with this new booking data
                sql2=("""INSERT INTO booking (class_id, date, booking_status,member_id) VALUES (%s, %s,'booked', %s);""")
                parameters2=(classid,current_date,userid)
                cur2.execute(sql2,parameters2)
                connection.commit()
            
                cur3 = getCursor() # fetch the booked space currently of this class member booked
                sql3 = ("""select book_space from group_class where class_id = %s;""")
                parameter3 = (classid,)
                cur3.execute(sql3,parameter3)
                dbOutput3= cur3.fetchall()
                current_booked_space = dbOutput3[0][0]

                cur4=getCursor()  # update the group class , booked space  +1
                sql4=("""update group_class set book_space = %s where class_id = %s;""")
                parameter4=((int(current_booked_space)+1),classid)
                cur4.execute(sql4,parameter4)
                connection.commit()

                return render_template("member/groupclass_book.html",dbOutput6=dbOutput6,class_name=class_name,date=class_date,time=class_time,first_name=first_name,last_name=last_name,userid=userid)
        else:
            inactive='sorry , you need to pay off your outstanding balance first.'
            return render_template("member/groupclass_book.html",inactive=inactive,dbOutput6=dbOutput6,userid=userid)

# b5 As a member, I would like to pay subsvription fee. So I don't owe anything.

@app.route("/member/paysubscription/")
def paysubscription():
    
        userid = request.args.get("userid")
        dbsql = ("SELECT userid, subscription_start_date,subscription_end_date,balance FROM member where userid = %s;")
        parameter = (userid,)
        cur = getCursor()
        cur.execute(dbsql,parameter)
        dbOutput = cur.fetchall()
        if dbOutput[0][3] >=0:
            own=0
        else:
            own=-dbOutput[0][3]
        
        return render_template("member/paymembership.html", subscription = dbOutput,own=own,userid=userid)

@app.route("/member/paynow/")
def paynow():

        userid = request.args.get("userid")
        amount = request.args.get("amount")

        return render_template("member/paypage.html",userid=userid,amount=amount)
@app.route("/member/paysubscription/success/")
def paysubscription_success():
    userid = request.args.get("userid")
    amount = request.args.get("amount")
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    payment_type = 'subscription'
    status = 'paid'

    dbsql = ("UPDATE member SET balance = 0 WHERE userid = %s;") # set balance to 0
    parameter = (userid,)
    cur = getCursor()
    cur.execute(dbsql,parameter)
        
    cur3 =getCursor()  # insert a new data to payment table
    data = (userid, amount, current_date, current_time, payment_type, status)
    dbsql3 = ("INSERT INTO payment (member_id, amount, date, time, type, status) VALUES (%s, %s, %s, %s, %s, %s)")
    cur3.execute(dbsql3,data)
    return render_template("member/paysubscription_success.html",userid=userid)

#  member view bookings

@app.route("/member/booking/")
def booking():
    userid = request.args.get("userid")
    cur = getCursor()  # fetch all group class this member have booked in the future
    sql=("""select g.class_id, g.class_name, g.date, g.time from group_class as g
                   join booking as b on g.class_id = b.class_id
                   where b.booking_status = 'booked' and b.member_id = %s""")
    parameter =(userid,)
    cur.execute(sql,parameter)
    dbOutput = cur.fetchall()


    cur2=getCursor() # fetch all the pt session this member have booked in the future
    sql2=("""SELECT s.sessions_id , concat(t.first_name, ' ' , t.last_name),s.date, s.time 
            from trainer_sessions as s join trainer as t
            on s.staff_id = t.userid
            join booking as b
            on s.sessions_id = b.session_id
            where b.booking_status = 'booked' and  b.member_id = %s ;""")
    cur2.execute(sql2,parameter)
    dbOutput2 = cur2.fetchall()

    return render_template("member/booking.html",userid=userid,group_class=dbOutput,trainer_session=dbOutput2)


# memeber cancel booking
@app.route("/member/cancel/")
def cancel():
    userid = request.args.get("userid")
    classid =request.args.get("classid")
    sessionid = request.args.get("sessionid")

    if classid:
        cur2=getCursor() # update the booking table with deleting the bookig data
        sql2=("""delete from booking where class_id = %s and member_id = %s;""")
        parameters2=(classid,userid)
        cur2.execute(sql2,parameters2)
        connection.commit()
        
        cur3 = getCursor() # fetch the booked space currently of this class member booked
        sql3 = ("""select book_space from group_class where class_id = %s;""")
        parameter3 = (classid,)
        cur3.execute(sql3,parameter3)
        dbOutput3= cur3.fetchall()
        current_booked_space = dbOutput3[0][0]

        cur4=getCursor()  # update the group class , booked space  -1
        sql4=("""update group_class set book_space = %s where class_id = %s;""")
        parameter4=((int(current_booked_space)-1),classid)
        cur4.execute(sql4,parameter4)
        connection.commit()
    else:
        cur2 = getCursor()  # fetch session details
        dbsql2 = ("""select date, time, fee from trainer_sessions where sessions_id = %s""")
        parameter2 = (sessionid,)
        cur2.execute(dbsql2,parameter2)
        dbOutput2 = cur2.fetchall()  
        session_date = dbOutput2[0][0]
        

        cur3 = getCursor()      # update trainer_session table,status column
        dbsql3 = ("""update trainer_sessions set session_status = 'available' where sessions_id = %s and date = %s""") # change the session status to available after someone cancelled it
        parameter3 = (sessionid,session_date)
        cur3.execute(dbsql3,parameter3)
        connection.commit()

        cur4 = getCursor()   # update booking table ,delete booking 
        dbsql4=("""delete from booking where session_id = %s and member_id = %s;""")
        parameter4 = (sessionid,userid)
        cur4.execute(dbsql4,parameter4)
        connection.commit()

        # no deleting payment

    return render_template("member/cancel.html",userid= userid,classid=classid,sessionid=sessionid)



















# gym system for admin------------------------------------------------------------------
# c1 manager-deactivate member

@app.route("/admin/deactivate/", methods=['POST', 'GET'])
def deactivate():
    if request.method == 'POST':
       cur = getCursor()
       dbsql = ("""update member
                   set subscription_status = 0 where balance < -20.00 ;""")    #change the subscription_status to deactive for all memebers with the balance under 0
       cur.execute(dbsql)
       connection.commit()

       cur2 = getCursor()
       dbsql2 = ("""SELECT * FROM member where balance  < -20.00 and subscription_status = 1;""")    #fetch the member with the balance under 20
       cur2.execute(dbsql2)
       dbOutput2 = cur2.fetchall() 
       return render_template("admin/deactivate.html",deactivate_success = "You deactivated all memebers with balance under 0 !",member_deactive = dbOutput2)
    else:
       
        cur = getCursor()
        dbsql = """SELECT * FROM member
                   WHERE balance < -20.00 AND subscription_status = 1;"""
        cur.execute(dbsql)
        dbOutput = cur.fetchall()
        return render_template("admin/deactivate.html", member_deactive=dbOutput)


# c2 manager-view member's profile
@app.route("/admin/memberprofile/")
def memberprofile():
    connection = getCursor()
    connection.execute("""SELECT * FROM member;""")
    memberList=connection.fetchall()
    return render_template("admin/memberprofile.html", memberlist =  memberList)

# c3 manager-update member's profile
@app.route("/admin/memberprofile/update", methods=['POST'])
def updatemember():
    member_detail = request.form
    member_id = member_detail.get('member_id')
    email = member_detail.get('email')
    phone = member_detail.get('phone')
    address = member_detail.get('address')
    # Update the member's profile
    cur = getCursor()
    dbsql = """UPDATE member SET email = %s, phone = %s, address = %s WHERE member_id = %s;"""
    parameters = (email, phone, address, member_id)
    cur.execute(dbsql, parameters)
    connection.commit()
    return redirect(url_for('memberprofile', member_id=member_id))



# c4 manager-add new member
@app.route("/admin/addmember/", methods=["GET","POST"])
def addmember():
    # format dates for the query
    if request.method == "POST": 
         # Get the form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        date_of_birth= request.form.get('date_of_birth') 
        # Check if the email address is already in use
        cur = getCursor()
        cur.execute("SELECT email FROM member WHERE email = %s", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            message = 'This email address is already in use.'
            return render_template("admin/addmember.html", message=message)
        # Validate phone number
        if not phone.isdigit() or len(phone[0]) > 10:
            message = 'Phone number must be number and less than 10-digit.'
            return render_template("admin/addmember.html", message=message)
    
        # Validate date of birth
        dob = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 14:
            message = "You must be older than 14 years old."
            return render_template("admin/addmember.html", message=message)
        
        # subscrtion date star and end
        current_date = date.today()
        future_date = current_date + timedelta(days=7)
        current_date_str = current_date.strftime('%Y-%m-%d')
        future_date_str = future_date.strftime('%Y-%m-%d')
        
        cur = getCursor()
        cur.execute("INSERT INTO user (password,role) VALUES ('aaa000','member')")
        userid = cur.lastrowid
        # Insert a new member with the user_id
        cur.execute('''
                INSERT INTO member (userid, first_name, last_name, email, phone, address, date_of_birth,subscription_status,subscription_start_date,subscription_end_date,balance)
                VALUES(%s,%s,%s,%s,%s,%s,%s,1,%s,%s,0.00)''',
                (userid, first_name, last_name, email, phone, address, date_of_birth,current_date_str,future_date_str))
    
        # Commit the transaction and redirect to member profile
        connection.commit()
        return redirect(url_for('memberprofile'))
    # Render the add member page if the request method is not POST
    return render_template("admin/addmember.html")

# c5 manager ---deducting member's subscription fee
@app.route("/admin/deduct/",methods=["GET","POST"])
def deduct():
    if request.method == "GET": 

        userid = request.args.get("userid")
        cur = getCursor()   # fetch current subscription end date for active members
        cur.execute("""select subscription_end_date from member where subscription_status = 1;""")
        dbOutput = cur.fetchall()

        try:
            current_sub_end_date = dbOutput[0][0]
        except IndexError:
            no_active='whoops, there are no active member now...'
            return render_template("admin/deduct.html", no_active=no_active, dbOutput=dbOutput)  
        return render_template("admin/deduct.html",current_sub_end_date=current_sub_end_date,userid=userid)
           

    if request.method == "POST": 
       deducted = 1
       cur = getCursor()   # fetch current balance info of all the active members
       cur.execute("""select balance from member where subscription_status = 1;""")
       dbOutput = cur.fetchall()
       before_deduct_balance_list = [x[0] for x in dbOutput]

       after_deduct_balance_list = [x - Decimal('20.00') for x in before_deduct_balance_list] 

       cur2 = getCursor()  # minus $20 from the balance for all the active members (our subscription fee is $20 per week)
       for i in range(len(after_deduct_balance_list)):
          sql = ("""UPDATE member SET balance = %s WHERE subscription_status = 1;""")
          parameter = (after_deduct_balance_list[i],)
       cur2.execute(sql,parameter)
       connection.commit()

       cur3 = getCursor() # extend 7 days to subscription end date for all the active member
       sql3 = ("""update member set subscription_end_date = %s where subscription_status = 1;""")
       parameter3 = (future_date,)
       cur3.execute(sql3,parameter3)
       connection.commit()
       return render_template("admin/deduct.html",seven_days_after = future_date,deducted=deducted)
    
    
# c6 As a manager, I want to filter the status of subscription so that I can see the people are overdue

# c7 manager---view member’s subscription status So that I can see who paid and overdue to keep track of the member’s subscription payment monthly
@app.route("/admin/subscription/", methods = ['POST','GET'])
def subscription():
    userid = request.args.get("userid")
    connection = getCursor()
    sql=("""SELECT member_id, first_name, last_name, subscription_status, subscription_start_date, subscription_end_date, balance FROM member where balance < 0;""")    #fetch the member info
    
    connection.execute(sql)
    dboutput=connection.fetchall()
    return render_template("admin/viewsubscription.html", mbersub_status= dboutput ,userid=userid)




# c8 As a manager, I want to delete a member. So that member can be current and up to date.
@app.route('/admin/memberprofile/delete', methods=['POST'])
def delete_member():
    member_id = request.form.get('id')

    cur1=getCursor()    # fetch userid
    sql1=("""select userid from member where member_id = %s;""")
    parameter1=(member_id,)
    cur1.execute(sql1,parameter1)
    dbOutput1 = cur1.fetchall()

    member_userid = dbOutput1[0][0]

    cur5 = getCursor()  # delet from payment
    cur5.execute('DELETE FROM payment WHERE member_id = %s', (member_userid,))
    connection.commit() 

    cur4 = getCursor()  # delet from attendance
    cur4.execute('DELETE FROM attendance WHERE member_id = %s', (member_userid,))
    connection.commit() 

    cur3 = getCursor()  # delet from booking
    cur3.execute('DELETE FROM booking WHERE member_id = %s', (member_userid,))
    connection.commit() 

    cur = getCursor()  # delete from member
    cur.execute('DELETE FROM member WHERE userid = %s', (member_userid,))
    connection.commit()

    cur2 = getCursor()  # delet from user
    cur2.execute('DELETE FROM user WHERE userid = %s', (member_userid,))
    connection.commit()
    
    return redirect(url_for('memberprofile'))


# c9 As manager , I want to view the most popular group classes , so that I can better understand member preferences and make informed decisions.
@app.route("/admin/popularclass/")
def popularclass():
    cur = getCursor()
   
    sql = ("""
        SELECT class_name, concat(t.first_name," ",t.last_name) ,SUM(book_space) as total_booked_spaces, date, time
        FROM group_class as g
			INNER JOIN trainer as t 
			ON t.userid=g.userid
        WHERE date >= %s - INTERVAL 7 DAY
        GROUP BY class_name
        ORDER BY total_booked_spaces DESC;
    """)
    parameter=(current_date,)
    cur.execute(sql,parameter)
    dbOutput = cur.fetchall()
    return render_template("admin/popularclass.html", classlist=dbOutput,current_date=current_date,week_ago=week_ago)


# c10 As a manager, I want to view financial report. So that I can know if the gym is making money.
@app.route("/admin/financialreport/month")
def financialreport():
    cur = getCursor()  # fetch all PT payments
    sql = ("""SELECT payment_id, date, amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 1 Month) and status="paid" and type = 'personal training session';""")
    cur.execute(sql)
    dbOutput = cur.fetchall()
    total_PT = 0
    for payment in dbOutput:
        total_PT += payment[2]
     
    cur1 = getCursor()  # fetch all subscription payments
    sql1 = ("""SELECT payment_id, date, amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 1 Month) and status="paid" and type = 'subscription';""")
    cur1.execute(sql1)
    dbOutput1 = cur1.fetchall()
    total_sub = 0
    for payment in dbOutput1:
        total_sub += payment[2]

    cur2 = getCursor()  # fetch all payments
    sql2 = ("""SELECT amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 1 Month) and status="paid";""")
    cur2.execute(sql2)
    dbOutput2 = cur2.fetchall()
    total = 0
    for payment in dbOutput2:
        total += payment[0]

    return render_template("admin/financialreport.html", payment_PT = dbOutput,payment_sub=dbOutput1, total = total,total_PT=total_PT,total_sub=total_sub)



@app.route("/admin/financialreport/year")
def financialreportyear():
    cur = getCursor()  # fetch all PT payments
    sql = ("""SELECT payment_id, date, amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 365 DAY) and status="paid" and type = 'personal training session';""")
    cur.execute(sql)
    dbOutput = cur.fetchall()
    total_PT = 0
    for payment in dbOutput:
        total_PT += payment[2]
     
    cur1 = getCursor()  # fetch all subscription payments
    sql1 = ("""SELECT payment_id, date, amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 365 DAY) and status="paid" and type = 'subscription';""")
    cur1.execute(sql1)
    dbOutput1 = cur1.fetchall()
    total_sub = 0
    for payment in dbOutput1:
        total_sub += payment[2]

    cur2 = getCursor()  # fetch all payments
    sql2 = ("""SELECT amount FROM payment where date >= DATE_SUB(NOW(), INTERVAL 365 DAY) and status="paid";""")
    cur2.execute(sql2)
    dbOutput2 = cur2.fetchall()
    total = 0
    for payment in dbOutput2:
        total += payment[0]

    return render_template("admin/financialreport.html", payment_PT = dbOutput,payment_sub=dbOutput1, total = total,total_PT=total_PT,total_sub=total_sub)


# c11 As a manager, I want to sends reminders to member when their subscription is due
@app.route("/admin/feenotification/")
def sendnotification():

    cur = getCursor()
    dbsql = ("""SELECT * FROM member
                    where balance  < -20.00;""")    #fetch the member with the balance under 20
    cur.execute(dbsql)
    dbOutput = cur.fetchall() 

    cur = getCursor()
    sql = ('SELECT email FROM lincoln_fitness_club.member where balance<0;')
    cur.execute(sql)
    email = cur.fetchall()
    
    for memberemail in email:

        email_sender = 'lincolngymgrp14@gmail.com'
        email_password = 'cbveueimbuahdbbg'
        email_receiver = memberemail[0]
        subject = 'subscription fee is due'
        body = 'Please login to our website, and pay your subscription fee. Thank you.'
        send_noti = 'Congratulations, you had send news to all member via email.'

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
    return render_template("admin/deactivate.html",member_deactive = dbOutput, send_noti=send_noti)


# c11 As a manager, I want to sends news and updates
import time
from flask import Response

@app.route("/admin/sendnews/", methods= ["GET","POST"])
def sendnews():
    if request.method =="GET":
        return render_template("admin/sendnews.html")
    else:
        
        mynews = request.form.get("mynews")
        cur = getCursor()
        sql = ('SELECT email FROM lincoln_fitness_club.member;')
        cur.execute(sql)
        email = cur.fetchall()

        # Define the progress bar function
        def generate():
            for i, memberemail in enumerate(email):
                email_sender = 'lincolngymgrp14@gmail.com'
                email_password = 'cbveueimbuahdbbg'
                email_receiver = memberemail[0]
                print(memberemail)
                subject = 'News from lincoln gym, something cool is happening'
                body = mynews
                news_pop = 'Congratulations, you had send news to all member via email.'

                em = EmailMessage()
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_receiver, em.as_string())

                # Calculate the progress and yield it to the client
                progress = int(((i+1)/len(email))*100)
                yield f"data:{progress}\n\n"
                time.sleep(1)

            # When all emails have been sent, yield 100% progress to the client
            yield "data:100\n\n"

        # Return a response object with the progress bar generator
        return Response(stream_with_context(generate()), mimetype="text/event-stream")




# c12 manager-- view member's attendance
@app.route("/admin/attendance/")
def attendance():
    memberid = request.args.get("memberid")

    cur2 = getCursor()  # fetch member userid
    sql2 =("""select userid from member where member_id = %s;""")
    parameter2 = (memberid,)
    cur2.execute(sql2,parameter2)
    dbOutput2 =cur2.fetchall()
    member_userid = dbOutput2[0][0]
    print(member_userid)

    cur = getCursor()  #fetch specific member's attendance of gym area
    sql =("""select m.member_id, m.first_name, m.last_name, m.subscription_status, a.date, a.timein,a.timeout from member as m
             join attendance as a
             on m.userid = a.member_id where m.userid = %s;""")
    parameter = (member_userid,)
    cur.execute(sql,parameter)
    dbOutput =cur.fetchall()

    cur1 = getCursor()  #fetch specific member's attendance of PT, which PT booking status just be 'completed' or 'no-show'
    sql1 =("""SELECT b.session_id, CONCAT(t.first_name,' ', t.last_name), b.date, b.booking_status
FROM booking AS b
JOIN trainer_sessions AS ts
ON b.session_id = ts.sessions_id
JOIN trainer AS t
ON ts.staff_id = t.userid  
WHERE b.member_id = %s
HAVING b.booking_status != 'booked'
ORDER BY b.date DESC;""")
    parameter1 = (member_userid,)
    cur1.execute(sql1,parameter1)
    dbOutput1 =cur1.fetchall()
    print(dbOutput)
    print(dbOutput1)
    if dbOutput or dbOutput1:
       return render_template("admin/attendance.html",dbOutput=dbOutput,dbOutput1=dbOutput1)
    else:
        return render_template("admin/attendance.html")

# c13-1 manager --view the payments
@app.route("/admin/viewpayment/",methods=['GET','POST'])
def viewpayment():  
   
    cur = getCursor()   # fetch all the payments that the status is 'pending' (not been processed)
    sql = ("""select * from payment where status = 'pending';""")
    cur.execute(sql)
    dbOutput = cur.fetchall()

    if dbOutput and request.method == "GET":  # showing all 'pending'
        return render_template("admin/viewpayment.html",payment = dbOutput)
    
    elif dbOutput and request.method == "POST":  # change all 'pending' to 'paid'
        processed=1
        cur1= getCursor()
        sql1=("""update payment set status = 'paid';""")
        cur1.execute(sql1)
        connection.commit()
        return render_template("admin/viewpayment.html",processed=processed)
    else:
        process_one = 'you had processed one payment'
        return render_template("admin/viewpayment.html",process_one=process_one)

    

# c13-2 manager --process the payments
@app.route("/admin/viewpayment/process/")
def process():
    userid = request.args.get("userid")
    paymentid = request.args.get("paymentid")



   
    
    # cur2 = getCursor()  # update member table, balance column(current balance + payment fee)
    # sql2 = ("""update member set balance = %s where userid = %s;""")
    # parameters2 = ((current_balance + Decimal(payment_amount)),userid)
    # cur2.execute(sql2,parameters2)
    # connection.commit()

    cur4 = getCursor()  #update payment table, change status
    sql4 = ("""update payment set status = 'paid' where payment_id = %s;""")
    parameter = (paymentid,)
    cur4.execute(sql4,parameter)
    connection.commit()

    cur3 = getCursor()   # fetch all the payments that the status is 'pending' (not been processed)
    sql3 = ("""select * from payment where status = 'pending';""")
    cur3.execute(sql3)
    dbOutput3 = cur3.fetchall()

    



    return render_template("admin/viewpayment.html", process_one = "processed one payment successfully!",payment = dbOutput3)

# c14-1 manager--view trainer
@app.route("/admin/viewtrainers/")
def viewtrainers():
    cur = getCursor()
    sql= ("""select * from trainer;""")
    cur.execute(sql)
    dbOutput=cur.fetchall()
    return render_template("admin/viewtrainers.html",dbOutput=dbOutput)
# c14-2 manager--view trainer's classes
@app.route("/admin/viewtrainers/groupclass/")
def viewtrainers_groupclass():
    trainer_user_id = request.args.get("trainer_user_id")

    cur = getCursor()  # fetch all the group classes under this trainer from today to 7 days later
    sql=("""select g.class_name, g.date, g.time, g.book_space, g.max_space, t.userid, t.first_name, t.last_name 
           from group_class as g
           join trainer as t
           on g.userid = t.userid where t.userid = %s and date > %s and date < %s;""")
    parameters = (trainer_user_id,current_date, future_date)
    cur.execute(sql,parameters)
    dbOutput = cur.fetchall()
    
    return render_template("admin/viewtrainers_groupclass.html", dbOutput=dbOutput,today=current_date,seven_days_later=future_date)




