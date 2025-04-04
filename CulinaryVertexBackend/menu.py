from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

class MongoDBHelper:
    def __init__(self, connection_uri: str):
        """Initialize MongoDB connection."""
        self.client = MongoClient(connection_uri, tlsCAFile=certifi.where())
        self.db = self.client["restaurant_db"]
        self.menu_collection = self.db["menu"]

    def insert_menu_items(self, items):
        """Insert multiple menu items into the 'menu' collection."""
        try:
            cleaned_items = self.clean_menu_items(items)
            result = self.menu_collection.insert_many(cleaned_items)
            print(f"Inserted {len(result.inserted_ids)} menu items successfully.")
            return result.inserted_ids
        except Exception as e:
            print(f"Error inserting menu items: {e}")
            return []

    def clean_menu_items(self, items):
        """Ensure price keys are strings for dictionary-based prices."""
        for item in items:
            if isinstance(item.get("price"), dict):
                item["price"] = {str(k): v for k, v in item["price"].items()}
        return items

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
        print("MongoDB connection closed.")

# Menu items data
menu_items = [
    {
        "category": "Dessert",
        "menu_type": ["Lunch","Dinner"],
        "name": "Sticky Toffee Pudding",
        "description": "english toffee sauce, ice cream",
        "price": 18.00,
        "dietary": ["Vegetarian"]
    },
    {
        "category": "Dessert",
        "menu_type": ["Lunch","Dinner"],
        "name": "Chocolate Orange Trifle",
        "description": "citrus-soaked chocolate sponge, orange gelée, chocolate mousse, chantilly cream, candied hazelnuts",
        "price": 17.00,
        "dietary": ["Vegetarian"]
    },
    {
        "category": "Dessert",
        "menu_type": ["Lunch","Dinner"],
        "name": "Lemon Blueberry Cheesecake",
        "description": "graham cracker crust, lemon curd, blueberry compote",
        "price": 15.00,
        "dietary": ["Vegetarian"]
    },
    {
        "category": "Dessert",
        "menu_type": ["Lunch","Dinner"],
        "name": "Pineapple Carpaccio",
        "description": "coconut sorbet, passion fruit, coconut flakes, lime",
        "price": 16.00,
        "dietary": ["DF", "GF", "Vegan"]
    },
    {
        "category": "Coffee",
        "menu_type": "Drinks",
        "name": "Drip Coffee by La Colombe",
        "price": 4.00
    },
    {
        "category": "Coffee",
        "menu_type": "Drinks",
        "name": "Espresso Coffee by La Colombe",
        "price": 4.00
    },
    {
        "category": "Coffee",
        "menu_type": "Drinks",
        "name": "Cappuccino & Latte Coffee by La Colombe",
        "price": 5.00
    },
    {
        "category": "Digestif",
        "menu_type": "Drinks",
        "name": "Nonino Quintessencia Amaro",
        "price": 15.00
    },
    {
        "category": "Digestif",
        "menu_type": "Drinks",
        "name": "Montenegro Amaro",
        "price": 14.00
    },
    {
        "category": "Digestif",
        "menu_type": "Drinks",
        "name": "Fernet Branca Amaro",
        "price": 14.00
    },
    {
        "category": "Digestif",
        "menu_type": "Drinks",
        "name": "Cynar Amaro",
        "price": 16.00
    },
    {
        "category": "Cognac",
        "menu_type": "Drinks",
        "name": "Remy Martin, Louis XIII",
        "description": "2 oz",
        "price": 500.00
    },
    {
        "category": "Cognac",
        "menu_type": "Drinks",
        "name": "Hennessy XO",
        "price": 85.00
    },
    {
        "category": "Cognac",
        "menu_type": "Drinks",
        "name": "Hennessy Paradis",
        "price": 300.00
    },
    {
        "category": "Grappa",
        "menu_type": "Drinks",
        "name": "Jacopo Poli, Moscato",
        "price": 35.00
    },
    {
        "category": "Grappa",
        "menu_type": "Drinks",
        "name": "Jacopo Poli, Torcolato",
        "price": 35.00
    },
    {
        "category": "Grappa",
        "menu_type": "Drinks",
        "name": "Jacopo Poli, Vespaiolo",
        "price": 35.00
    },
    {
        "category": "Fortified Wine",
        "menu_type": "Drinks",
        "name": "Dow's 10 Year Tawny",
        "price": 18.00
    },
    {
        "category": "Fortified Wine",
        "menu_type": "Drinks",
        "name": "Gould Campbell Vintage 1997",
        "price": 35.00
    },
    {
        "category": "Sweet Wine",
        "menu_type": "Drinks",
        "name": "Royal Tokaji 5 Puttonyos Tokaji Aszu",
        "price": 21.00
    },
    {
        "category": "Sweet Wine",
        "menu_type": "Drinks",
        "name": "Anselmi Recioto 'I Capitelli'",
        "price": 23.00
    },
    {
        "category": "Sparkling",
        "menu_type": "Drinks",
        "name": "Montelvini Prosecco",
        "description": "asolo docg, italy nv",
        "price": 15.00
    },
    {
        "category": "Sparkling",
        "menu_type": "Drinks",
        "name": "Albrecht Crémant d'Alsace",
        "description": "brut rosé, alsace, france nv",
        "price": 15.00
    },
    {
        "category": "Sparkling",
        "menu_type": "Drinks",
        "name": "Louis Massing Blanc de Blanc",
        "description": "grand cru champagne, france nv",
        "price": 33.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Sauvignon Blanc, Lauvertat",
        "description": "\"moulin des vrillères\" sancerre, loire valley, france 2023",
        "price": 20.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Sauvignon Blanc, Flannery Hill",
        "description": "marlborough, new zealand 2021",
        "price": 15.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Pinot Grigio, Scarpetta",
        "description": "friuli, italy 2022",
        "price": 13.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Riesling, Gunderloch",
        "description": "\"jean-baptiste\" kabinett, rheinhessen, germany 2022",
        "price": 15.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Chardonnay, Domaine Brigitte Cerveau",
        "description": "chablis, burgundy, france 2022",
        "price": 23.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Chardonnay, Timbre Winery",
        "description": "santa maria valley, california 2018",
        "price": 20.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Viognier, Michael Shaps Wineworks",
        "description": "charlottesville, va 2023",
        "price": 19.00
    },
    {
        "category": "White/Rosé",
        "menu_type": "Drinks",
        "name": "Grenache, Peyrassol",
        "description": "\"la croix des templiers\", méditerranée igp, france 2023",
        "price": 14.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Pinot Noir, La Follette",
        "description": "\"los primeros\", sonoma, california 2021",
        "price": 18.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Pinot Noir, G&B Rion",
        "description": "\"la croix blanche\", burgundy, france 2021",
        "price": 24.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Sangiovese, Rodano",
        "description": "chianti classico tuscany, italy 2020",
        "price": 15.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Saperavi, KGM Kindzmarauli",
        "description": "semi-sweet, republic of georgia 2022",
        "price": 16.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Tempranillo, C.V.N.E.",
        "description": "\"cune\", reserve, rioja, spain 2018",
        "price": 19.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Merlot, Trig Point",
        "description": "alexander valley, california 2022",
        "price": 17.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Malbec, Cuveliar Los Andes",
        "description": "mendoza, argentina 2019",
        "price": 17.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Cabernet Sauvignon, L'Esprit de Chevalier",
        "description": "pessac-leognac, bordeaux, france 2018",
        "price": 28.00
    },
    {
        "category": "Red Wine",
        "menu_type": "Drinks",
        "name": "Cabernet Sauvignon, Daou",
        "description": "paso robles, california 2022",
        "price": 18.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Fujiwhara Effect",
        "description": "blackstrap rum, lime, fresh pineapple, house made ginger beer",
        "price": 19.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Poire You Always Hating",
        "description": "tequila blanco, lime, ménage au poire, fino, candied walnut",
        "price": 20.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "A Diving Bell",
        "description": "london dry gin, yuzu, mezcal, pineapple gomme, cayenne",
        "price": 21.00
    },
    {
        "category": "Lager",
        "menu_type": "Drinks",
        "name": "Bud Light",
        "description": "st. louis, mo",
        "price": 7.00
    },
    {
        "category": "Lager",
        "menu_type": "Drinks",
        "name": "Stella Artois",
        "description": "belgium",
        "price": 9.00
    },
    {
        "category": "Lager",
        "menu_type": "Drinks",
        "name": "Estrella Jalisco",
        "description": "mexico",
        "price": 8.00
    },
    {
        "category": "Lager",
        "menu_type": "Drinks",
        "name": "Ayinger \"Celebrator\"",
        "description": "germany",
        "price": 10.00
    },
    {
        "category": "Cider",
        "menu_type": "Drinks",
        "name": "Bold Rock \"IPA\"",
        "description": "charlottesville, va",
        "price": 8.00
    },
    {
        "category": "Ale",
        "menu_type": "Drinks",
        "name": "Port City \"Optimal Wit\"",
        "description": "witbier, alexandria, va",
        "price": 7.00
    },
    {
        "category": "Ale",
        "menu_type": "Drinks",
        "name": "Westmalle",
        "description": "trappist tripel, belgium",
        "price": 14.00
    },
    {
        "category": "Ale",
        "menu_type": "Drinks",
        "name": "Bear Republic \"Racer 5\"",
        "description": "ipa, cloverdale, ca",
        "price": 8.00
    },
    {
        "category": "Ale",
        "menu_type": "Drinks",
        "name": "Solace \"Little Bit Cloudy\"",
        "description": "new england ipa, chantilly, va",
        "price": 8.00
    },
    {
        "category": "Mocktails",
        "menu_type": "Drinks",
        "name": "Lychee Cooler",
        "description": "lychee, grapefruit, elderflower, lime juice",
        "price": 11.00
    },
    {
        "category": "Mocktails",
        "menu_type": "Drinks",
        "name": "Hibiscus Sour",
        "description": "hibiscus tea, lemon, simple syrup",
        "price": 10.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Obligatory Vodka Drink",
        "description": "vodka, fresh grapefruit, peychauds, pamplemousse cordial, pink peppercorn",
        "price": 18.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Red Eye Old Fashioned",
        "description": "bourbon, demerara gomme, hints of tobacco leaf & roasted coffee",
        "price": 22.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Espresso Martini",
        "description": "tequila reposado, espresso, kahlúa, vanilla",
        "price": 23.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Eighteen Stars",
        "description": "tequila reposado, cointreau, yellow pepper, passion fruit, lime",
        "price": 21.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Smoke On The Water",
        "description": "rye, aperol, averna amaro, sweet vermouth, smoked with cherry wood",
        "price": 24.00
    },
    {
        "category": "Cocktails",
        "menu_type": "Drinks",
        "name": "Notes From Gordon",
        "description": "dry gin, green tea, lemongrass, peach, lemon, message from gordon",
        "price": 19.00
    }
]

if __name__ == "__main__":
    MONGO_URI = os.getenv("MONGO_DB_URL")
    mongo_helper = MongoDBHelper(MONGO_URI)
    
    inserted_ids = mongo_helper.insert_menu_items(menu_items)

    # Close connection when done
    mongo_helper.close_connection()
