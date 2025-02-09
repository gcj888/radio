import os
import time

# Predefined list of internet radio streams
RADIO_STATIONS = [
    {"name": "Station 1", "url": "http://example.com/stream1.mp3"},
    {"name": "Station 2", "url": "http://example.com/stream2.mp3"},
    {"name": "Station 3", "url": "http://example.com/stream3.mp3"},
    {"name": "Station 4", "url": "http://example.com/stream4.mp3"},
    {"name": "Station 5", "url": "http://example.com/stream5.mp3"},
]

# Current selected station index
current_station_index = 0


def display_station():
    station = RADIO_STATIONS[current_station_index]
    print(f"Current Station: {station['name']}")


def play_station():
    station = RADIO_STATIONS[current_station_index]
    print(f"Playing {station['name']}...")
    os.system(f"mpc clear && mpc add {station['url']} && mpc play")


def next_station():
    global current_station_index
    current_station_index = (current_station_index + 1) % len(RADIO_STATIONS)
    display_station()


def prev_station():
    global current_station_index
    current_station_index = (current_station_index - 1) % len(RADIO_STATIONS)
    display_station()


def main():
    display_station()

    while True:
        print("\nOptions:")
        print("n: Next station")
        print("p: Previous station")
        print("s: Select station and play")
        print("q: Quit")

        choice = input("Enter choice: ").strip().lower()

        if choice == "n":
            next_station()
        elif choice == "p":
            prev_station()
        elif choice == "s":
            play_station()
        elif choice == "q":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
