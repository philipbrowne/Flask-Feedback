from flask import Flask, render_template, request, redirect, session, flash, abort
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import NewUserForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    """Redirects user to register"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register user to database"""
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data

        password = User.register(username, form.password.data).password
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors = ['Sorry - that username is already taken!']
            return render_template('register.html', form=form)
        flash(f'Welcome {new_user.username}!', 'success')
        session['username'] = new_user.username
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in user based on credentials"""
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {user.username}!', 'success')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid Username/Password']
    return render_template('login.html', form=form)

@app.route('/secret')
def show_secret_page():
    """Shows secret page to registered and logged in user!"""
    if 'username' not in session:
        flash('Please log in first', 'danger')
        return redirect('/login')
    else:
        return render_template('secret_page.html')

@app.route('/logout')
def log_out():
    """Logs out user"""
    session.pop('username')
    flash('User logged out!', 'success')
    return redirect('/')
    

@app.route('/users/<username>')
def show_user_info(username):
    """Shows information on user based on their username"""
    user = User.query.filter(User.username == username).first()
    if 'username' not in session and user.is_admin == False:
        flash('Please login first!', 'danger')
        return redirect('/login')
    if not user:
        abort(404)
    return render_template('user_details.html', user=user)
        
        
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    curr_user = User.query.filter(User.username == session.get('username')).first()
    user = User.query.filter(User.username == username).first()
    if session.get('username') != username and curr_user.is_admin == False:
        flash('Must be logged in as user to delete', 'danger')
        return redirect('/')
    else:
        deleted_user = User.query.filter(User.username == username).first()
        db.session.delete(deleted_user)
        db.session.commit()
        if User.query.filter(User.username == session.get('username')).first().is_admin == False:
            session.pop('username')
        flash('User deleted', 'success')
        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def get_feedback_form(username):
    """Display a form to add feedback"""
    curr_user = User.query.filter(User.username == session.get('username')).first()
    if session.get('username') != username and curr_user.is_admin == False:
        flash('Must be logged in as that user to add feedback', 'danger')
        return redirect('/')
    form = FeedbackForm()
    user = User.query.filter(User.username == username).first()
    if form.validate_on_submit():
        title = form.title.data 
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('New feedback added!', 'success')
        return redirect(f'/users/{username}')
    return render_template('feedback_form.html', form=form, user=user)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Form to edit feedback"""
    curr_user = User.query.filter(User.username == session.get('username')).first()
    feedback = Feedback.query.get_or_404(feedback_id)
    if session.get('username') != feedback.username and curr_user.is_admin == False:
        flash('Must be logged in as that user', 'danger')
        return redirect('/')
    form = FeedbackForm()
    user = User.query.filter(User.username == feedback.username).first()
    if request.method == 'GET':
        form.title.data = feedback.title
        form.content.data = feedback.content
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback updated', 'success')
        return redirect(f'/users/{user.username}')
    return render_template('edit_feedback.html', form=form, feedback=feedback, user=user)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback_item(feedback_id):
    """Delete feedback"""
    curr_user = User.query.filter(User.username == session.get('username')).first()
    feedback = Feedback.query.get_or_404(feedback_id)
    if session.get('username') != feedback.username and curr_user.is_admin == False:
        flash('Must be logged in as that user', 'danger')
        return redirect('/')
    user = User.query.filter(User.username == feedback.username).first()
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback item deleted!', 'success')
    return redirect(f'/users/{user.username}')
        
# http://localhost:5000/feedback/1/update