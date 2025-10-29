from photogallery.models import Admin, Client, Photographer, Category, Image, Booking, Payment
from datetime import datetime
from . import mysql



def get_all_categories():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    cursor.close()
    return categories
    

def get_category_by_id(category_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Categories WHERE CategoryID = %s", (category_id,))
    category = cursor.fetchone()
    cursor.close()
    return category


def get_all_photographers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Photographers")
    photographers = cursor.fetchall()
    cursor.close()
    return photographers

def get_photographer_by_id(photographer_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Photographers WHERE PhotographerID = %s", (photographer_id,))
    photographer = cursor.fetchone()
    cursor.close()
    return photographer

def get_photographer_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Photographers WHERE Email = %s", (email,))
    photographer = cursor.fetchone()
    cursor.close()
    return photographer

def create_photographer(full_name, email, phone, specialization, biography, location, price_per_hr):
    cursor = mysql.connection.cursor()
 
    cursor.execute("SELECT PhotographerID FROM Photographers ORDER BY PhotographerID DESC LIMIT 1")
    last_photographer = cursor.fetchone()
    if last_photographer:
        last_num = int(last_photographer['PhotographerID'][1:])
        new_id = f"P{str(last_num + 1).zfill(2)}"
    else:
        new_id = "P01"

    cursor.execute(
        "INSERT INTO Photographers (PhotographerID, FullName, Email, Phone, Specialization, Biography, Location, PricePerHr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (new_id, full_name, email, phone, specialization, biography, location, price_per_hr)
    )
    mysql.connection.commit()
    cursor.close()
    return new_id


def delete_photographer(photographer_id):
    cursor = mysql.connection.cursor()
  
    cursor.execute("DELETE FROM Images WHERE PhotographerID = %s", (photographer_id,))

    cursor.execute("DELETE FROM Photographers WHERE PhotographerID = %s", (photographer_id,))
    mysql.connection.commit()
    cursor.close()


def get_images_by_photographer(photographer_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Images WHERE PhotographerID = %s AND Visibility = 'Published'", (photographer_id,))
    images = cursor.fetchall()
    cursor.close()
    return images


def get_all_images_by_photographer(photographer_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Images WHERE PhotographerID = %s", (photographer_id,))
    images = cursor.fetchall()
    cursor.close()
    return images

def get_image_by_id(image_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Images WHERE ImageID = %s", (image_id,))
    image = cursor.fetchone()
    cursor.close()
    return image

def create_image(photographer_id, category_id, url, title, visibility):
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT ImageID FROM Images ORDER BY ImageID DESC LIMIT 1")
    last_image = cursor.fetchone()
    if last_image:
        last_num = int(last_image['ImageID'][3:])
        new_id = f"IMG{str(last_num + 1).zfill(3)}"
    else:
        new_id = "IMG001"

    cursor.execute(
        "INSERT INTO Images (ImageID, PhotographerID, CategoryID, Url, Title, Visibility) VALUES (%s, %s, %s, %s, %s, %s)",
        (new_id, photographer_id, category_id, url, title, visibility)
    )
    mysql.connection.commit()
    cursor.close()
    return new_id

def update_image_visibility(image_id, visibility):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Images SET Visibility = %s WHERE ImageID = %s", (visibility, image_id))
    mysql.connection.commit()
    cursor.close()

def delete_image(image_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Images WHERE ImageID = %s", (image_id,))
    mysql.connection.commit()
    cursor.close()



def get_bookings_by_photographer(photographer_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Bookings WHERE PhotographerID = %s", (photographer_id,))
    bookings = cursor.fetchall()
    cursor.close()
    return bookings

def get_all_bookings_with_details():
    cursor = mysql.connection.cursor()
    query = """
        SELECT
            bookings.BookingID,
            bookings.PhotographerID,
            photographers.FullName as PhotographerName,
            bookings.CategoryID,
             categories.Name as CategoryName,
            bookings.StartTime,
            bookings.Duration,
            bookings.Status,
            payments.PaymentID,
            payments.ClientID,
              clients.FullName as ClientName,
            payments.Price,
            payments.PaymentMethod,
            payments.PaymentStatus
        FROM bookings
        LEFT JOIN photographers ON bookings.PhotographerID = photographers.PhotographerID
        LEFT JOIN categories ON bookings.CategoryID = categories.CategoryID
        LEFT JOIN payments ON bookings.BookingID = payments.BookingID
        LEFT JOIN clients ON payments.ClientID = clients.ClientID
        ORDER BY bookings.BookingID
    """
    cursor.execute(query)
    bookings = cursor.fetchall()
    cursor.close()
    return bookings

def get_booking_by_id(booking_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Bookings WHERE BookingID = %s", (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    return booking

def create_booking(photographer_id, category_id, descriptions, location, start_time, duration, status='pending'):
    cursor = mysql.connection.cursor()
    
    cursor.execute("SELECT BookingID FROM Bookings ORDER BY BookingID DESC LIMIT 1")
    last_booking = cursor.fetchone()
    if last_booking:
        last_num = int(last_booking['BookingID'][1:])
        new_id = f"B{str(last_num + 1).zfill(2)}"
    else:
        new_id = "B01"

    cursor.execute(
        "INSERT INTO Bookings (BookingID, PhotographerID, CategoryID, Descriptions, Location, StartTime, Duration, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (new_id, photographer_id, category_id, descriptions, location, start_time, duration, status)
    )
    mysql.connection.commit()
    cursor.close()
    return new_id

def update_booking(booking_id, descriptions, location, start_time, duration):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE Bookings SET Descriptions = %s, Location = %s, StartTime = %s, Duration = %s WHERE BookingID = %s",
        (descriptions, location, start_time, duration, booking_id)
    )
    mysql.connection.commit()
    cursor.close()

def delete_booking(booking_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Bookings WHERE BookingID = %s", (booking_id,))
    mysql.connection.commit()
    cursor.close()

def update_booking_status(booking_id, status):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Bookings SET Status = %s WHERE BookingID = %s", (status, booking_id))
    mysql.connection.commit()
    cursor.close()


"""
This is our app's unique feature for booking management. It checks if a photographer is available rifht after a client selects time slot on the booking page.
  After querying the photographer's existing booking records, MySQL returns True if he's available, and False if not available.
"""
def check_photographer_availability(photographer_id, start_time, duration):

    cursor = mysql.connection.cursor()


    query = """
        SELECT
            CASE WHEN COUNT(*) > 0 THEN 'Not available' ELSE 'Available' END AS availability
        FROM Bookings
        WHERE PhotographerID = %s
          AND StartTime < DATE_ADD(%s, INTERVAL %s HOUR)
          AND DATE_ADD(StartTime, INTERVAL Duration HOUR) > %s
    """

    cursor.execute(query, (photographer_id, start_time, duration, start_time))
    result = cursor.fetchone()
    cursor.close()

    if result and result['availability'] == 'Available':
        return True
    return False


def get_client_by_id(client_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Clients WHERE ClientID = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()
    return client

def get_client_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Clients WHERE Email = %s", (email,))
    client = cursor.fetchone()
    cursor.close()
    return client

def create_client(full_name, email, phone, address):
    cursor = mysql.connection.cursor()
  
    cursor.execute("SELECT ClientID FROM Clients ORDER BY ClientID DESC LIMIT 1")
    last_client = cursor.fetchone()
    if last_client:
        last_num = int(last_client['ClientID'][1:])
        new_id = f"C{str(last_num + 1).zfill(2)}"
    else:
        new_id = "C01"

    cursor.execute(
        "INSERT INTO Clients (ClientID, FullName, Email, Phone, Address) VALUES (%s, %s, %s, %s, %s)",
        (new_id, full_name, email, phone, address)
    )
    mysql.connection.commit()
    cursor.close()
    return new_id


def get_admin_by_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Admins WHERE Email = %s", (email,))
    admin = cursor.fetchone()
    cursor.close()
    return admin

def get_payments_by_client(client_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Payments WHERE ClientID = %s", (client_id,))
    payments = cursor.fetchall()
    cursor.close()
    return payments

def get_payment_by_booking(booking_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Payments WHERE BookingID = %s", (booking_id,))
    payment = cursor.fetchone()
    cursor.close()
    return payment

def create_payment(client_id, booking_id, duration, price, payment_method, payment_status='Successful'):
    cursor = mysql.connection.cursor()
  
    cursor.execute("SELECT PaymentID FROM Payments ORDER BY PaymentID DESC LIMIT 1")
    last_payment = cursor.fetchone()
    if last_payment:
        last_num = int(last_payment['PaymentID'][3:])
        new_id = f"Pay{str(last_num + 1).zfill(2)}"
    else:
        new_id = "Pay01"

    payment_date = datetime.now()
    cursor.execute(
        "INSERT INTO Payments (PaymentID, ClientID, BookingID, Duration, Price, PaymentMethod, PaymentDate, PaymentStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (new_id, client_id, booking_id, duration, price, payment_method, payment_date, payment_status)
    )
    mysql.connection.commit()
    cursor.close()
    return new_id


def search_photographers_and_categories(query):
    cursor = mysql.connection.cursor()
    search_term = f"%{query}%"
    cursor.execute(
        "SELECT 'photographer' as type, PhotographerID as id, FullName as name, Specialization as description FROM Photographers WHERE FullName LIKE %s OR Specialization LIKE %s "
        "UNION "
        "SELECT 'category' as type, CategoryID as id, Name as name, Descriptions as description FROM Categories WHERE Name LIKE %s OR Descriptions LIKE %s",
        (search_term, search_term, search_term, search_term)
    )
    results = cursor.fetchall()
    cursor.close()
    return results
