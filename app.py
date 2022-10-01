from flask import Flask, render_template, redirect, url_for, flash, session, request
from Database import User, Cars
from flask_bcrypt import generate_password_hash, check_password_hash

app: Flask = Flask(__name__)
app.secret_key = "Twisterzen2900"


@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        userName = request.form["u_name"]
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        encryptedUserPassword = generate_password_hash(userPassword)
        User.create(name=userName, email=userEmail, password=encryptedUserPassword)
        flash("User created successfully")

    return render_template("signup.html")


@app.route('/index')
def index():
    return render_template("updatecars.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        userEmail = request.form["u_email"]
        userPassword = request.form["u_pass"]
        try:
            user = User.get(User.email == userEmail)
            encryptedPassword = user.password
            if check_password_hash(encryptedPassword, userPassword):
                flash("Login successful")
                session["loggedIn"] = True
                session["userName"] = user.name

                return redirect(url_for("home"))
        except:
            flash("wrong email or password")

    return render_template("login.html")


@app.route("/add_product", methods=["GET", "POST"])
def addcars():
    if not session["loggedIn"]:
        return redirect(url_for("login"))

    if request.method == "POST":
        carName = request.form["name"]
        carQuantity = request.form["quantity"]
        carPrice = request.form["price"]
        Cars.create(name=carName, quantity=carQuantity, price=carPrice)
        flash("Product created successfully")

    return render_template("addcars.html")


@app.route("/cars")
def cars():
    if not session["loggedIn"]:
        return redirect(url_for("login"))

    cars = Cars.select()
    return render_template("cars.html", products=cars)


@app.route("/delete/<int:id>")
def delete(id):
    if not session["loggedIn"]:
        return redirect(url_for("login"))

    Cars.delete().where(Cars.id == id).execute()
    flash("Product deleted successfully")
    return redirect(url_for("products"))


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update():
    if not session["loggedIn"]:
        return redirect(url_for("login"))

    if request.method == "POST":
        car = Cars.get(Cars.id == id)
        updatedName = request.form["name"]
        updatedQuantity = request.form["quantity"]
        updatedPrice = request.form["price"]
        car.name = updatedName
        car.quantity = updatedQuantity
        car.price = updatedPrice
        car.save()
        flash("Product updated successfully")
        return redirect(url_for("products"))
    return render_template("update_product_page.html", car=cars)


@app.route('/logout')
def logout():
    if not session.get("logged in"):
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
