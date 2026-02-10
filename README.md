🚁 Skylark Drone Operations AI Agent

An AI-powered operational assistant for managing drone fleets and pilot assignments across multiple projects using a conversational interface and Google Sheets as the backend.

📌 Problem Overview

Skylark Drones operates multiple drones and pilots simultaneously across different client missions.
Manual coordination using spreadsheets and messages leads to:

Frequent context switching

Scheduling conflicts

Inefficient pilot–drone assignment

Delays during urgent missions

This project introduces an AI Agent that assists a drone operations coordinator by automating:

Pilot availability tracking

Drone inventory management

Conflict-free urgent reassignments

Natural language queries for operations

✨ Key Features Implemented
👨‍✈️ Pilot Roster Management

View all pilots and their status (Available / Assigned / On Leave)

View available pilots across all locations

Mark a pilot as Available (syncs back to Google Sheets)

Filter pilots by location via conversational queries

🚁 Drone Fleet Management

View all drones and their operational status

View available drones across all locations

Mark a drone as Available (syncs back to Google Sheets)

Filter drones by location via conversational queries

💬 Conversational AI Agent

Users can interact using natural language, for example:

I need a pilot in Mumbai

Find drones in Bangalore

Urgent mission

The agent:

Understands intent and location

Responds with friendly messages

Displays relevant filtered tables

Clears previous messages automatically (single-turn interaction)

🚨 Urgent Reassignment

Automatically assigns:

First available pilot

First available drone in the same location

Updates both pilot and drone status to Assigned

Syncs assignment (Urgent-Mission) back to Google Sheets

Prevents assigning unavailable pilots or drones

🔗 Google Sheets Integration (2-Way Sync)

Read:

Pilot Roster sheet

Drone Fleet sheet

Write:

Pilot status updates

Drone status updates

Uses service account authentication

Read operations are cached to avoid API quota limits

Google Sheets acts as the single source of truth for all operations.

🧠 Design Decisions

Conversational Agent is isolated from the main dashboard
(Chat responses do not affect global tables)

Single-turn conversation to avoid confusion

Dashboard always shows global system state

Google Sheets chosen for transparency and easy manual overrides

🛠️ Tech Stack

Frontend: Streamlit

Backend Logic: Python

Database: Google Sheets

Auth: Google Service Account

Libraries:

streamlit

pandas

gspread

google-auth