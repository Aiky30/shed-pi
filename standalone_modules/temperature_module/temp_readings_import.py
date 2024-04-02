"""
A script ot import the data that has already been gathered

Historic data structure:
    "Shed pi started: {get_time()}, using version: 0.0.1"
    "Pi temp: {pi_temp}, probe_1 temp: {probe_1_temp}"

FIXME:
    Allow the data submission endpoint to take multiple device modules and readings.
    Example: Pi has it's own data and so does the temp probe. More effecient to send at once
"""

data_feed = "./data/shed-pi-2024-04-02.log"

with open(data_feed, "r") as file_feed:

    for log in file_feed.readlines():
        log_parts = log.split(":INFO:parent:")
        log_timestamp = log_parts[0]
        log_message = log_parts[1]

        # Handle started at message
        if log_message.startswith("Shed pi started: "):
            # Need a way to be able to record events, such as the device turning on / off
            continue

        elif log_message.startswith("Pi temp: "):
            temps = log_message.split(": ")

            if len(temps) > 2:
                assert temps[0] == "Pi temp"
                # Splti the next reading into 2
                partial_reading = temps[1].split(",")
                assert partial_reading[1] == " probe_1 temp"

                pi_temp = partial_reading[0]
                probe_temp = temps[2].strip()
            else:
                assert temps[0] == "Pi temp"
                pi_temp = temps[1].strip()
        # DeviceModuleReading.get_or_create(
        #     created_at=
        #     data=
        # )
