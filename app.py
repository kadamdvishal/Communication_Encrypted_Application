from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import ceasar_cipher as cc
import database as db 

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

email = ""
plain_text = ""
encrypted_text = ""
messages = []
images = []

def authenticate(email, password):
    exist = False
    users = db.select_users()
    for user in users:
        if((user[1] == email) and (user[2] == password)):
            exist = True
    if(exist):
        print("User found, logging in...")
    else:
        print("User not found, registering...")
        db.register_user(email, password)


@app.route('/encrypt/', methods=['GET', 'POST'])
def encrypt():
    global plain_text
    global encrypted_text
    if (request.method == 'POST'):
        plain_text = request.form['plain-text']
        encrypted_text = "".join(cc.encode(plain_text, 3))
        return render_template('home.html', email=email, plain_text=plain_text, encrypted_text=encrypted_text, messages=messages)
    else:
        return render_template('home.html')


@app.route('/decrypt/', methods=['GET', 'POST'])
def decrypt():
    if (request.method == 'POST'):
        decrypted_text = "".join(cc.decode(encrypted_text, 3))
        return render_template('home.html', email=email, plain_text=plain_text, encrypted_text=encrypted_text, decrypted_text=decrypted_text, messages=messages)
    else:
        return render_template('home.html')


@app.route('/send/', methods=['GET', 'POST'])
def send():
    if(request.method == 'POST' and 'photo' in request.files):
        recipient = request.form['recipient']
        filename = photos.save(request.files['photo'])
        db.create_images_table()
        db.send_email(email, recipient, encrypted_text)
        db.send_image(email, recipient, filename)
        return render_template('home.html', email=email, plain_text=plain_text, encrypted_text=encrypted_text, messages=messages)
    if (request.method == 'POST'):
        recipient = request.form['recipient']
        db.send_email(email, recipient, encrypted_text)
        return render_template('home.html', email=email, plain_text=plain_text, encrypted_text=encrypted_text, messages=messages)
    else:
        return render_template('home.html')

@app.route('/home/', methods=['GET', 'POST'])
def home():
    global email
    if (request.method == 'POST'):
        email = request.form['email']
        password = request.form['pw']
        db.create_connection()
        authenticate(email, password)
        for item in db.get_messages():
            if(item[1] == email):
                messages.append(
                    (item[0], item[2], "".join(cc.decode(item[2], 3))))
        for item in db.get_images():
            if(item[1] == email):
                images.append(
                    (item[0], item[2]))
        return render_template('home.html', email=email, messages=messages, images=images)
    else:
        return render_template('login.html')


@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
