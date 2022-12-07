import validators
from flask import Flask
from werkzeug.security import generate_password_hash
from decorators import *
app = Flask(__name__)
app.debug = True

incorrect = "Only admin has access to do this operation"


@app.route('/')
def home():
    return jsonify({"message":"Welcome to Digital Library"})


@app.route('/register', methods=["POST"])
def register():
    if request.method == "POST":
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        phone_number = request.args.get('phone_number')
        email = request.args.get('email')
        password = request.args.get('password')

        if not first_name.replace(" ", "").isalpha():
            return jsonify({"message": "Please enter a valid first name, First name should contain only alphabets"}), 400

        if not last_name.replace(" ", "").isalpha():
            return jsonify({"message": "Please enter a valid last name, Last name should contain only alphabets"}), 400

        if not phone_number_validator(phone_number):
            return jsonify({"message": "Please enter a valid phone number"}), 400

        if not validators.email(email):
            return jsonify({'error': "Email is invalid"}), 400

        if not is_password(password):
            return jsonify({'error': "Enter valid password, Password should contain a "
                                     "Uppercase value, special character and should contain a numeric value"}), 400

        pwd_hash = generate_password_hash(password)
        print(first_name,last_name,phone_number,email,pwd_hash)

        check1 = session.query(user_details).filter(user_details.c.email == email)
        res = check1.all()

        if res:
            return jsonify({"message": "Account already exists"}), 403

        ins = user_details.insert().values(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
        conn.execute(ins)

        return jsonify({"message": "User registered successfully"}), 200


@app.route('/login/<email>/<password>', methods = ["GET"])
def login(email, password):
    if request.method == "GET":
        check = session.query(user_details).filter(user_details.c.email == email, user_details.c.password == password)

        result = check.all()

        if not result:
            return jsonify({"message": incorrect}), 401
        else:
            return jsonify({'message': 'Logged in successfully'}), 200


@app.route('/get/<id>', methods=['GET'])
def get_book_details(id):
    if request.method == "GET":

        check1 = session.query(book_details).filter(book_details.c.id == id)
        result = check1.all()
        if not result:
            jsonify({"message": "Enter valid book id"})
        return jsonify({"message": result}), 200


@app.route('/<email>/<password>/fetch_all_book', methods=["GET"])
def fetch_all_book(email, password):
    if request.method == "GET":
        check = session.query(user_details).filter(user_details.c.email == email, user_details.c.password == password)

        result = check.all()

        if not result:
            return jsonify({"message": "The email and password given for the user is incorrect."}), 400
        else:
            query = db.select([book_details])
            result = engine.execute(query)
            resultset = result.fetchall()
            return jsonify({'result': [dict(row) for row in resultset]}), 200


@app.route('/add_book', methods=["POST"])
@admin_login_required
def add_book():
    if request.method == "POST":

        book_name = request.args.get('book_name')
        author_name = request.args.get('author_name')
        published_year = request.args.get('published_year')
        count = request.args.get('count')
        print("book_name,author_name,published_year,Count", book_name, author_name, published_year, count)

        ins = book_details.insert().values(book_name=book_name, author_name=author_name,
                                           published_year=published_year, count=count)
        conn.execute(ins)

        return jsonify({'message': 'Book added successfully'}), 200


@app.route('/fetch_book', methods=["GET"])
@admin_login_required
def fetch_book():
    if request.method == "GET":
        query = db.select([book_details])
        result = engine.execute(query)
        resultset = result.fetchall()
        return jsonify({'result': [dict(row) for row in resultset]}), 200


@app.route('/update_count/<id>', methods=["PUT"])
@admin_login_required
def update_count(id):
    if request.method == "PUT":

        count = request.args.get('count')
        update = book_details.update().where(book_details.c.id == id).values(count=count)
        conn.execute(update)

        return jsonify({'message': 'Book updated successfully'}), 200


@app.route('/delete_book/<id>', methods=["DELETE"])
@admin_login_required
def delete_book(id):
    if request.method == "DELETE":

        check1 = session.query(book_details).filter(book_details.c.id == id)
        res = check1.all()
        print(res)
        if not res:
            return jsonify({"message": "Enter valid book id"}), 400
        else:
            delete = book_details.delete().where(book_details.c.id == id)
            conn.execute(delete)
            print("hi")
            return jsonify({"message": "Book deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5555)