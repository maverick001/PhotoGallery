from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from datetime import datetime
from .forms import LoginForm, ClientRegistrationForm, PhotographerRegistrationForm
from .forms import BookingForm, ImageUploadForm, PaymentForm, AddPhotographerForm
from . import db
from .wrappers import admin_required


bp = Blueprint('main', __name__)

def is_logged_in():
    return 'user' in session and session['user'] is not None


def get_current_user():
    return session.get('user', None)



@bp.route('/')
def index():
    categories = db.get_all_categories()
    return render_template('index.html', categories=categories)


@bp.route('/photographers')
@bp.route('/vendor_gallery')
def vendor_gallery():
    
    selected_category = request.args.get('category', None)

    photographers = db.get_all_photographers()

    
    photographer_images = {
        'P01': ['wedding1.png', 'wedding2.png', 'wedding3.png', 'wedding4.png'],
        'P02': ['corporate2.png', 'events.png', 'events2.png', 'product.png'],
        'P03': ['family1.png', 'baby.png', 'dog.png', 'friends.png'],
        'P04': ['model.png', 'wedding5.png', 'wedding6.png', 'portraits.png'],
        'P05': ['product.png', 'products.png', 'corporate.png', 'image-3.png']
    }


    category_photographers = {
        'Cat01': ['P01'],  
        'Cat02': ['P02'],  
        'Cat03': ['P03'],  
        'Cat04': ['P04'], 
        'Cat05': ['P05']   
    }


    if selected_category and selected_category in category_photographers:
        allowed_photographer_ids = category_photographers[selected_category]
        photographers = [p for p in photographers if p['PhotographerID'] in allowed_photographer_ids]

        
        category_info = db.get_category_by_id(selected_category)
    else:
        category_info = None

 
    photographer_data = []
    for photographer in photographers:
        photographer_id = photographer['PhotographerID']
        bookings = db.get_bookings_by_photographer(photographer_id)

        
        image_files = photographer_images.get(photographer_id, ['wedding.png'])

        photographer_data.append({
            'photographer': photographer,
            'image_files': image_files,
            'bookings': bookings
        })

    return render_template('vendor_gallery.html',
                         photographer_data=photographer_data,
                         selected_category=category_info)


@bp.route('/photographer/<photographer_id>')
def photographer_detail(photographer_id):
    photographer = db.get_photographer_by_id(photographer_id)
    if not photographer:
        flash('Photographer not found', 'error')
        return redirect(url_for('main.vendor_gallery'))

    images = db.get_images_by_photographer(photographer_id)
    bookings = db.get_bookings_by_photographer(photographer_id)

    return render_template('photographer_detail.html',
                         photographer=photographer,
                         images=images,
                         bookings=bookings)


@bp.route('/book/<photographer_id>', methods=['GET', 'POST'])
def book_session(photographer_id):
    if not is_logged_in():
        flash('Hi there, Please login to book a session', 'error')
        return redirect(url_for('main.login'))

    photographer = db.get_photographer_by_id(photographer_id)
    if not photographer:
        flash('Photographer not found', 'error')
        return redirect(url_for('main.vendor_gallery'))

    form = BookingForm()

    
    categories = db.get_all_categories()
    form.category_id.render_kw = {'list': 'categories'}

    if request.method == 'POST':
  
        descriptions = request.form.get('descriptions')
        location = request.form.get('location')
        start_time_str = request.form.get('start_time')
        duration = request.form.get('duration')

        photographer_category_map = {
            'P01': 'Cat01',  
            'P02': 'Cat02',  
            'P03': 'Cat03',  
            'P04': 'Cat04',  
            'P05': 'Cat05'   
        }
        category_id = photographer_category_map.get(photographer_id, 'Cat01')

        is_available = db.check_photographer_availability(
            photographer_id,
            start_time_str,
            int(duration)
        )

        if not is_available:
            flash(f'Sorry, {photographer["FullName"]} is not available for the selected period. Would u pls select a different time?', 'error')
            return redirect(url_for('main.book_session', photographer_id=photographer_id))

        booking_id = db.create_booking(
            photographer_id,
            category_id,
            descriptions,
            location,
            start_time_str,
            int(duration),
            status='pending payment'
        )

        session['pending_booking'] = {
            'booking_id': booking_id,
            'photographer_name': photographer['FullName'],
            'start_time': start_time_str,
            'duration': int(duration),
            'price': photographer['PricePerHr'] * int(duration)
        }
        
        return redirect(url_for('main.checkout'))

    return render_template('book_session.html', form=form, photographer=photographer, categories=categories)


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not is_logged_in():
        flash('Hi there, please log in first to check out', 'error')
        return redirect(url_for('main.login'))

    user = get_current_user()
    pending_booking = session.get('pending_booking', None)

    
    client_bookings = []
    if user and user['user_type'] == 'client':

        pass

    form = PaymentForm()

    if form.validate_on_submit() and pending_booking:
        booking_id = pending_booking['booking_id']

        db.update_booking_status(booking_id, 'success')

        payment_id = db.create_payment(
            user['user_id'],
            booking_id,
            pending_booking['duration'],
            pending_booking['price'],
            form.payment_method.data
        )

  
        session.pop('pending_booking', None)

        flash('Thank u. Your booking is confirmed!', 'success')
        return redirect(url_for('main.index'))

    return render_template('checkout.html',
                         form=form,
                         pending_booking=pending_booking,
                         user=user)


