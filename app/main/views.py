from itertools import product
from flask import render_template,request,redirect,url_for, abort
from . import main
from flask_login import login_required, current_user
from ..models import Pitch, Comment, User
from .forms import PitchForm,CommentForm,UpdateProfile
from .. import db, photos

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitches = Pitch.query.all()
    product = Pitch.query.filter_by(category = 'Product').all()
    interview = Pitch.query.filter_by(category = 'Interview').all()
    promotion = Pitch.query.filter_by(category = 'Promotion').all()
    Pickup = Pitch.query.filter_by(category = 'Pickup')

    return render_template('index.html', product = product, interview = interview, promotion = promotion, Pickup = Pickup )

@main.route('/pitches/new_pitch',methods = ['GET','POST'])
@login_required
def new_pitch():
  form = PitchForm()
  
  if form.validate_on_submit():
    category =form.category.data
    pitch =form.pitch.data
    
    #pitch instance
    new_pitch =  Pitch(pitch=pitch,category=category)
    
    #save_pitch
    new_pitch.save_pitch()
    return redirect(url_for('.new_pitch'))

    
  return render_template('new_pitch.html', pitch_form=form )

@main.route('/pitches/comment/<int:pitch_id>',methods = ['GET','POST'])
@login_required
def new_comment(pitch_id):
    form = CommentForm()
    comments = Comment.get_comments(pitch_id)
    
    if form.validate_on_submit():
        comment = form.comment.data
        pitch_id = pitch_id
        new_comment = Comment(comment = comment, pitch_id=pitch_id)
        
        
        new_comment.save_comment()
        return redirect(url_for('.index',form =form,pitch_id =pitch_id))
    
    return render_template('comments.html', comment_form =form, comments = comments, pitch_id =pitch_id)

@main.route('/pitches')
def get_pitches():
    user = User.query.filter_by(username = 'uname').first()
    pitches = Pitch.query.all()
    user = current_user

    return render_template ('pitch.html',pitches = pitches, user = user)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id =current_user.id
    my_pitches = Pitch.query.filter_by(user_id = user_id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/pitches/Product') 
@login_required
def product_pitches():
    all_pitches = Pitch.query.all() 
    product =  Pitch.query.filter_by(category = 'product').all()
    
    
    return render_template('product.html', product = product)


@main.route('/pitches/Interview') 
@login_required
def Interview_pitches():
    all_pitches = Pitch.query.all() 
    interview =  Pitch.query.filter_by(category = 'interview').all()
    
    
    return render_template('interview.html', interview = interview)

@main.route('/pitches/Promotion') 
@login_required
def promotion_pitches():
    all_pitches = Pitch.query.all() 
    promotion =  Pitch.query.filter_by(category = 'Promotion').all()
    
    
    return render_template('promotion.html', promotion = promotion)

@main.route('/pitches/Pick-up') 
@login_required
def Pickup_pitches():
    all_pitches = Pitch.query.all() 
    pick_up =  Pitch.query.filter_by(category = 'Pick-up').all()
    
    
    return render_template('pickup.html', pick_up=pick_up)