from flask import Flask, render_template, redirect, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from config import db
from forms import AddPetForm, EditPetForm
from models import Pet


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.init_app(app)
toolbar = DebugToolbarExtension(app)


@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(name=form.name.data, species=form.species.data, 
                      photo_url=form.photo_url.data, age=form.age.data, 
                      notes=form.notes.data, available=True)
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if request.method == 'POST':
        if form.validate_on_submit():
            pet.photo_url = form.photo_url.data
            pet.notes = form.notes.data
            pet.available = form.available.data
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('pet_detail.html', form=form, pet=pet)

    return render_template('pet_detail.html', pet=pet, form=form)
if __name__ == '__main__':
    app.run(debug=True)