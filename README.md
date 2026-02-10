# Skylark Drone Operations AI Agent 🚁

## Overview
Skylark Drones operates multiple drones and pilots across concurrent client projects. 
This project implements a conversational AI agent that automates pilot roster management, drone inventory tracking, assignment coordination, and conflict detection using Google Sheets as the backend.

The system reduces manual coordination overhead by enabling natural-language queries and real-time updates.

---

## Features

### 1. Pilot Roster Management
- Query pilot availability by skill, location, and status
- View current assignments
- Update pilot status (Available / Assigned / On Leave)
- Two-way sync with Google Sheets

### 2. Assignment Tracking
- Match pilots to missions based on skills and availability
- Track current assignments
- Handle urgent reassignments with priority-based logic

### 3. Drone Inventory Management
- Query drones by capability, availability, and location
- Exclude drones under maintenance
- Track deployment readiness

### 4. Conflict Detection
- Prevent pilot double-booking
- Detect skill or certification mismatches
- Flag maintenance conflicts
- Handle pilot-drone location mismatches

---

## Urgent Reassignment Logic
For high-priority scenarios, the agent identifies the best available pilot and reassigns them immediately, updating the pilot status and assignment in Google Sheets. This ensures minimal disruption and fast operational response.

---

## Tech Stack
- **Frontend:** Streamlit (Conversational UI)
- **Backend:** Python
- **Data Store:** Google Sheets
- **APIs:** Google Sheets API, Google Drive API
- **Libraries:** pandas, gspread, oauth2client

---

## Architecture

