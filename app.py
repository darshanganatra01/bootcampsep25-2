from flask import Flask,render_template,request,redirect

app=Flask(__name__)



# if person comes for the first time
# do this task

# when user comes in to the ('/')
# i have not given any instructions in my app

#/-->landing , '/login'--->login page


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/login',methods=["GET","POST"])  
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"Email: {email}, Password: {password}")\

        #verufy the user in the db
        #Dashboard
        #if yes
        return redirect('/dashboard')
    
        #else
        #return redirect('/signup')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
