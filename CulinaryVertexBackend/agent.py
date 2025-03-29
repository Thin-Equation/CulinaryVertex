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
from bson import ObjectId

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
        self.policies_collection = self.db["policies"]

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
    
    @fnc_ctx.ai_callable()
    async def get_menu_item_by_name(
        name: Annotated[str, llm.TypeInfo(description="Name of the menu item to find")]
    ):
        """Find a specific menu item by its name."""
        return db_helper.menu_collection.find_one({"name": name}, {"_id": 0})
    
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
    
    @fnc_ctx.ai_callable()
    async def modify_reservation(
        reservation_id: Annotated[str, llm.TypeInfo(description="ID of the reservation to modify")],
        customer_name: Annotated[Optional[str], llm.TypeInfo(description="Updated full name of the customer")] = None,
        contact_number: Annotated[Optional[str], llm.TypeInfo(description="Updated customer's phone number")] = None,
        date: Annotated[Optional[str], llm.TypeInfo(description="Updated date in YYYY-MM-DD format")] = None,
        time: Annotated[Optional[str], llm.TypeInfo(description="Updated time in HH:MM format")] = None,
        party_size: Annotated[Optional[int], llm.TypeInfo(description="Updated number of people in the party")] = None
    ):
        """Modify an existing restaurant reservation."""
        # Prepare update dict with only the fields that are provided
        update_fields = {}
        if customer_name is not None:
            update_fields["customer_name"] = customer_name
        if contact_number is not None:
            update_fields["contact_number"] = contact_number
        if date is not None:
            update_fields["date"] = date
        if time is not None:
            update_fields["time"] = time
        if party_size is not None:
            update_fields["party_size"] = party_size
        
        # Add updated_at timestamp
        update_fields["updated_at"] = datetime.now()
        
        # Update the reservation in the database
        result = db_helper.reservations_collection.update_one(
            {"_id": ObjectId(reservation_id)},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            # Get the updated reservation to return it
            updated_reservation = db_helper.reservations_collection.find_one(
                {"_id": ObjectId(reservation_id)},
                {"_id": 0}  # Exclude _id field from the result
            )
            
            return {
                "success": True,
                "message": f"Reservation updated successfully for {updated_reservation['customer_name']} on {updated_reservation['date']} at {updated_reservation['time']}.",
                "reservation": updated_reservation
            }
        else:
            return {
                "success": False,
                "message": "Reservation not found or no changes were made."
            }
    
    @fnc_ctx.ai_callable()
    async def get_reservation_by_id(
        reservation_id: Annotated[str, llm.TypeInfo(description="ID of the reservation to retrieve")]
    ):
        """Retrieve a specific reservation by its ID."""
        reservation = db_helper.reservations_collection.find_one(
            {"_id": ObjectId(reservation_id)},
            {"_id": 0}  # Exclude _id field from the result
        )
        
        if reservation:
            return reservation
        else:
            return {"message": "Reservation not found."}

    @fnc_ctx.ai_callable()
    async def search_reservations(
        customer_name: Annotated[Optional[str], llm.TypeInfo(description="Customer name to search for")] = None,
        date: Annotated[Optional[str], llm.TypeInfo(description="Date to search for in YYYY-MM-DD format")] = None,
        contact_number: Annotated[Optional[str], llm.TypeInfo(description="Contact number to search for")] = None
    ):
        """Search for reservations by customer name, date, or contact number."""
        query = {}
        if customer_name:
            query["customer_name"] = {"$regex": customer_name, "$options": "i"}  # Case-insensitive search
        if date:
            query["date"] = date
        if contact_number:
            query["contact_number"] = contact_number
        
        if not query:
            return {"message": "Please provide at least one search parameter."}
        
        reservations = list(db_helper.reservations_collection.find(query, {"_id": 1, "customer_name": 1, "date": 1, "time": 1, "party_size": 1}))
        
        # Convert ObjectId to string for JSON serialization
        for reservation in reservations:
            reservation["_id"] = str(reservation["_id"])
        
        if reservations:
            return reservations
        else:
            return {"message": "No reservations found matching the search criteria."}

    # Register policy-related functions
    @fnc_ctx.ai_callable()
    async def get_all_policies():
        """Retrieve all restaurant policies."""
        return list(db_helper.policies_collection.find({}, {"_id": 0}))

    @fnc_ctx.ai_callable()
    async def get_policy_by_type(
        type: Annotated[str, llm.TypeInfo(description="Type of policy to retrieve (e.g., restaurant_info, hours_of_operation, reservation_policy, dress_code)")] 
    ):
        """Retrieve a specific restaurant policy by its type."""
        return db_helper.policies_collection.find_one({"type": type}, {"_id": 0})

    @fnc_ctx.ai_callable()
    async def get_policy_by_id(
        policy_id: Annotated[str, llm.TypeInfo(description="ID of the specific policy to retrieve")]
    ):
        """Retrieve a specific restaurant policy by its ID."""
        return db_helper.policies_collection.find_one({"_id": ObjectId(policy_id)}, {"_id": 0})

    @fnc_ctx.ai_callable()
    async def get_special_experience_by_name(
        name: Annotated[str, llm.TypeInfo(description="Name of the special experience to retrieve")]
    ):
        """Retrieve details about a specific special experience by its name."""
        policy = db_helper.policies_collection.find_one(
            {"type": "special_experiences"}, 
            {"_id": 0}
        )
        if policy and "options" in policy:
            for option in policy["options"]:
                if option.get("name") == name:
                    return option
        return {"message": "Special experience not found."}

    @fnc_ctx.ai_callable()
    async def get_hours_for_day(
        day: Annotated[str, llm.TypeInfo(description="Day of the week (e.g., Monday, Tuesday)")]
    ):
        """Retrieve operating hours for a specific day of the week."""
        policy = db_helper.policies_collection.find_one(
            {"type": "hours_of_operation"}, 
            {"_id": 0}
        )
        if policy and "regularHours" in policy:
            for hours in policy["regularHours"]:
                if hours.get("dayOfWeek") == day:
                    return hours
        return {"message": f"Hours for {day} not found."}

    current_date = datetime.now().strftime("%Y-%m-%d")

    agent = multimodal.MultimodalAgent(
        model=google.beta.realtime.RealtimeModel(
            instructions=f"""You are Culinary Vertex, an advanced AI restaurant assistant designed to enhance the dining experience at Gourmet Bistro. 
                Your primary functions are to manage reservations, take orders, provide personalized dish recommendations, and inform guests about restaurant policies.
                Today's Date is {current_date}. You have access to the restaurant's menu through get_menu_items tool and policies through get_all_policies tool.
                
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
                
                Policy Information:
                    Be familiar with all restaurant policies stored in the policies collection.
                    Accurately inform customers about policies when asked, including reservation policies, cancellation policies, dress code, etc.
                    Make sure to reference the correct and most up-to-date policy information using the policy tools.
                    If a customer has a question about a specific policy, use get_policy_by_category or get_policy_by_name to retrieve accurate information.
                
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
        transcription=multimodal.AgentTranscriptionOptions(user_transcription=True, agent_transcription=True),
        fnc_ctx=fnc_ctx
    )
    agent.start(ctx.room)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, worker_type=WorkerType.ROOM))
