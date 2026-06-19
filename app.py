from flask import Flask, render_template, request, redirect, session, flash
from supabase import create_client
from flask_mail import Mail, Message    
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("SUPABASE_URL =", SUPABASE_URL)
print("SUPABASE_KEY EXISTS =", bool(SUPABASE_KEY))

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Sample stats data
stats = [
    {"value": "1200+", "title": "Total Volunteers"},
    {"value": "350+", "title": "Events Conducted"},
    {"value": "50K+", "title": "Beneficiaries Reached"},
    {"value": "80+", "title": "Partner Organizations"}
]

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html', stats=stats)

@app.route('/register', methods=['GET', 'POST'])
def register():

 if request.method == 'POST':

    data = {
        "full_name": request.form["full_name"],
        "email": request.form["email"],
        "phone": request.form["phone"],
        "age": request.form["age"],
        "gender": request.form["gender"],
        "city": request.form["city"],
        "skills": request.form["skills"],
        "availability": request.form["availability"],
        "program": request.form["program"],
        "reason": request.form["reason"]
    }

    # Save to Supabase
    supabase.table("volunteers").insert(data).execute()

    # Send Email
    msg = Message(
    subject="Welcome to NayePankh Foundation",
    sender=app.config['MAIL_USERNAME'],
    recipients=[data["email"]]
)

    msg.html = f"""
    <h2>Welcome {data['full_name']} 🎉</h2>

    <p>Thank you for registering as a volunteer.</p>

    <p>We have successfully received your application.</p>

    <p>Our team will contact you soon.</p>
    """

    mail.send(msg)

    # Success Page
    return render_template(
        "success.html",
        volunteer_name=data["full_name"]
    )

 return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        print("Entered Email:", email)
        print("Entered Password:", password)

        print("Admin Email:", admin_email)
        print("Admin Password:", admin_password)

        if email == admin_email and password == admin_password:
            session['admin'] = True
            session['admin_email'] = email

            return redirect('/dashboard')

        flash("Invalid email or password", "danger")

    return render_template('login.html')


@app.route('/programs')
def programs():
    return render_template('programs.html')

@app.route('/dashboard')
def dashboard():

    if not session.get('admin'):
        return redirect('/login')

    response = (
        supabase
        .table("volunteers")
        .select("*")
        .execute()
    )

    volunteers = response.data or []

    total_volunteers = len(volunteers)

    education = len([
        v for v in volunteers
        if v.get("program") == "Education Support"
    ])

    youth = len([
        v for v in volunteers
        if v.get("program") == "Youth Empowerment"
    ])

    community = len([
        v for v in volunteers
        if v.get("program") == "Community Development"
    ])

    skill = len([
        v for v in volunteers
        if v.get("program") == "Skill Development"
    ])

    return render_template(
        "dashboard.html",
        volunteers=volunteers,
        total_volunteers=total_volunteers,
        education=education,
        youth=youth,
        community=community,
        skill=skill
    )

@app.route('/delete/<int:id>')
def delete_volunteer(id):

    if not session.get('admin'):
        return redirect('/login')

    supabase.table("volunteers") \
        .delete() \
        .eq("id", id) \
        .execute()

    return redirect('/dashboard')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():

    if not session.get('admin'):
        return redirect('/login')

    response = (
        supabase
        .table("volunteers")
        .select("*")
        .execute()
    )

    volunteers = response.data

    return render_template(
        'admin.html',
        volunteers=volunteers
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)