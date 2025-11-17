from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootcamp.db'
app.config['SECRET_KEY'] = 'ahdbdfhbflkdc'

db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    #Customer #Admin #Theatre

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    franchise = db.Column(db.String(150), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(Customer.id), nullable=True)
    theatre_id = db.Column(db.Integer, db.ForeignKey(Theatre.id), nullable=False)
    show_time = db.Column(db.Date,nullable=False)
    show_date = db.Column(db.Date,nullable=False)
    status = db.Column(db.String(50), nullable=False)  #Available/Booked/Cancelled

class CompBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey(Booking.id), nullable=False)
    feedback = db.Column(db.String(500), nullable=True)

















# Availability 
# Cancelation

# Days theatre is going to create slot
# id   cid   tid   time   date   status
# 1          2     6 pm   10-11  Available


# Customer Comes and Books
# id   cid   tid   time   date   status
# 1     3    2     6 pm   10-11  Booked


# Customer Cancels
# id   cid   tid   time   date   status
# 1    null  2     6 pm   10-11  Available


#Theatre can cancel a slot which they have made available 
#remove that entry from the table


#Cancel status
#Booking cancleation by thetre
#other core requirements




# if person comes for the first time
# do this task

# when user comes in to the ('/')
# i have not given any instructions in my app

#/-->landing , '/login'--->login page

@app.route('/')
def home():
    print(session)
    return render_template('landing.html')

#CUSTOMER
@app.route('/customer_login',methods=["GET","POST"])  
def login():
    if request.method == "GET":
        return render_template('customer_login.html')
    else:
        form_email = request.form.get("email")
        form_password = request.form.get("password")

        #i am going to check if that user exists in the database or not
        user_exist = User.query.filter_by(email=form_email,role="customer").first()
        if user_exist:
            #check the password
            if user_exist.password == form_password:
                flash("login successful")
                session["role"]="customer"
                session["email"]=user_exist.email
                return redirect('/dashboard')
            else:
                flash("incorrect password")
                return redirect('/customer_login')
        else:
            flash("user does not exist")
            return redirect('/signup')
        

@app.route('/theatre_login',methods=["GET","POST"])
def theatre_login():
    if request.method == "GET":
        return render_template('theatre_login.html')
    else:
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        
        #i am going to check if that user exists in the database or not
        user_exist = User.query.filter_by(email=form_email,role="theatre").first()
        if user_exist:
            #check the password
            if user_exist.password == form_password:
                flash("login successful")
                session["role"] = "theatre"
                session["email"] = user_exist.email
                return redirect('/dashboard')
            else:
                flash("incorrect password")
                return redirect('/theatre_login')
        else:
            flash("These credentials doesnt exist please check with admin")
            return redirect('/theatre_login')
        
        
@app.route('/admin_login',methods=["GET","POST"])
def admin_login():  
    if request.method == "GET":
        return render_template('admin_login.html')
    else:
        form_email = request.form.get("email")
        form_password = request.form.get("password")

        #i am going to check if that user exists in the database or not
        user_exist = User.query.filter_by(email=form_email,role="admin").first()
        if user_exist:
            #check the password
            if user_exist.password == form_password:
                flash("login successful")
                session["role"]="admin"
                session["email"]=user_exist.email
                return redirect('/dashboard')
            else:
                flash("incorrect password")
                return redirect('/admin_login')
        else:
            flash("These credentials doesnt exist please contact support")
            return redirect('/admin_login')


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        form_email = request.form.get("email")
        form_password = request.form.get("password")
        form_name = request.form.get("name")
        form_age = request.form.get("age")

        #i am going to check if that user exists in the database or not

        user_exist = User.query.filter_by(email=form_email).first()
        if user_exist:
            flash("user already exists")
            return redirect('/customer_login')
        else:
            new_user = User(email=form_email,password=form_password,role="customer")
            db.session.add(new_user)
            db.session.commit()
            flash("user created successfully")

            new_customer = Customer(name=form_name,age=form_age,user_id=new_user.id)
            db.session.add(new_customer)
            db.session.commit()
            flash("customer created successfully")

            return redirect('/customer_login')


@app.route('/dashboard')
def dashboard():
    #role is customer show customer dashboard
    #if role is theatre show theatre dashboard
    #if role is admin show admin dashboard

    role = session.get("role")   #session["role"]
    print(role)
    if role == "customer":
        return render_template("customer_dashboard.html")
    elif role == "theatre":
        return render_template("theatre_dashboard.html")
    elif role == "admin":
        return render_template("admin_dashboard.html")
    else:
        print("user had not logged in")
        return redirect('/landing')
    



def auto_admin_creation():
    #i need to find in the user table if a user with role column name admin
    #exists
    #if exists then do nothing
    #but if not exist then you create one 
    admin_check = User.query.filter_by(email="admin@gmail.com",role="admin").first()
    if not admin_check:
        admin_user = User(email="admin@gmail.com",password="admin123",role="admin")
        db.session.add(admin_user)
        db.session.commit()
        print("admin created")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        auto_admin_creation()
    app.run(debug=True)
