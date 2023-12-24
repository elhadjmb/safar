from interface import KeyPressGUI
from logic import Player


def headless():
    player = Player()

    while True:
        print("\nSteps:")
        print("0. Preconfigure Monitors and Videos")
        print("1. Setup Monitors")
        print("2. Setup Videos")
        print("3. Create Sequences")
        print("4. Start a Sequence")
        print("5. Stop a Sequence")
        print("6. Exit")

        player.load_config()
        if not player.screens:
            player.setup_screens()
        if not player.videos:
            player.setup_videos()
        if not player.sequences:
            player.create_sequences()
        save = input("Save config? (y/n): ")
        if save == 'y':
            player.save_config()

        while True:
            sequence_id = int(input(f"Enter the sequence ID to start ({player.sequences}): "))
            player.start_sequence(sequence_id)

            choice = input("Stop sequence? (y/n/q): ")
            if choice == 'y':
                print("Stopping sequence...")
                player.stop_sequence(sequence_id)
            elif choice == 'q':
                print("Stopping sequence...")
                player.stop_sequence(sequence_id)
                break

        choice = input("Exit? (y/n): ")
        if choice == 'y':
            print("Exiting the program...")
            break


def graphical():
    player = Player(True)
    gui = KeyPressGUI(player)


def main(headless):
    if headless:
        headless()
    else:
        graphical()


if __name__ == "__main__":
    main(headless=False)
