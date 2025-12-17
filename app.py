from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============================================================
# MODELS
# ============================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    name = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)  # fixed to real Date type
    category = db.Column(db.String(100))
    notes = db.Column(db.Text)

# ============================================================
# LOGIN REQUIRED DECORATOR
# ============================================================

def login_required(f):
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ============================================================
# AUTH ROUTES
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Please provide username and password.", "error")
            return redirect(url_for("register"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "error")
            return redirect(url_for("register"))

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now login.", "success")
        return redirect(url_for("login"))

    return render_template("login.html", register=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Please provide username and password.", "error")
            return redirect(url_for("login"))

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["username"] = user.username

        flash("Logged in successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html", register=False)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# ============================================================
# EXPENSE ROUTES (REQUIRE LOGIN)
# ============================================================

@app.route("/", methods=["GET"])
@login_required
def index():
    user_id = session["user_id"]
    query = Expense.query.filter_by(user_id=user_id)

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        query = query.filter(Expense.date >= start_obj)
    if end_date:
        end_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(Expense.date <= end_obj)

    expenses = query.order_by(Expense.date.desc()).all()

    return render_template("index.html",
                           expenses=expenses,
                           start_date=start_date,
                           end_date=end_date)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    if request.method == "POST":
        name = request.form["name"]
        amount = float(request.form["amount"] or 0)
        date_str = request.form["date"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        category = request.form["category"]
        notes = request.form["notes"]

        new_expense = Expense(
            user_id=session["user_id"],
            name=name,
            amount=amount,
            date=date_obj,
            category=category,
            notes=notes
        )

        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added.", "success")
        return redirect(url_for("index"))

    return render_template("add_expense.html", expense=None)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)

    if expense.user_id != session["user_id"]:
        return "Unauthorized", 403

    if request.method == "POST":
        expense.name = request.form["name"]
        expense.amount = float(request.form["amount"] or 0)
        date_str = request.form["date"]
        expense.date = datetime.strptime(date_str, "%Y-%m-%d").date()
        expense.category = request.form["category"]
        expense.notes = request.form["notes"]
        db.session.commit()
        flash("Expense updated.", "success")
        return redirect(url_for("index"))

    return render_template("add_edit_expense.html", expense=expense)


@app.route("/delete/<int:id>")
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)

    if expense.user_id != session["user_id"]:
        return "Unauthorized", 403

    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted.", "success")
    return redirect(url_for("index"))

# ============================================================
# ADDED ROUTE: EXPENSE LIST PAGE
# ============================================================

@app.route("/expenses")
@login_required
def expenses():
    user_id = session["user_id"]
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
    return render_template("expenses.html", expenses=expenses)

# ============================================================
# DASHBOARD WITH DATE FILTERING
# ============================================================

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user_id = session["user_id"]
    query = Expense.query.filter_by(user_id=user_id)

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        query = query.filter(Expense.date >= start_obj)
    if end_date:
        end_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(Expense.date <= end_obj)

    expenses = query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)

    categories = {}
    for e in expenses:
        categories[e.category or "Uncategorized"] = categories.get(e.category or "Uncategorized", 0) + e.amount

    return render_template(
        "dashboard.html",
        total=total,
        categories=categories,
        expenses=expenses,
        start_date=start_date,
        end_date=end_date
    )

# ============================================================
# REPORT
# ============================================================

@app.route("/report")
@login_required
def report():
    user_id = session["user_id"]
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template("report.html", expenses=expenses, total=total)

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Seed sample data (only if no users exist)
        if not User.query.first():
            hashed_pw = generate_password_hash("password123")
            user = User(username="Louise", password=hashed_pw)
            db.session.add(user)
            db.session.commit()

            sample_expense = Expense(
                user_id=user.id,
                name="Sample Expense",
                amount=100.0,
                date=date.today(),
                category="Food",
                notes="Test data"
            )
            db.session.add(sample_expense)
            db.session.commit()

    app.run(debug=True)
