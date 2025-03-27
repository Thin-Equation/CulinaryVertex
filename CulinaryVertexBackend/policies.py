from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

client = MongoClient(os.getenv("MONGO_DB_URL"))
db = client['restaurant_db']
collection = db['policies']

# Restaurant Information
restaurant_info = {
    "type": "restaurant_info",
    "name": "Gourmet Bistro",
    "location": {
        "address": "652 Wharf Street SW",
        "city": "Washington",
        "state": "DC",
        "neighborhood": "The Wharf",
        "proximityInfo": {
            "georgetown": "15 minutes",
            "downtown": "10 minutes",
            "chinatown": "10 minutes"
        }
    },
    "contactInfo": {
        "phone": "(202) 555-1234",
        "website": "https://www.gordonramsayrestaurants.com/hells-kitchen/washington-dc/",
        "social": {
            "instagram": "@hellskitchendc",
            "facebook": "HellsKitchenDC"
        }
    },
    "accessibility": {
        "adaCompliant": True,
        "noSteps": True
    },
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Hours of Operation
hours_of_operation = {
    "type": "hours_of_operation",
    "regularHours": [
        {"dayOfWeek": "Monday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Tuesday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Wednesday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Thursday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Friday", "openTime": "11:00", "closeTime": "23:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Saturday", "openTime": "11:00", "closeTime": "23:00", "breakStart": "15:30", "breakEnd": "16:30"},
        {"dayOfWeek": "Sunday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"}
    ],
    "holidayHours": [],
    "notes": "The dining room closes daily from 3:30 PM to 4:30 PM for transition between lunch and dinner service.",
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Reservation Policy
reservation_policy = {
    "type": "reservation_policy",
    "description": "Reservations are in high demand and all available slots are listed online. The restaurant does not maintain a waitlist.",
    "details": [
        "Newly available time slots from cancellations become bookable on the website",
        "Large groups of 12 or more can make reservations by calling directly",
        "No reservation fee for large groups"
    ],
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Service Charge
service_charge = {
    "type": "service_charge",
    "description": "A 20% service charge is automatically included on all bills.",
    "breakdown": [
        {"percentage": 16, "description": "Distributed directly to service workers on top of their base wage"},
        {"percentage": 4, "description": "Contributes toward staff benefits"}
    ],
    "additionalInfo": "This fee is not considered a tip. Guests may provide additional gratuity for their server if they wish.",
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Dress Code
dress_code = {
    "type": "dress_code",
    "description": "While there is no enforced dress code, many guests choose to dress up for this fine dining experience.",
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Children Policy
children_policy = {
    "type": "children_policy",
    "description": "All ages are welcome to dine at the restaurant.",
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Menus
menus = {
    "type": "menus",
    "description": "QR code menus are available for guests.",
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Special Experiences
special_experiences = {
    "type": "special_experiences",
    "options": [
        {
            "name": "Three-course dinner experience",
            "availability": {
                "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "startTime": "17:00",
                "endTime": "21:45"
            },
            "description": "Special three-course dinner experience featuring Chef Ramsay's signature dishes."
        },
        {
            "name": "Five-course prefix menu",
            "availability": {
                "minimumGuests": 6,
                "requiresReservation": True
            },
            "description": "Exclusive five-course dining experience showcasing seasonal ingredients and Chef Ramsay's culinary expertise."
        },
        {
            "name": "Front-row kitchen seating",
            "description": "Special seating arrangement allowing guests to watch the red and blue kitchen teams in action.",
            "availability": {
                "limitedSeating": True,
                "requiresReservation": True
            }
        }
    ],
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Private Dining
private_dining = {
    "type": "private_dining",
    "options": [
        {
            "name": "Private Dining Room",
            "capacity": 30,
            "description": "Exclusive private dining room for special events and gatherings."
        },
        {
            "name": "Semi-private Table",
            "location": "Second Floor",
            "description": "Semi-private dining experience on the second floor with partial privacy."
        },
        {
            "name": "Balcony Patio",
            "description": "Outdoor dining space with views of the Potomac River.",
            "features": ["River View", "Outdoor Seating"],
            "weatherDependent": True
        }
    ],
    "buyoutOptions": [
        {"area": "Bar Lounge", "capacity": None},
        {"area": "Second Floor", "capacity": None},
        {"area": "Entire Restaurant", "capacity": 450}
    ],
    "description": "Various options for private events and gatherings, including full restaurant buyouts.",
    "customizable": True,
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Insert all documents
documents = [
    restaurant_info,
    hours_of_operation,
    reservation_policy,
    service_charge,
    dress_code,
    children_policy,
    menus,
    special_experiences,
    private_dining
]

for doc in documents:
    collection.insert_one(doc)
    print(f"Inserted {doc['type']} document")

print("All documents inserted successfully!")
