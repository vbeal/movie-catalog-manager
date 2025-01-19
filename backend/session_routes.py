from flask import render_template, request, session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from bson import ObjectId

bcrypt = Bcrypt()

def initialize_session_routes(app, db):
    @app.route("/login", methods=["GET", "POST"])
    def login_page():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = db.users.find_one({"username": username})
            if user and bcrypt.check_password_hash(user["password"], password):
                session["user"] = username
                session["role"] = user.get("role", "common")
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("dashboard"))
            flash("Credenciais inválidas!", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logout realizado com sucesso!", "info")
        return redirect(url_for("login_page"))

    @app.route("/dashboard")
    def dashboard():
        if "user" not in session:
            flash("Por favor, faça login para acessar o painel.", "warning")
            return redirect(url_for("login_page"))

        users = db.users.find() if session.get("role") == "master" else []
        return render_template("dashboard.html", user=session["user"], users=users)
