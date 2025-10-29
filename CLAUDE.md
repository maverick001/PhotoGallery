# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Photo Gallery is a full-stack photography studio platform connecting professional photographers with clients. Built with Flask + MySQL + Bootstrap 5, it allows photographers to showcase portfolios, clients to browse and book sessions, and administrators to manage the platform.

## Running the Application

**Start the development server:**
```bash
python run.py
```
The app runs on `http://localhost:9999` with debug mode enabled.

**Database setup:**
The database schema is defined in `photogallery/ifn582_database.sql`. Import this into MySQL before running:
```bash
mysql -u root -p < photogallery/ifn582_database.sql
```

**Database credentials are configured in `photogallery/__init__.py`:**
- User: `root`
- Password: `waderabc`
- Database: `ifn582_database` (created as `IFN582_group23` in SQL file)
- Host: `localhost`

## Technology Stack Constraints

**STRICT REQUIREMENT**: Only use these technologies:
- Frontend: HTML5, CSS3, Bootstrap 5.3.7 (no JavaScript frameworks)
- Backend: Flask, Jinja2
- Database: MySQL via Flask-MySQLdb
- Forms: Flask-WTF, WTForms
- Libraries: Only those in requirements.txt

Do not add React, Vue, jQuery, or other JS frameworks. Do not add additional Python packages without explicit approval.

## Architecture

### Application Structure
```
photogallery/
├── __init__.py          # App factory, MySQL config, error handlers
├── views.py             # Route handlers (Blueprint: 'bp')
├── models.py            # Data classes for 7 DB tables (incomplete)
├── db.py                # Database query functions (incomplete)
├── forms.py             # WTForms definitions (incomplete)
├── wrappers.py          # Decorators (admin_required implemented)
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template with navbar/footer
│   ├── index.html       # Homepage with categories
│   ├── vendor_gallery.html      # Photographer portfolios with carousels
│   ├── item_details.html        # Session details & booking form
│   ├── checkout.html            # Booking summary & payment
│   ├── vendor_management.html   # Photographer dashboard
│   ├── login.html & registration.html
│   └── 404.html & 500.html
└── static/
    ├── style.css        # Custom styles
    └── img/             # Portfolio images
```

### Database Schema (7 Tables)

**DO NOT modify the database schema.** All tables are defined in `photogallery/ifn582_database.sql`:

1. **Admins**: AdminID (PK), FullName, Email, PriviliageList
2. **Clients**: ClientID (PK), FullName, Email, Phone, Address
3. **Photographers**: PhotographerID (PK), FullName, Email, Phone, Specialization, Biography, CoverImageID (FK→Images), Location, PricePerHr
4. **Categories**: CategoryID (PK), Name, Descriptions, ImageLink
5. **Images**: ImageID (PK), PhotographerID (FK), CategoryID (FK), Url, Title, Visibility
6. **Bookings**: BookingID (PK), PhotographerID (FK), CategoryID (FK), Descriptions, Location, StartTime, Duration, Status
7. **Payments**: PaymentID (PK), ClientID (FK), BookingID (FK), Duration, Price, PaymentMethod, PaymentDate, PaymentStatus

**Key relationships:**
- Photographers → Images (one-to-many via PhotographerID)
- Categories → Images (one-to-many via CategoryID)
- Photographers have a CoverImageID pointing to their cover image
- Bookings link Photographers and Categories, track Status ('success', 'pending', 'cancelled')
- Payments link Clients to Bookings

**ID patterns (enforced by CHECK constraints):**
- AdminID: 'A01', 'A02', ... (regex: A[0-9][0-9])
- ClientID: 'C01', 'C02', ...
- PhotographerID: 'P01', 'P02', ...
- CategoryID: 'Cat01', 'Cat02', ...
- ImageID: 'IMG001', 'IMG002', ...
- BookingID: 'B01', 'B02', ...
- PaymentID: 'Pay01', 'Pay02', ...

### User Roles & Authentication

Three user types with distinct workflows:
- **Client**: Browse photographers by category, book sessions, make payments
- **Photographer**: Manage portfolio (upload images, set visibility), view bookings, update availability
- **Administrator**: Platform management (use `admin_required` decorator from `wrappers.py`)

Session structure stores authenticated user info (see `photogallery/__init__.py` line 37 imports session module - implementation TBD).

### Key Implementation Patterns

**Database queries** should go in `db.py`, imported into `views.py`. Use MySQL cursor with DictCursor for row dictionaries.

**Models** (`models.py`) are dataclasses corresponding to tables - currently empty skeletons, fill in fields as needed.

**Forms** (`forms.py`) uses Flask-WTF/WTForms. Base imports are present but no forms defined yet.

**Templates** must extend `base.html` for consistent navbar/footer. Some HTML files are not yet Jinja2 templates - convert as needed while preserving current structure.

**Availability checking**: Prevent double-booking by querying Bookings table for conflicts (check PhotographerID, StartTime, Duration).

**Image visibility**: Images have Visibility field ('Published' or 'Hidden') - only show published images in portfolios.

## Critical Requirements

1. **All dynamic content must come from MySQL database** - no hardcoded data in templates
2. **Use existing database schema** - do not add/modify tables
3. **Preserve file structure** - templates already exist, convert to Jinja2 format without creating new files
4. **Keep backend simple** - only add code when necessary for frontend functionality
5. **Follow existing code style** in `__init__.py`, `models.py`, `run.py`
6. **Ask for clarification** - don't overthink or make assumptions about requirements

## Design Guidelines

**Navbar** (consistent across all pages):
- Light blue background (#e3f2fd)
- Logo + Brand: "Studio Essence" with logo.png
- Menu: Home, Photographers, Upload, About the Session, Checkout
- Search bar (Bootstrap styled)
- Responsive collapse for mobile

**Footer**:
- Dark background
- Copyright: "2025 Studio Essence. All Rights Reserved."

**Bootstrap components used**: Cards, Carousels, Forms, Tables, Badges, Buttons, Grid system

## Common Workflows

**Browse & Book Flow**:
1. Homepage shows categories (from Categories table)
2. Click category → vendor_gallery.html shows photographers filtered by specialization
3. Each photographer has Bootstrap carousel of their images (from Images table)
4. Click "Book Now" → item_details.html with session details
5. Select date/time (check availability in Bookings table)
6. checkout.html for payment details (insert into Payments table)

**Photographer Dashboard Flow**:
1. Login as photographer
2. vendor_management.html displays personal portfolio grid
3. Upload new images (insert into Images table with PhotographerID)
4. Edit/delete existing images (update/delete in Images table)
5. Set image visibility ('Published' or 'Hidden')

**Search Functionality**:
- Search bar on all pages
- Query Photographers table by name/specialization
- Query Categories table by name
- Display results with links to portfolios
