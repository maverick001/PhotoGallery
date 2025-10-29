DROP DATABASE IF EXISTS gallery_database;

create database gallery_database;

use gallery_database;

/*----------------------------------------------------Admins-------------------------------------------------------------*/
create table Admins (
	AdminID char(3) not null primary key
        Check (AdminID Regexp 'A[0-9][0-9]'),
    FullName text,
    Email varchar(50),
    PriviliageList char(2) 
);
insert into admins  
values
	('A01', 'admin1', 'admin1@platform.com', 'P1'),
    ('A02', 'admin2', 'admin2@platform.com', 'P1'),
    ('A03', 'admin3', 'admin3@platform.com', 'P2'),
    ('A04', 'admin4', 'admin4@platform.com', 'P2'),
    ('A05', 'admin5', 'admin5@platform.com', 'P2');
    
/*----------------------------------------------------clients-------------------------------------------------------------*/
create table Clients (
	ClientID char(3) not null primary key
        Check (ClientID Regexp 'C[0-9][0-9]'),
    FullName text,
    Email varchar(50),
    Phone char(10),
    Address text
);
insert into clients  
values
	('C01', 'Daniel Gomez', 'Daniel.gomez@hotmail.com', '0481993187', '25 Walsh Street, Milton, 4064, QLD'),
    ('C02', 'Paulina Gamboa', 'Paulina.gamboa@hotmail.com', '0426776501', '66 High Street, Toowong, 4066, QLD'),
    ('C03', 'Suhani Mehta', 'Suhani.mehta@gmail.com', '0412857096', '82 Alfred Street, Fortitude Vallet, 4006, QLD'),
    ('C04', 'Daniela Zapata', 'Dani.zapata@gmail.com', '0403112214', '300 Spencer Street, Melbourne City, 3000, VIC'),
    ('C05', 'Nicoll Marin', 'Nicoll.marin@hotmail.com', '0414028956', '509 Pitt Street, Haymarket, 2000, NSW'),
    ('C06', 'Kevin Bai', 'k.bai@connect.qut.edu.au', '0400888888', 'F-101, GP Campus, QUT, 4000, QLN');

/*----------------------------------------------------photographers-------------------------------------------------------------*/
create table Photographers (
	PhotographerID char(3) not null primary key
        Check (PhotographerID Regexp 'P[0-9][0-9]'),
    FullName text,
    Email varchar(50),
    Phone char(10),
    Specialization text,
    Biography text,
    CoverImageID char(6) references images(ImageID),
    Location text,
    PricePerHr float
);
insert into photographers  
values
('P01','Joe Smith','Joe.smith@studio.com','0413730419','Weddings & Lifestyle','Award-winning wedding photographer', 'IMG001', 'Brisbane',150.0),
('P02','Jack Russel','Jack.russell@studio.com','0404333850','Corporate & Events','Helping brands look professional', 'IMG003', 'Brisbane',125.0),
('P03','Stephanie Vargas','Stephanie.vargas@studio.com','0405909639','Portraits','Specialist in creative portraits', 'IMG004', 'Sydney',200.0),
('P04','Carl Wilson','Carl.wilson@studio.com','0420587174','Fashion','Focused on modern fashion shoots', 'IMG005', 'Perth',187.5),
('P05','Nick Bryant','Nick.bryant@studio.com','0411160572','Products','Product photographer for eCommerce','IMG006','Melbourne',150.0);

/*----------------------------------------------------categories-------------------------------------------------------------*/
create table Categories (
	CategoryID char(5) not null primary key
        Check (CategoryID Regexp 'Cat[0-9][0-9]'),
    Name text,
    Descriptions text,
    ImageLink text 
);
insert into categories  
values
('Cat01',"Weddings","Wedding ceremonies and related events","/categories/wedding.jpg"),
('Cat02',"Corporate & events","Professional headshots and photography for businesses and events","/categories/corporate.jpg"),
('Cat03',"Portraits","Individual, family, or group portraits in studio or outdoor settings.","/categories/portrait.jpg"),
('Cat04',"Fashion","Photography for fashion brands, modelling, and editorial shoots.","/categories/fashion.jpg"),
('Cat05',"Products","Commercial product shoots","/categories/products.jpg");

