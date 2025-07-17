#!/usr/bin/env python3
# File: delhivery.py

import argparse
import requests
import sys
import os
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(LOG_DIR, "tracking_log.txt")

def fetch_tracking_info(awb):
    url = f"https://dlv-api.delhivery.com/v3/unified-tracking?wbn={awb}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.delhivery.com",
        "Referer": "https://www.delhivery.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

def save_log(timestamp, awb, status_line, slot_line, last_scan_info):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}] AWB: {awb}\n")
        f.write(status_line + "\n")
        if slot_line:
            f.write(slot_line + "\n")
        if last_scan_info:
            f.write("Last Tracking Entry:\n")
            f.write(f"  Location: {last_scan_info['Location']}\n")
            f.write(f"  Scan    : {last_scan_info['Scan']}\n")
            f.write(f"  Remark  : {last_scan_info['Remark']}\n")

def display_info(data):
    if not data.get("data"):
        console.print("[bold yellow]No data found for the given AWB.[/bold yellow]")
        return

    shipment = data["data"][0]
    awb = shipment.get('awb', 'N/A')

    # Status date
    raw_datetime = shipment.get('status', {}).get('statusDateTime')
    try:
        dt = datetime.fromisoformat(raw_datetime)
    except:
        dt = datetime.now(timezone.utc)

    formatted_time = dt.astimezone(timezone(timedelta(hours=5, minutes=30))).strftime("%d %b %Y, %I:%M %p")
    log_time = dt.astimezone(timezone(timedelta(hours=5, minutes=30))).strftime("%d/%m/%y %I:%M %p")

    # ETA & status
    status_line = (
        f"Updated On (IST): {formatted_time} │ "
        f"ETA: {shipment.get('deliveryDate', 'N/A')}"
    )

    # Slot info (Scheduled delivery window)
    slot_line = None
    slot = shipment.get("slot")
    if slot and all(k in slot for k in ("date", "from", "to")):
        slot_line = f"Scheduled Slot: {slot['date']} from {slot['from']} to {slot['to']}"

    # Panel output
    panel_info = Panel.fit(
        f"[bold cyan]AWB:[/bold cyan] {awb}\n"
        f"[bold cyan]Status:[/bold cyan] {shipment.get('hqStatus')} ({shipment.get('status', {}).get('status', 'N/A')})\n"

        f"[bold cyan]Package Type:[/bold cyan] {shipment.get('packageType', 'N/A')}\n"
        f"[bold cyan]Product Type:[/bold cyan] {shipment.get('productType', 'N/A')}\n"
        f"[bold cyan]Reference No:[/bold cyan] {shipment.get('referenceNo', 'N/A')}\n"
        f"[bold cyan]Updated On (IST):[/bold cyan] {formatted_time}\n"
        f"[bold cyan]ETA:[/bold cyan] {shipment.get('deliveryDate', 'N/A')}\n"
        f"[bold cyan]Slot:[/bold cyan] {slot['date']} from {slot['from']} to {slot['to']}" if slot else "" + "\n",
        title="📦 Delhivery Shipment Info",
        border_style="blue"
    )
    console.print(panel_info)

    #Report
    last_scan_info = None
    if shipment.get("trackingStates"):
        table = Table(title="Report", show_header=True, header_style="bold magenta")
        table.add_column("Location", style="cyan")
        table.add_column("Scan", style="green")
        table.add_column("Remark", style="white")

        for state in shipment["trackingStates"]:
            for scan in state.get("scans", []):
                location = scan.get("cityLocation", "N/A")
                scan_type = scan.get("scan", "N/A")
                remark = scan.get("scanNslRemark", "N/A")
                last_scan_info = {
                    "Location": location,
                    "Scan": scan_type,
                    "Remark": remark
                }
                table.add_row(location, scan_type, remark)
        console.print(table)

    save_log(log_time, awb, status_line, slot_line, last_scan_info)

def main():
    parser = argparse.ArgumentParser(description="Track Delhivery shipment by AWB number.")
    parser.add_argument("awb", type=str, help="AWB number to track")
    args = parser.parse_args()

    data = fetch_tracking_info(args.awb)
    display_info(data)

if __name__ == "__main__":
    main()