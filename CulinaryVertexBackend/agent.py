from __future__ import annotations
import logging
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, WorkerType, cli, multimodal, llm
from livekit.plugins import google
from datetime import datetime 
import certifi
import enum
from pymongo import MongoClient
from typing import List, Dict, Optional, Annotated, Any, Union, get_type_hints
from livekit.agents.llm import TypeInfo
import os

load_dotenv(dotenv_path=".env")
logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)

class MongoDBHelper:
    def __init__(self, connection_uri: str):
        self.client = MongoClient(
            connection_uri,
            tlsCAFile=certifi.where()
        )
        self.db = self.client["restaurant_db"]
        self.menu_collection = self.db["menu"]
        self.reservations_collection = self.db["reservations"]
        self.orders_collection = self.db["orders"]

    def close_connection(self):
        if self.client:
            self.client.close()

async def entrypoint(ctx: JobContext):
    logger.info("starting culinary vertex backend")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    uri = os.getenv("MONGO_DB_URL")

    db_helper = MongoDBHelper(uri)
    
    # Create function context following LiveKit pattern
    fnc_ctx = llm.FunctionContext()
    
    # Register menu-related functions
    @fnc_ctx.ai_callable()
    async def get_menu_items():
        """Retrieve all items from the restaurant menu."""
        return list(db_helper.menu_collection.find({}, {"_id": 0}))
    
    @fnc_ctx.ai_callable()
    async def get_menu_by_category(
        category: Annotated[str, llm.TypeInfo(description="Category of menu items to retrieve")]
    ):
        """Retrieve menu items filtered by category."""
        return list(db_helper.menu_collection.find({"category": category}, {"_id": 0}))
    
    # @fnc_ctx.ai_callable()
    # async def get_menu_item_by_name(
    #     name: Annotated[str, llm.TypeInfo(description="Name of the menu item to find")]
    # ):
    #     """Find a specific menu item by its name."""
    #     return db_helper.menu_collection.find_one({"name": name}, {"_id": 0})
    
    # Register reservation-related functions
    @fnc_ctx.ai_callable()
    async def create_reservation(
        customer_name: Annotated[str, llm.TypeInfo(description="Full name of the customer")],
        contact_number: Annotated[str, llm.TypeInfo(description="Customer's phone number")],
        date: Annotated[str, llm.TypeInfo(description="Date in YYYY-MM-DD format")],
        time: Annotated[str, llm.TypeInfo(description="Time in HH:MM format")],
        party_size: Annotated[int, llm.TypeInfo(description="Number of people in the party")]
    ):
        """Create a new restaurant reservation."""
        reservation = {
            "customer_name": customer_name,
            "contact_number": contact_number,
            "date": date,
            "time": time,
            "party_size": party_size,
            "status": "confirmed",
            "created_at": datetime.now()
        }
        
        result = db_helper.reservations_collection.insert_one(reservation)
        reservation_id = str(result.inserted_id)
        
        return {
            "reservation_id": reservation_id,
            "message": f"Reservation confirmed for {customer_name} on {date} at {time} for {party_size} people."
        }
    
    # @fnc_ctx.ai_callable()
    # async def get_reservations_by_date(
    #     date: Annotated[str, llm.TypeInfo(description="Date in YYYY-MM-DD format")]
    # ):
    #     """Retrieve all reservations for a specific date."""
    #     reservations = list(db_helper.reservations_collection.find({"date": date}))
    #     # Convert ObjectId to string for JSON serialization
    #     for reservation in reservations:
    #         reservation["_id"] = str(reservation["_id"])
    #     return reservations
    
    # # Register order-related functions
    # @fnc_ctx.ai_callable()
    # async def create_order(
    #     customer_name: Annotated[str, llm.TypeInfo(description="Name of the customer")],
    #     items: Annotated[List[Dict], llm.TypeInfo(description="List of items with name, price, and quantity")],
    #     table_number: Annotated[Optional[str], llm.TypeInfo(description="Table number (optional)")] = None
    # ):
    #     """Create a new food order."""
    #     # Calculate total based on items
    #     total = sum(item.get("price", 0) * item.get("quantity", 1) for item in items)
        
    #     order = {
    #         "customer_name": customer_name,
    #         "table_number": table_number,
    #         "items": items,
    #         "total": total,
    #         "status": "received",
    #         "created_at": datetime.now()
    #     }
        
    #     result = db_helper.orders_collection.insert_one(order)
    #     order_id = str(result.inserted_id)
        
    #     return {
    #         "order_id": order_id,
    #         "message": f"Order placed successfully for {customer_name}. Total: ${total:.2f}"
    #     }
    
    # @fnc_ctx.ai_callable()
    # async def get_active_orders():
    #     """Retrieve all currently active orders (not completed or cancelled)."""
    #     orders = list(db_helper.orders_collection.find(
    #         {"status": {"$nin": ["completed", "cancelled"]}}
    #     ).sort("created_at", 1))
        
    #     # Convert ObjectId to string for JSON serialization
    #     for order in orders:
    #         order["_id"] = str(order["_id"])
    #     return orders
    
    # @fnc_ctx.ai_callable()
    # async def update_order_status(
    #     order_id: Annotated[str, llm.TypeInfo(description="ID of the order to update")],
    #     status: Annotated[str, llm.TypeInfo(description="New status (preparing, ready, delivered, completed, cancelled)")]
    # ):
    #     """Update the status of an existing order."""
    #     result = db_helper.orders_collection.update_one(
    #         {"_id": ObjectId(order_id)},
    #         {"$set": {"status": status}}
    #     )
        
    #     if result.modified_count > 0:
    #         return {"success": True, "message": f"Order {order_id} status updated to {status}"}
    #     else:
    #         return {"success": False, "message": "Order not found or status unchanged"}
    
    current_date = datetime.now().strftime("%Y-%m-%d")

    agent = multimodal.MultimodalAgent(
        model=google.beta.realtime.RealtimeModel(
            instructions=f"""You are Culinary Vertex, an advanced AI restaurant assistant designed to enhance the dining experience at Gourmet Bistro. 
                            Your primary functions are to manage reservations, take orders, and provide personalized dish recommendations.
                            Today's Date is {current_date}. You have access to the restaurant's menu through get_menu_items tool. 
                            Reservation Management: 
                                Greet customers warmly and offer to assist with reservations. 
                                Ask if they would like to make a new reservation or modify an existing reservation.
                                If it is a new reservation then collect the following information: 
                                    Customer's name
                                    Contact number 
                                    Date and time for the reservation in natural language
                                    Party size 
                                Confirm availability for the requested time and date. If the desired time is unavailable, suggest alternative time slots. 
                                Once you have all the details, format them properly.
                                Provide a confirmation number upon successful reservation. 
                                If they want to modify the reservation, then ask for confirmation_number and ask the details of what they want to modify
                                Update the reservation with new details and format them properly.
                            Order Taking: 
                                Familiarize yourself with the current menu items, including specials and seasonal offerings. 
                                Ask if the customer has any dietary restrictions or allergies. 
                                Guide customers through the menu, answering any questions about ingredients or preparation methods. 
                                Accurately record the customer's order, including any modifications or special requests. 
                                Repeat the order back to the customer for confirmation. 
                            Dish Recommendations: 
                                Ask customers about their preferences (e.g., flavor profiles, cuisine types, dietary needs). 
                                Based on their responses, recommend dishes from the current menu that best match their tastes. 
                                Highlight popular items, chef's specials, and dishes that complement the customer's choices. 
                                Suggest wine pairings or beverage options that enhance the meal. 
                            General Guidelines: 
                                Maintain a friendly, professional tone throughout all interactions. 
                                Be knowledgeable about the restaurant's policies, hours of operation, and any upcoming events. 
                                Handle special requests or accommodations with care and attention to detail. 
                                If faced with a question or situation outside your capabilities, offer to connect the customer with a human staff member. 
                                Remember to always prioritize customer satisfaction and create a welcoming atmosphere that reflects the quality and character of our restaurant. 
                                Once you have all the details, format them properly and call the appropriate tool.""",
            voice="Kore",
            temperature=0.8,
            modalities=["AUDIO"]
        ),
        fnc_ctx=fnc_ctx
    )
    agent.start(ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
