from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass
class Admin:
    AdminID: str
    FullName: str
    Email: str
    PriviliageList: str


@dataclass
class Client:
    ClientID: str
    FullName: str
    Email: str
    Phone: str
    Address: str

@dataclass
class Photographer:
    PhotographerID: str
    FullName: str
    Email: str
    Phone: str
    Specialization: str
    Biography: str
    CoverImageID: Optional[str]
    Location: str
    PricePerHr: float

@dataclass
class Category:
    CategoryID: str
    Name: str
    Descriptions: str
    ImageLink: str

@dataclass
class Image:
    ImageID: str
    PhotographerID: str
    CategoryID: str
    Url: str
    Title: str
    Visibility: str

@dataclass
class Booking:
    BookingID: str
    PhotographerID: str
    CategoryID: str
    Descriptions: str
    Location: str
    StartTime: datetime
    Duration: int
    Status: str

@dataclass
class Payment:
    PaymentID: str
    ClientID: str
    BookingID: str
    Duration: int
    Price: float
    PaymentMethod: str
    PaymentDate: datetime
    PaymentStatus: str
