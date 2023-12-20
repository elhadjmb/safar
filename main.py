from logic import Player


def main():
    player = Player()

    while True:
        print("\nMenu:")
        print("1. Setup Monitors")
        print("2. Setup Videos")
        print("3. Create Sequences")
        print("4. Start a Sequence")
        print("5. Stop a Sequence")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            player.setup_monitors()
        elif choice == '2':
            player.setup_videos()
        elif choice == '3':
            player.create_sequences()
        elif choice == '4':
            sequence_id = int(input("Enter the sequence ID to start: "))
            player.start_sequence(sequence_id)
        elif choice == '5':
            sequence_id = int(input("Enter the sequence ID to stop: "))
            player.stop_sequence(sequence_id)
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
