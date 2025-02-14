import os
import requests
import random

# 🔍 Fetch all available years with Grateful Dead shows
def get_gd_years():
    base_url = "https://archive.org/advancedsearch.php"
    queries = [
        'creator:"Grateful Dead" AND date:[1969-01-01 TO 1985-12-31]',
        'creator:"Grateful Dead" AND date:[1986-01-01 TO 1995-12-31]'
    ]

    all_dates = set()

    for query in queries:
        params = {
            "q": query,
            "fl[]": "date",
            "sort[]": "date asc",
            "rows": 10000,
            "output": "json"
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            num_results = data.get("response", {}).get("numFound", 0)
            new_dates = [doc.get("date", "UNKNOWN") for doc in data.get("response", {}).get("docs", [])]
            all_dates.update([d[:4] for d in new_dates if d[:4].isdigit()])

    filtered_dates = sorted(year for year in all_dates if 1969 <= int(year) <= 1995)
    return filtered_dates if filtered_dates else ["1969"]

# 🔍 Get all Grateful Dead shows for a given year
def get_gd_shows(year):
    base_url = "https://archive.org/advancedsearch.php"
    query = {
        "q": f'creator:"Grateful Dead" AND date:{year}',
        "fl[]": "identifier,title",
        "sort[]": "date asc",
        "rows": 1000,
        "output": "json"
    }

    response = requests.get(base_url, params=query)
    if response.status_code == 200:
        data = response.json()
        shows = data.get("response", {}).get("docs", [])
        return shows if shows else None
    return None

# 🎲 Select a random Grateful Dead show from a given year
def get_random_show(year):
    shows = get_gd_shows(year)
    if not shows:
        return None

    show = random.choice(shows)

    # Extract date & venue if available
    show_date = show.get("date", "Unknown Date")
    venue = show.get("venue", "Unknown Venue")

    return {
        "identifier": show["identifier"],
        "title": show["title"],
        "date": show_date,
        "venue": venue
    }

# 🎵 Get a playable audio stream URL from a show's archive.org identifier
def get_stream_urls(identifier):
    url = f"https://archive.org/metadata/{identifier}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        files = data.get("files", [])

        stream_urls = []
        for file in files:
            if file.get("format") == "VBR MP3":  # ✅ Collect all MP3 files
                stream_urls.append(f"https://archive.org/download/{identifier}/{file['name']}")

        if stream_urls:
            return stream_urls  # ✅ Return full list of tracks

    print("No valid stream found.")
    return None

def mode_1():
    stations = {
        "1": ("NTS Live", "https://stream-relay-geo.ntslive.net/stream"),
        "2": ("dublab", "http://dublab.out.airtime.pro:8000/dublab_a"),
        "3": ("The Lot Radio", "http://thelothq.out.airtime.pro:8000/thelothq_a"),
        "4": ("Worldwide FM", "http://worldwidefm.out.airtime.pro:8000/worldwidefm_a")
    }

    index = 0
    station_keys = list(stations.keys())

    while True:
        station_id = station_keys[index]
        station_name, stream_url = stations[station_id]

        print(f"\n📻 Now Playing: {station_name}")
        os.system("mpc stop > /dev/null 2>&1")
        os.system("mpc clear > /dev/null 2>&1")
        os.system(f"mpc add {stream_url} > /dev/null 2>&1")
        os.system("mpc play > /dev/null 2>&1")

        print("\nOptions: [n] Next Station | [p] Previous Station | [q] Quit")
        choice = input("Enter choice: ").strip().lower()

        if choice == 'n':
            index = (index + 1) % len(station_keys)
        elif choice == 'p':
            index = (index - 1) % len(station_keys)
        elif choice == 'q':
            print("📴 Exiting Internet Radio mode...")
            os.system("mpc stop > /dev/null 2>&1")
            return
        else:
            print("❌ Invalid choice. Use 'n', 'p', or 'q'.")


#  Mode 2: Select a Year and Play a Random Grateful Dead Show
def mode_2():
    print("\nFetching available years for Grateful Dead shows...")
    years = get_gd_years()  # Dynamically fetch available years
    index = 0

    while True:
        selected_year = years[index]
        print(f"\n📅 Selected Year: {selected_year}")
        print("Options: [n] Next Year | [p] Previous Year | [s] Select Year | [k] Skip Track | [q] Quit")

        choice = input("Enter choice: ").strip().lower()

        if choice == 'n':
            index = (index + 1) % len(years)  # Move to next available year
        elif choice == 'p':
            index = (index - 1) % len(years)  # Move to previous available year
        elif choice == 's':
            print(f"\n🎵 Fetching a random Grateful Dead show from {selected_year}...")

            show = get_random_show(selected_year)
            if not show:
                print("❌ No shows found for this year. Try another.")
                continue

            identifier = show["identifier"]
            title = show["title"]
            show_date = show["date"]
            venue = show["venue"]

            print(f"\n🎶 Selected Show: {title}")
            print(f"📅 Date: {show_date} | 🏟️ Venue: {venue}")

            # ✅ Fetch all track URLs (instead of just one track)
            stream_urls = get_stream_urls(identifier)
            if not stream_urls:
                print("❌ No playable files found for this show.")
                continue

            print(f"🎶 Adding {len(stream_urls)} tracks to the playlist...")

            # 🎯 Ensure playback starts fresh every time
            os.system("mpc stop > /dev/null 2>&1")
            os.system("mpc clear > /dev/null 2>&1")

            # ✅ Add all tracks to MPC
            for url in stream_urls:
                os.system(f"mpc add {url} > /dev/null 2>&1")

            os.system("mpc play > /dev/null 2>&1")
            os.system("mpc seek 0 > /dev/null 2>&1")  # Ensure playback starts at 0:00

        elif choice == 'k':
            print("⏭️ Skipping to next track...")
            os.system("mpc next > /dev/null 2>&1")  # ✅ Skip to the next track
        elif choice == 'q':
            print("📴 Exiting Grateful Dead mode...")
            os.system("mpc stop > /dev/null 2>&1")
            return
        else:
            print("❌ Invalid choice. Use 'n', 'p', 's', 'k', or 'q'.")

def main():
    while True:  # ✅ Keep looping until user quits the entire app
        print("\n🎛️ Select a mode:")
        print("1: 📻 Internet Radio")
        print("2: 🎸 Grateful Dead Archive")
        print("q: ❌ Quit")

        choice = input("Enter mode number (1/2) or 'q' to quit: ").strip()

        if choice == '1':
            mode_1()  # ✅ This function must return properly too
        elif choice == '2':
            mode_2()  # ✅ When this returns, the menu reappears
        elif choice == 'q':
            print("🔴 Stopping playback and exiting program.")
            os.system("mpc stop > /dev/null 2>&1")
            break  # ✅ Exit the loop when the user chooses to quit
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 'q'.")

if __name__ == "__main__":
    main()
