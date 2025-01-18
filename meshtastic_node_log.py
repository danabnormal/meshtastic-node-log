#!/usr/bin/python3
import meshtastic
import meshtastic.tcp_interface
import json
from datetime import datetime
import os
import argparse


def has_data_changed(existing_data, new_data):
    """
    Compares the current data with the latest history entry to determine if any field has changed.
    Returns True if any field has changed, otherwise False.
    """
    for key in new_data:
        if key not in existing_data or existing_data[key] != new_data[key]:
            return True
    return False


def merge_node_data(existing_data, new_data, force_update=False):
    """
    Merges new node data into the existing backup, ensuring only new or changed data is added to history.

    Args:
        existing_data (dict): The current backup data.
        new_data (dict): The newly fetched node data.
        force_update (bool): If True, forces a new history entry even if no data has changed.

    Returns:
        dict: Merged node data.
    """
    for node_id, new_node in new_data.items():
        if node_id in existing_data:
            existing_node = existing_data[node_id]

            # Check if data has changed (based on any field)
            if force_update or has_data_changed(existing_node["current"], new_node):
                # Add a new history entry
                existing_node["history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "data": new_node
                })
                # Update the "current" data
                existing_node["current"] = new_node
        else:
            # Create a new entry if the node is not in the existing data
            existing_data[node_id] = {
                "current": new_node,
                "history": [{
                    "timestamp": datetime.now().isoformat(),
                    "data": new_node
                }]
            }

    return existing_data


def backup_all_meshtastic_node_info(ip_address, output_file, force_update=False):
    """
    Connects to a Meshtastic node over IP, retrieves all available information about other nodes,
    merges with the existing backup, and saves the data to a JSON file.

    Args:
        ip_address (str): IP address of the Meshtastic node.
        output_file (str): Path to the output JSON file.
        force_update (bool): If True, forces a new history entry even if no data has changed.
    """
    # Connect to the Meshtastic node via IP
    interface = meshtastic.tcp_interface.TCPInterface(ip_address)

    try:
        # Fetch all node information
        nodes = interface.nodes

        # Prepare new node data
        new_node_data = {}
        for node_id, node in nodes.items():
            user = node.get("user", {})
            position = node.get("position", {})
            hardware = node.get("hardware", {})

            new_node_data[node_id] = {
                "user": {
                    "longName": user.get("longName", "Unknown"),
                    "shortName": user.get("shortName", "Unknown"),
                    "id": user.get("id", "Unknown"),
                },
                "position": {
                    "latitude": position.get("latitude", None),
                    "longitude": position.get("longitude", None),
                    "altitude": position.get("altitude", None),
                    "battery_level": position.get("batteryLevel", None),
                },
                "hardware": {
                    "num": node.get("num", None),
                    "firmware_version": node.get("firmwareVersion", "Unknown"),
                    "hardware_version": node.get("hardwareVersion", "Unknown"),
                },
                "lastSeen": node.get("lastSeen", None),
                "snr": node.get("snr", None),
                "hopLimit": node.get("hopLimit", None),
                "battery_level": node.get("battery_level", None),
            }

        # Load existing backup data if the file exists
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                existing_data = json.load(f).get("nodes", {})
        else:
            existing_data = {}

        # Merge new data into existing data
        merged_data = merge_node_data(existing_data, new_node_data, force_update)

        # Add a timestamp for when the backup was created
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "nodes": merged_data,
        }

        # Save merged data to a JSON file
        with open(output_file, "w") as f:
            json.dump(backup_data, f, indent=4)

        print(f"All node information has been backed up to {output_file}")

    finally:
        # Ensure the connection is closed
        interface.close()

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Backup all Meshtastic node information to a JSON file.")
    parser.add_argument("ip_address", type=str, help="IP address of the Meshtastic node")
    parser.add_argument("output_file", type=str, help="Path to the output JSON file")
    parser.add_argument(
        "--force_update", action="store_true",
        help="Force a new history entry even if no data has changed"
    )
    args = parser.parse_args()

    # Call the backup function with parsed arguments
    backup_all_meshtastic_node_info(args.ip_address, args.output_file, force_update=args.force_update)

if __name__ == "__main__":
    main()