from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(250), unique=True, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, default=False, nullable=False)
    has_toilet = db.Column(db.Boolean, default=False, nullable=False)
    has_wifi = db.Column(db.Boolean, default=False, nullable=False)
    can_take_calls = db.Column(db.Boolean, default=False, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Image Of The Place (URL)', validators=[DataRequired(), URL()])
    location = StringField('Location e.g. Cairo, Egypt', validators=[DataRequired()])
    seats = SelectField("Number Of Seats", choices=["0-10", "10-20", "20-30", "30-40", "40-50", "50+"],
                        validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    has_sockets = BooleanField('Has Sockets?')
    has_toilet = BooleanField('Has Toilet?')
    has_wifi = BooleanField('Has Wifi?')
    can_take_calls = BooleanField('Can Take Calls?')

    submit = SubmitField('Submit')


@app.route("/")
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/add', methods=["POST", "GET"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


@app.route("/delete/<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
