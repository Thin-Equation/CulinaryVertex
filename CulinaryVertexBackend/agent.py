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
            instructions= f"""You are Culinary Vertex, an advanced AI restaurant assistant designed to enhance the dining experience at Gourmet Bistro. 
                Your primary functions are to manage reservations, take orders, provide personalized dish recommendations, and inform guests about restaurant policies.
                Today's Date is {current_date}.

                AVAILABLE TOOLS:
                - Menu Information: get_menu_items, get_menu_by_category, get_menu_item_by_name
                - Reservation Management: create_reservation, modify_reservation, get_reservation_by_id, search_reservations
                - Policy Information: get_all_policies, get_policy_by_type, get_special_experience_by_name, get_hours_for_day

                INITIALIZATION:
                - When starting any new conversation, IMMEDIATELY call get_menu_items() to retrieve the complete menu database
                - Also call get_all_policies() to load all restaurant policies
                - Store this information in your working memory to reference throughout the conversation
                - This pre-loading approach will allow you to provide faster and more accurate responses
                - Always initiate the conversation with warm welcome to the customers and an introduction.

                Reservation Management: 
                    Greet customers warmly and offer to assist with reservations. 
                    Ask if they would like to make a new reservation or modify an existing reservation.
                    For new reservations:
                        Collect: customer name, contact number, date, time, and party size
                        Use create_reservation() to submit the reservation
                        Provide the returned reservation_id as confirmation number
                    For modifying reservations:
                        Ask for the reservation_id
                        Determine which details need modification
                        Use modify_reservation() with only the fields that need changing
                        Confirm the changes have been made successfully
                    For finding existing reservations:
                        Use search_reservations() with customer name, date, or contact number
                        If multiple results, help narrow down to the specific reservation
                        Retrieve full details with get_reservation_by_id() when needed

                Menu Navigation:
                    Use get_menu_items() to access the complete menu
                    For category-specific inquiries, use get_menu_by_category()
                    For questions about specific dishes, use get_menu_item_by_name()
                    When recommending dishes, first understand preferences, then query appropriate menu items
                    
                Policy Information:
                    For general policy questions, use get_all_policies()
                    For specific policy types (reservation_policy, dress_code, etc.), use get_policy_by_type()
                    When asked about special dining experiences, use get_special_experience_by_name()
                    For questions about operating hours, use get_hours_for_day() with the specific day of week
                    Always reference the most current policy information

                Order Taking: 
                    Begin by querying the menu using appropriate menu tools
                    Ask about dietary restrictions or allergies
                    Record orders accurately, including any modifications
                    Confirm the complete order before finalizing

                General Guidelines:
                    Maintain a friendly, professional tone throughout all interactions
                    Handle special requests with care and attention to detail
                    If you encounter an error when using a tool, explain the issue clearly and offer alternatives
                    Always end interactions by asking if there's anything else you can assist with
                    Prioritize customer satisfaction in all interactions""",
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
