import time

def mode_1():
    print("Radio")
    # Simulate doing something in mode 1
    time.sleep(2)
    print("Finished mode 1.")

def mode_2():
    print("Grateful Dead")
    # Simulate doing something in mode 2
    time.sleep(2)
    print("Finished mode 2.")

def mode_3():
    print("Music Library")
    # Simulate doing something in mode 3
    time.sleep(2)
    print("Finished mode 3.")

def main():
    while True:
        print("Select a mode:")
        print("1: Radio")
        print("2: Grateful Dead")
        print("3: Music Library")
        print("q: Quit")

        choice = input("Enter mode number (1/2/3) or 'q' to quit: ").strip()

        if choice == '1':
            mode_1()
        elif choice == '2':
            mode_2()
        elif choice == '3':
            mode_3()
        elif choice.lower() == 'q':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 'q'.")

if __name__ == "__main__":
    main()