/*----------------------------------------------------images-------------------------------------------------------------*/
create table Images (
	ImageID char(6) not null primary key
        Check (ImageID Regexp 'IMG[0-9][0-9][0-9]'),
    PhotographerID char(3) references photographers(PhotographerID),
    CategoryID char(5) references categories (CategoryID),
    Url varchar(50),
    Title text,
    Visibility varchar(9)
 );
insert into images  
values
('IMG001', 'P01', 'Cat01', "wedding1.png", "City Wedding", "Published"),
('IMG002', 'P01', 'Cat01', "wedding2.png", "Beach Vows", "Published"),
('IMG003', 'P02', 'Cat02', "corporate2.png", "CEO Portrait", "Published"),
('IMG004', 'P03', 'Cat04', "model.png", "Fashion Editorial", "Published"),
('IMG005', 'P04', 'Cat03', "family1.png", "Gethering", "Published"),
('IMG006', 'P05', 'Cat05', "product.png", "Soft Drinks", "Published"),
('IMG007', 'P05', 'Cat05', "product2.png", "Creams", "Hidden"),
('IMG008', 'P02', 'Cat02', "corporate.png", "Conference Audience", "Published"),
('IMG009', 'P04', 'Cat03', "family2.png", "Newborn", "Published");

/*----------------------------------------------------bookings-------------------------------------------------------------*/
create table Bookings (
	BookingID char(3) not null primary key
        Check (BookingID Regexp 'B[0-9][0-9]'),
    PhotographerID char(3) references photographers(PhotographerID),
    CategoryID char(5) references categories(CategoryID),
	Descriptions text,
    Location text,
    StartTime Datetime,
    Duration int,
	Status text
);
insert into bookings  
values
('B01','P01','Cat01','A Wedding ceremony','Brisbane City',"2025-09-18 12:00",8,'success'),
('B02','P02','Cat02','Professional headshots photography for 50 employees of Company ABC','South Brisbane',"2025-10-22 09:00",4,'success'),
('B03','P03','Cat03','A famaliy event photography in outdoor settings', 'Sydney CBD',"2025-10-20 13:00",2,'success'),
('B04','P04','Cat04','Photography for fashion brand CottonOn, modelling, and editorial shoots','Perth',"2025-11-11 08:00",8,'success'),
('B05','P05','Cat05',"Commercial product shoots for the new Macbook Pro",'Melbourne',"2025-11-15 9:00",2,'success'),
('B06','P05','Cat05',"Commercial product shoots for the new Dell laptop", "Melbourne","2025-11-16 9:00",2,'cancelled'),
('B07','P05','Cat05',"Commercial product shoots for the new Lenovo laptop", "Melbourne","2025-11-17 9:00",2,'pending');

/*----------------------------------------------------payments-------------------------------------------------------------*/
create table Payments (
	PaymentID char(5) not null primary key
        Check (PaymentID Regexp 'Pay[0-9][0-9]'),
    ClientID char(3) references clients(ClientID),
    BookingID char(3) references bookings(BookingID),
    Duration int references bookings(Duration),
    Price float,
    PaymentMethod varchar(20),
    PaymentDate DateTime,
	PaymentStatus varchar(10)
);
insert into payments
values
('Pay01','C01','B01',8,1200.0,'Visa','2025-09-1 10:30','Successful'),
('Pay02','C02','B02',4,500.0,'MasterCard','2025-10-1 10:30','Successful'),
('Pay03','C03','B03',2,400.0,'Paypal','2025-10-1 10:30','Successful'),
('Pay04','C04','B04',8,1500.0,'Afterpay','2025-11-1 10:30','Successful'),
('Pay05','C05','B05',2,300.0,'ZIP','2025-11-1 10:30','Successful'),
('Pay06','C05','B05',2,300.0,'ZIP','2025-11-1 10:30','Failed'),
('Pay07','C04','B06',2,300.0,'Visa','2025-11-10 14:30','Failed'),
('Pay08','C03','B07',2,300.0,'MasterCard','2025-11-12 10:15','Pending');
