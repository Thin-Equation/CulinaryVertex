from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")
# Connect to MongoDB (adjust connection string as needed)
URI = os.getenv("MONGO_DB_URL")
client = MongoClient(URI)

# Create or access the database
db = client['restaurant_db']

# Create a single comprehensive document containing ALL restaurant information
restaurant_policies = {
    "restaurantInfo": {
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
            "phone": "(202) 555-1234",  # Example phone number
            "website": "https://www.gordonramsayrestaurants.com/hells-kitchen/washington-dc/",
            "social": {
                "instagram": "@hellskitchendc",
                "facebook": "HellsKitchenDC"
            }
        },
        "accessibility": {
            "adaCompliant": True,
            "noSteps": True
        }
    },
    
    "hoursOfOperation": {
        "regularHours": [
            {"dayOfWeek": "Monday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Tuesday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Wednesday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Thursday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Friday", "openTime": "11:00", "closeTime": "23:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Saturday", "openTime": "11:00", "closeTime": "23:00", "breakStart": "15:30", "breakEnd": "16:30"},
            {"dayOfWeek": "Sunday", "openTime": "11:00", "closeTime": "22:00", "breakStart": "15:30", "breakEnd": "16:30"}
        ],
        "holidayHours": [],  # Can be populated with special holiday hours
        "notes": "The dining room closes daily from 3:30 PM to 4:30 PM for transition between lunch and dinner service."
    },
    
    "reservation": {
        "description": "Reservations are in high demand and all available slots are listed online. The restaurant does not maintain a waitlist.",
        "details": [
            "Newly available time slots from cancellations become bookable on the website",
            "Large groups of 12 or more can make reservations by calling directly",
            "No reservation fee for large groups"
        ]
    },
    
    "serviceCharge": {
        "description": "A 20% service charge is automatically included on all bills.",
        "breakdown": [
            {"percentage": 16, "description": "Distributed directly to service workers on top of their base wage"},
            {"percentage": 4, "description": "Contributes toward staff benefits"}
        ],
        "additionalInfo": "This fee is not considered a tip. Guests may provide additional gratuity for their server if they wish."
    },
    
    "dressCode": {
        "description": "While there is no enforced dress code, many guests choose to dress up for this fine dining experience."
    },
    
    "children": {
        "description": "All ages are welcome to dine at the restaurant."
    },
    
    "menus": {
        "description": "QR code menus are available for guests."
    },
    
    "specialExperiences": {
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
        ]
    },
    
    "privateDining": {
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
        "customizable": True
    },
    
    "metadata": {
        "lastUpdated": datetime.now(),
        "version": 1.0,
        "updatedBy": "Admin"
    }
}

# Insert the single comprehensive document
result = db.policies.insert_one(restaurant_policies)

print(f"Database populated successfully! Document ID: {result.inserted_id}")