@bp.route('/booking/edit/<booking_id>', methods=['POST'])
def edit_booking(booking_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    descriptions = request.form.get('descriptions')
    location = request.form.get('location')
    start_time = request.form.get('start_time')
    duration = request.form.get('duration')

    db.update_booking(booking_id, descriptions, location, start_time, duration)
    flash('Booking is updated successfully', 'success')
    return redirect(url_for('main.checkout'))


@bp.route('/booking/delete/<booking_id>', methods=['POST'])
def delete_booking(booking_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    db.delete_booking(booking_id)
    flash('Booking is deleted successfully', 'success')
    return redirect(url_for('main.checkout'))


@bp.route('/vendor_management', methods=['GET', 'POST'])
def vendor_management():
    if not is_logged_in():
        flash('Please log in as a photographer to view this page', 'error')
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user['user_type'] != 'photographer':
        flash('Only photographers can view this page', 'error')
        return redirect(url_for('main.index'))

    form = ImageUploadForm()
    categories = db.get_all_categories()
    form.category_id.choices = [(c['CategoryID'], c['Name']) for c in categories]

    if form.validate_on_submit():
        
        import os
        from werkzeug.utils import secure_filename
        from flask import current_app

        if form.image_file.data:
            file = form.image_file.data
            filename = secure_filename(file.filename)

       
            upload_folder = os.path.join(current_app.root_path, 'static', 'img')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

          
            db.create_image(
                photographer_id=user['user_id'],
                category_id=form.category_id.data,
                url=filename,
                title=form.title.data,
                visibility=form.visibility.data
            )

            flash('This image has been uploaded successfully!', 'success')
            return redirect(url_for('main.vendor_management'))

    images = db.get_all_images_by_photographer(user['user_id'])

    return render_template('vendor_management.html', form=form, images=images)


@bp.route('/image/delete/<image_id>', methods=['POST'])
def delete_image(image_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user['user_type'] != 'photographer':
        flash('Only photographers can delete images', 'error')
        return redirect(url_for('main.index'))

    db.delete_image(image_id)
    flash('Image is deleted successfully', 'success')
    return redirect(url_for('main.vendor_management'))


@bp.route('/image/toggle/<image_id>', methods=['POST'])
def toggle_image_visibility(image_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user['user_type'] != 'photographer':
        flash('Only photographers can edit his images', 'error')
        return redirect(url_for('main.index'))

    image = db.get_image_by_id(image_id)
    new_visibility = 'Hidden' if image['Visibility'] == 'Published' else 'Published'
    db.update_image_visibility(image_id, new_visibility)

    flash(f'Image visibility is changed to {new_visibility}', 'success')
    return redirect(url_for('main.vendor_management'))


@bp.route('/image/publish/<image_id>', methods=['POST'])
def publish_image(image_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user['user_type'] != 'photographer':
        flash('Only photographers can edit his images', 'error')
        return redirect(url_for('main.index'))

    db.update_image_visibility(image_id, 'Published')
    flash('Hi, Your photo has been published successfully', 'success')
    return redirect(url_for('main.vendor_management'))


@bp.route('/image/hide/<image_id>', methods=['POST'])
def hide_image(image_id):
    if not is_logged_in():
        return redirect(url_for('main.login'))

    user = get_current_user()
    if user['user_type'] != 'photographer':
        flash('Only photographers can edit his images', 'error')
        return redirect(url_for('main.index'))

    db.update_image_visibility(image_id, 'Hidden')
    flash('Hi, Your photo have been hidden successfully', 'success')
    return redirect(url_for('main.vendor_management'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        user_type = form.user_type.data

        user = None
        if user_type == 'client':
            user = db.get_client_by_email(email)
            if user:
                session['user'] = {
                    'user_id': user['ClientID'],
                    'email': user['Email'],
                    'name': user['FullName'],
                    'user_type': 'client'
                }
        elif user_type == 'photographer':
            user = db.get_photographer_by_email(email)
            if user:
                session['user'] = {
                    'user_id': user['PhotographerID'],
                    'email': user['Email'],
                    'name': user['FullName'],
                    'user_type': 'photographer'
                }
        elif user_type == 'admin':
            user = db.get_admin_by_email(email)
            if user:
                session['user'] = {
                    'user_id': user['AdminID'],
                    'email': user['Email'],
                    'name': user['FullName'],
                    'user_type': 'admin'
                }

        if user:
            flash(f'Hi {user["FullName"]},  welcome back.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or user type', 'error')

    return render_template('login.html', form=form)


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    user_type = request.args.get('type', 'client')

    if user_type == 'client':
        form = ClientRegistrationForm()
        if form.validate_on_submit():
            
            existing_client = db.get_client_by_email(form.email.data)
            if existing_client:
                flash('This Email addr is already registerd', 'error')
            else:
                client_id = db.create_client(
                    form.full_name.data,
                    form.email.data,
                    form.phone.data,
                    form.address.data
                )
                flash('Registration is successful! Please log in.', 'success')
                return redirect(url_for('main.login'))
    else:
        form = PhotographerRegistrationForm()
        if form.validate_on_submit():
            
            existing_photographer = db.get_photographer_by_email(form.email.data)
            if existing_photographer:
                flash('This Email addr is already registerd', 'error')
            else:
                photographer_id = db.create_photographer(
                    form.full_name.data,
                    form.email.data,
                    form.phone.data,
                    form.specialization.data,
                    form.biography.data,
                    form.location.data,
                    form.price_per_hr.data
                )
                flash('Registration is successful! Please log in.', 'success')
                return redirect(url_for('main.login'))

    return render_template('registration.html', form=form, user_type=user_type)


@bp.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('pending_booking', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))


@bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = db.search_photographers_and_categories(query)
    else:
        results = []

    return render_template('search_results.html', results=results, query=query)


@bp.route('/admin/vendors', methods=['GET', 'POST'])
@admin_required
def admin_vendor_management():
    form = AddPhotographerForm()

    if request.method == 'POST' and form.validate_on_submit():

        existing_photographer = db.get_photographer_by_email(form.email.data)
        if existing_photographer:
            flash('This Email addr is already registerd', 'error')
        else:
   
            new_id = db.create_photographer(
                form.full_name.data,
                form.email.data,
                form.phone.data,
                form.specialization.data,
                form.biography.data,
                form.location.data,
                float(form.price_per_hr.data)
            )
            flash(f'Photographer {form.full_name.data} is added successfully', 'success')
            return redirect(url_for('main.admin_vendor_management'))


    photographers = db.get_all_photographers()

    return render_template('admin_vendor_management.html', form=form, photographers=photographers)


@bp.route('/admin/vendors/delete/<photographer_id>', methods=['POST'])
@admin_required
def admin_delete_photographer(photographer_id):
    photographer = db.get_photographer_by_id(photographer_id)
    if photographer:
        db.delete_photographer(photographer_id)
        flash(f'Photographer {photographer["FullName"]} has been deleted successfully', 'success')
    else:
        flash('This photographer is not found', 'error')
    return redirect(url_for('main.admin_vendor_management'))


@bp.route('/admin/orders')
@admin_required
def admin_order_management():

    orders = db.get_all_bookings_with_details()

    return render_template('order_management.html', orders=orders)


@bp.route('/admin/orders/delete/<booking_id>', methods=['POST'])
@admin_required
def admin_delete_order(booking_id):
    booking = db.get_booking_by_id(booking_id)
    if booking:
        db.delete_booking(booking_id)
        flash(f'This order {booking_id} has been deleted successfully', 'success')
    else:
        flash('This order is not found', 'error')
    return redirect(url_for('main.admin_order_management'))
