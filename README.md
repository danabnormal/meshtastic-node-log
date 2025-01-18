# Meshtastic Node Info Backup Script

This script connects to a Meshtastic node over IP, retrieves information about all seen nodes, and stores this data in a JSON file. It keeps a history of changes for each node, ensuring that updates are logged only when the data changes.

## Features

  -  Fetches and backs up all node information from a Meshtastic device.
  -  Maintains a history of changes for each node, adding new entries only when data updates.
  -  Includes an option to force the creation of a new history entry, even without changes.
---

## Requirements

### Prerequisites

  -  Python 3.6 or later
  -  A configured meshtastic node connected to your network and accessible via IP

A setup script is provided that sets up a suitable virtual environment and installs required modules.

---

## Automatic Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/my-python-tool.git
   cd my-python-tool
2. Run the setup script to configure the virtual environment and install dependencies:
   ```bash
   ./setup.sh
   ```
---

## Usage
### Running the Script

Run the script from the command line using the following syntax:

```bash
python script_name.py <node_ip_address> <output_file> [--force_update]
```

### Arguments
| Argument           | Description                                                      | Required |
|--------------------|------------------------------------------------------------------|----------|
| `<node_ip_address>` | The IP address of the Meshtastic node to connect to.            | Yes      |
| `<output_file>`     | The path to the JSON file where the backup will be saved.       | Yes      |
| `--force_update`    | Optional flag to force a new history entry, even without changes. | No       |

### Example Commands

  1.  Backup node information:

```bash
meshtastic_node_log.sh 192.168.1.100 all_node_info_backup.json
```
  2.  Force a new history entry:

```bash
meshtastic_node_log.sh 192.168.1.100 all_node_info_backup.json --force_update
```

---
## JSON Output Format

The script generates a JSON file with the following structure:
```json
{
    "timestamp": "2025-01-18T12:34:56.789123",
    "nodes": {
        "12345": {
            "current": {
                "user": {
                    "longName": "Alice",
                    "shortName": "A",
                    "id": "12345678"
                },
                "position": {
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "altitude": 15.0,
                    "battery_level": 95
                },
                "hardware": {
                    "num": 1,
                    "firmware_version": "1.2.3",
                    "hardware_version": "2.1"
                },
                "lastSeen": 1674059785,
                "snr": 20,
                "hopLimit": 3
            },
            "history": [
                {
                    "timestamp": "2025-01-18T12:34:56.789123",
                    "data": {
                        "user": {
                            "longName": "Alice",
                            "shortName": "A",
                            "id": "12345678"
                        },
                        "position": {
                            "latitude": 37.7749,
                            "longitude": -122.4194,
                            "altitude": 15.0,
                            "battery_level": 95
                        },
                        "hardware": {
                            "num": 1,
                            "firmware_version": "1.2.3",
                            "hardware_version": "2.1"
                        },
                        "lastSeen": 1674059785,
                        "snr": 20,
                        "hopLimit": 3
                    }
                }
            ]
        }
    }
}
```
---
## Notes
- Ensure the Meshtastic node is reachable on the specified IP address before running the script.
- The JSON file will be updated with any new or changed data, preserving historical entries.
- Use the `--force_update` flag if you want to add a history entry even when data hasn't changed.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.