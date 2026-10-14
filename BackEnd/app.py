from flask import Flask, jsonify, request
from flask_cors import CORS

from azure.cosmos import CosmosClient
from dotenv import load_dotenv

import os


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# FLASK SETUP
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# COSMOS DB CONFIGURATION
# ==========================================

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")

DATABASE_NAME = os.getenv("COSMOS_DATABASE")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER")


# ==========================================
# CONNECT TO AZURE COSMOS DB
# ==========================================

client = CosmosClient(
    COSMOS_ENDPOINT,
    COSMOS_KEY
)

database = client.get_database_client(
    DATABASE_NAME
)


# ==========================================
# COSMOS DB CONTAINERS
# ==========================================

# Events container
events_container = database.get_container_client(
    CONTAINER_NAME
)

# Registrations container
registration_container = database.get_container_client(
    "Registrations"
)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return "Cloud Event Management Backend is running!"


# ==========================================
# GET EVENTS
# ==========================================

@app.route("/events", methods=["GET"])
def get_events():

    try:

        query = "SELECT * FROM c"

        events = list(
            events_container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )

        return jsonify(events), 200

    except Exception as error:

        print(
            "Error retrieving events:",
            error
        )

        return jsonify({

            "message":
                "Unable to retrieve events",

            "error":
                str(error)

        }), 500


# ==========================================
# CREATE EVENT
# ==========================================

@app.route("/events", methods=["POST"])
def create_event():

    try:

        data = request.get_json()

        # Get existing event count

        query = "SELECT VALUE COUNT(1) FROM c"

        count_result = list(
            events_container.query_items(
                query=query,
                enable_cross_partition_query=True
            )
        )

        count = count_result[0]

        # Generate event ID

        event_id = "E" + str(
            count + 1
        ).zfill(3)


        # Create event

        new_event = {

            "id":
                event_id,

            "eventId":
                event_id,

            "title":
                data["title"],

            "description":
                data["description"],

            "date":
                data["date"],

            "time":
                data["time"],

            "venue":
                data["venue"],

            "capacity":
                data["capacity"]

        }


        # Save event to Cosmos DB

        events_container.create_item(
            body=new_event
        )


        return jsonify(
            new_event
        ), 201


    except Exception as error:

        print(
            "Error creating event:",
            error
        )

        return jsonify({

            "message":
                "Unable to create event",

            "error":
                str(error)

        }), 500


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route(
    "/registrations",
    methods=["POST"]
)
def create_registration():

    try:

        data = request.get_json()


        # Create unique registration ID

        registration_id = (

            "R"
            + str(data["studentId"])
            + "_"
            + str(data["eventId"])

        )


        # Create registration

        registration = {

            "id":
                registration_id,

            "registrationId":
                registration_id,

            "eventId":
                data["eventId"],

            "studentId":
                data["studentId"],

            "studentName":
                data["studentName"],

            "studentEmail":
                data["studentEmail"],

            # Default attendance status

            "attendance":
                "Absent"

        }


        # Save registration

        registration_container.create_item(
            body=registration
        )


        return jsonify({

            "message":
                "Registration successful!",

            "registration":
                registration

        }), 201


    except Exception as error:

        print(
            "Error creating registration:",
            error
        )

        return jsonify({

            "message":
                "Unable to create registration",

            "error":
                str(error)

        }), 500


# ==========================================
# GET REGISTRATIONS FOR AN EVENT
# ==========================================

@app.route(
    "/registrations/<event_id>",
    methods=["GET"]
)
def get_registrations(event_id):

    try:

        query = """
        SELECT * FROM c
        WHERE c.eventId = @eventId
        """

        parameters = [

            {
                "name":
                    "@eventId",

                "value":
                    event_id

            }

        ]


        registrations = list(

            registration_container.query_items(

                query=query,

                parameters=parameters,

                enable_cross_partition_query=True

            )

        )


        return jsonify(
            registrations
        ), 200


    except Exception as error:

        print(
            "Error retrieving registrations:",
            error
        )

        return jsonify({

            "message":
                "Unable to retrieve registrations",

            "error":
                str(error)

        }), 500


# ==========================================
# MARK ATTENDANCE
# ==========================================

@app.route(
    "/attendance",
    methods=["POST"]
)
def mark_attendance():

    try:

        data = request.get_json()


        # Required data

        registration_id = data["registrationId"]

        status = data["status"]


        # Validate attendance status

        if status not in [
            "Present",
            "Absent"
        ]:

            return jsonify({

                "message":
                    "Status must be Present or Absent"

            }), 400


        # Find registration

        query = """
        SELECT * FROM c
        WHERE c.registrationId = @registrationId
        """

        parameters = [

            {
                "name":
                    "@registrationId",

                "value":
                    registration_id

            }

        ]


        registrations = list(

            registration_container.query_items(

                query=query,

                parameters=parameters,

                enable_cross_partition_query=True

            )

        )


        # Registration not found

        if len(registrations) == 0:

            return jsonify({

                "message":
                    "Registration not found"

            }), 404


        registration = registrations[0]


        # Update attendance

        registration["attendance"] = status


        # Save updated registration

        registration_container.upsert_item(

            body=registration

        )


        return jsonify({

            "message":
                "Attendance updated successfully",

            "registration":
                registration

        }), 200


    except Exception as error:

        print(
            "Error marking attendance:",
            error
        )

        return jsonify({

            "message":
                "Unable to mark attendance",

            "error":
                str(error)

        }), 500


# ==========================================
# GET ATTENDANCE FOR AN EVENT
# ==========================================

@app.route(
    "/attendance/<event_id>",
    methods=["GET"]
)
def get_attendance(event_id):

    try:

        query = """
        SELECT * FROM c
        WHERE c.eventId = @eventId
        """

        parameters = [

            {
                "name":
                    "@eventId",

                "value":
                    event_id

            }

        ]


        registrations = list(

            registration_container.query_items(

                query=query,

                parameters=parameters,

                enable_cross_partition_query=True

            )

        )


        # Return only relevant attendance information

        attendance_data = []


        for registration in registrations:

            attendance_data.append({

                "registrationId":
                    registration.get(
                        "registrationId"
                    ),

                "eventId":
                    registration.get(
                        "eventId"
                    ),

                "studentId":
                    registration.get(
                        "studentId"
                    ),

                "studentName":
                    registration.get(
                        "studentName"
                    ),

                "studentEmail":
                    registration.get(
                        "studentEmail"
                    ),

                "attendance":
                    registration.get(
                        "attendance",
                        "Absent"
                    )

            })


        return jsonify(
            attendance_data
        ), 200


    except Exception as error:

        print(
            "Error retrieving attendance:",
            error
        )

        return jsonify({

            "message":
                "Unable to retrieve attendance",

            "error":
                str(error)

        }), 500


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    port = int(
        os.environ.get(
            "PORT",
            os.environ.get("WEBSITES_PORT", "5000")
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )