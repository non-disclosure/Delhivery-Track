
Delhivery Shipment Tracker CLI
A simple, fast, and elegant command-line tool to track Delhivery shipments directly from your terminal.
This script fetches the latest tracking information for a given Air Waybill (AWB) number from Delhivery's API and presents it in a clean, readable format. It also keeps a local log of all your tracked shipments.


 # Features
 * Track by AWB: Track any Delhivery shipment using its AWB number.
 * Clean Output: Displays information in a clean, readable table and panel using the rich library.
 * Detailed Info: Shows key details like ETA, current status, package type, and full tracking history.
 * **It'll Show you Delhivery's Schedule (slot) , which is not visible in official app/web.**
 * Local Logging: Automatically logs every query to a local tracking_log.txt file for your records.
 * Cross-Platform: Works on Windows, Linux, and Termux (Android).
Setup & Installation

# Usage
You'll need Git and Python 3 installed on your system.
 * Clone the repository:
   git clone https://github.com/non-disclosure/Delhivery-Track.git

 * Navigate into the directory:
   cd Delhivery-Track

 * Install the required dependencies:
   > For Windows & Linux (with Python/pip installed):
     pip install requests rich

   > For Termux (Android):
     pkg update && pkg upgrade
pkg install python git
pip install requests rich

Usage
Run the script from your terminal and provide the AWB number as an argument.
python delhivery.py <YOUR_AWB_NUMBER>

Example:
python delhivery.py 4417310325997

Logging
All tracking lookups are automatically saved with a timestamp in tracking_log.txt in the same directory as the script. This file is created automatically on the first run.
