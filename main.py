"""
Main CLI Application - Flashcard Study System

This is the entry point for the FlashcardApp. It provides the command-line interface,
main menu, study session logic, flashcard management, statistics, and import/export features.
All user interaction and application flow is handled here.
"""

import sys
from pathlib import Path
from flashcard_manager import FlashcardManager
from study_session import create_study_session
from utils import (
    print_header, print_success, print_error, print_info,
    print_warning, clear_screen, get_user_input, batch_input_flashcards,
    display_statistics_table, display_card_details, shuffle_cards,
    Colors
)
from config import STUDY_MODES, DATA_DIR


class FlashcardApp:
    """
    Main application class for the Flashcard Study System.
    Handles user interaction, menu navigation, and delegates to the flashcard manager and study session logic.
    """

    def __init__(self):
        """
        Initialize the FlashcardApp, setting up the flashcard manager and app state.
        """
        self.manager = FlashcardManager()
        self.running = True

    def main_menu(self):
        """
        Display the main menu and prompt the user for an action.
        Returns the user's menu choice as a string.
        """
        clear_screen()
        print_header("FLASHCARD STUDY SYSTEM")
        
        print(f"{Colors.BOLD}Main Menu:{Colors.ENDC}")
        print("1. Start Study Session")
        print("2. Manage Flashcards")
        print("3. View Statistics")
        print("4. Import/Export")
        print("5. Settings")
        print("6. Exit")

        choice = get_user_input(
            "Choose an option (1-6): ",
            ['1', '2', '3', '4', '5', '6']
        )
        return choice

    def study_menu(self):
        """
        Study session menu with topic selector.
        Lets the user pick a question bank (topic), then a category, then a study mode.
        Loads questions only from the selected topic file for the session.
        """
        import os
        clear_screen()
        print_header("SELECT TOPIC (QUESTION BANK)")

        # List all .json files in data dir except flashcards.json and progress.json
        # This allows each topic/question bank to be a separate file
        topic_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json') and f not in ('flashcards.json', 'progress.json')]
        if not topic_files:
            print_error("No topic/question bank files found in data folder!")
            input("Press ENTER to continue...")
            return

        for i, fname in enumerate(topic_files, 1):
            print(f"{i}. {fname}")
        print(f"{len(topic_files) + 1}. Back")

        topic_choice = get_user_input(
            "Select topic: ",
            [str(i) for i in range(1, len(topic_files) + 2)]
        )

        if int(topic_choice) == len(topic_files) + 1:
            return

        selected_file = topic_files[int(topic_choice) - 1]
        topic_path = DATA_DIR / selected_file
        # Load flashcards from the selected topic file (does not import to main DB)
        cards = self.manager.load_flashcards_from_file(topic_path)

        if not cards:
            print_error("No cards found in this topic!")
            input("Press ENTER to continue...")
            return

        # Category selection within topic
        # User can filter by category or study all cards in the topic
        categories = sorted(set(card.category for card in cards))
        print(f"\n{Colors.BOLD}Choose Category:{Colors.ENDC}")
        for i, cat in enumerate(categories, 1):
            count = sum(1 for card in cards if card.category == cat)
            print(f"{i}. {cat} ({count} cards)")
        print(f"{len(categories) + 1}. All Categories")
        print(f"{len(categories) + 2}. Back")

        cat_choice = get_user_input(
            "Select category: ",
            [str(i) for i in range(1, len(categories) + 3)]
        )

        if int(cat_choice) == len(categories) + 2:
            return

        if int(cat_choice) == len(categories) + 1:
            filtered_cards = cards
        else:
            selected_cat = categories[int(cat_choice) - 1]
            filtered_cards = [card for card in cards if card.category == selected_cat]

        if not filtered_cards:
            # No cards in the selected category
            print_error("No cards in this category!")
            input("Press ENTER to continue...")
            return

        # Let user select study mode (learn, practice, quiz, spaced)
        print(f"\n{Colors.BOLD}Study Modes:{Colors.ENDC}")
        modes = list(STUDY_MODES.keys())
        for i, mode in enumerate(modes, 1):
            print(f"{i}. {STUDY_MODES[mode]}")

        mode_choice = get_user_input(
            "Select mode (1-4): ",
            [str(i) for i in range(1, len(modes) + 1)]
        )

        selected_mode = modes[int(mode_choice) - 1]

        clear_screen()
        # Create and run the study session
        session = create_study_session(filtered_cards, selected_mode)
        session.run()

        # Save any progress (e.g., review stats)
        self.manager.save_flashcards()
        input(f"\n{Colors.BOLD}Press ENTER to continue...{Colors.ENDC}")

    def manage_menu(self):
        """
        Flashcard management menu.
        Lets the user add, view, search, edit, or delete flashcards, and view weak cards.
        """
        clear_screen()
        print_header("MANAGE FLASHCARDS")

        print(f"{Colors.BOLD}Options:{Colors.ENDC}")
        print("1. Add Single Flashcard")
        print("2. Add Multiple Flashcards (Batch)")
        print("3. View All Flashcards")
        print("4. Search Flashcards")
        print("5. Edit Flashcard")
        print("6. Delete Flashcard")
        print("7. View Weak Cards")
        print("8. Back")

        choice = get_user_input("Choose an option (1-8): ", [str(i) for i in range(1, 9)])

        if choice == '1':
            self.add_single_flashcard()
        elif choice == '2':
            self.add_batch_flashcards()
        elif choice == '3':
            self.view_all_flashcards()
        elif choice == '4':
            self.search_flashcards()
        elif choice == '5':
            self.edit_flashcard()
        elif choice == '6':
            self.delete_flashcard()
        elif choice == '7':
            self.view_weak_cards()

    def add_single_flashcard(self):
        """
        Add a single flashcard by prompting the user for details.
        """
        clear_screen()
        print_header("ADD NEW FLASHCARD")

        question = input(f"{Colors.BOLD}Question: {Colors.ENDC}").strip()
        if not question:
            print_error("Question cannot be empty!")
            return

        answer = input(f"{Colors.BOLD}Answer: {Colors.ENDC}").strip()
        if not answer:
            print_error("Answer cannot be empty!")
            return

        category = input(f"{Colors.BOLD}Category (default: General): {Colors.ENDC}").strip() or "General"

        difficulty = input(f"{Colors.BOLD}Difficulty 1-5 (default: 3): {Colors.ENDC}").strip() or "3"
        try:
            difficulty = int(difficulty)
            difficulty = max(1, min(5, difficulty))
        except ValueError:
            difficulty = 3

        tags_input = input(f"{Colors.BOLD}Tags (comma-separated, optional): {Colors.ENDC}").strip()
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]

        card_id = self.manager.add_flashcard(question, answer, category, difficulty, tags)
        self.manager.save_flashcards()
        print_success(f"Flashcard added (ID: {card_id})")
        input("Press ENTER to continue...")

    def add_batch_flashcards(self):
        """
        Add multiple flashcards interactively in a batch.
        """
        clear_screen()
        flashcards = batch_input_flashcards()

        if flashcards:
            for card_data in flashcards:
                self.manager.add_flashcard(**card_data)
            self.manager.save_flashcards()
            print_success(f"Added {len(flashcards)} flashcards!")
        else:
            print_warning("No flashcards added.")

        input("Press ENTER to continue...")

    def view_all_flashcards(self):
        """
        View all flashcards in the main database, with summary and details.
        """
        clear_screen()
        cards = self.manager.get_all_flashcards()

        if not cards:
            print_error("No flashcards available!")
            input("Press ENTER to continue...")
            return

        print_header(f"ALL FLASHCARDS ({len(cards)} total)")

        for i, card in enumerate(cards, 1):
            acc_color = Colors.OKGREEN if card.get_accuracy() >= 80 else Colors.WARNING if card.get_accuracy() >= 60 else Colors.FAIL
            accuracy_str = f"{acc_color}{card.get_accuracy():.1f}%{Colors.ENDC}" if card.review_count > 0 else "Unreviewed"
            print(f"{i:3}. {card.question[:40]:40} | {accuracy_str}")

        choice = get_user_input(
            "View details of card number (or ENTER to skip): ",
            list(map(str, range(1, len(cards) + 1))) + ['']
        )

        if choice:
            card = cards[int(choice) - 1]
            clear_screen()
            display_card_details(card)
            input(f"\n{Colors.BOLD}Press ENTER to continue...{Colors.ENDC}")

    def search_flashcards(self):
        """
        Search flashcards by question or answer text.
        """
        clear_screen()
        query = input(f"{Colors.BOLD}Search query: {Colors.ENDC}").strip()

        if not query:
            print_warning("Search query cannot be empty!")
            input("Press ENTER to continue...")
            return

        results = self.manager.search_flashcards(query)

        clear_screen()
        print_header(f"SEARCH RESULTS ({len(results)} found)")

        if not results:
            print_error("No flashcards found!")
        else:
            for i, card in enumerate(results, 1):
                print(f"{i}. {card.question[:50]}")

        input("Press ENTER to continue...")

    def edit_flashcard(self):
        """
        Edit an existing flashcard by ID, allowing the user to update its fields.
        """
        clear_screen()
        print_header("EDIT FLASHCARD")

        card_id = input(f"{Colors.BOLD}Card ID to edit: {Colors.ENDC}").strip()
        card = self.manager.get_flashcard(card_id)

        if not card:
            print_error("Card not found!")
            input("Press ENTER to continue...")
            return

        display_card_details(card)

        print(f"\n{Colors.BOLD}Leave fields empty to keep existing values{Colors.ENDC}\n")

        new_question = input(f"New question: ").strip() or card.question
        new_answer = input(f"New answer: ").strip() or card.answer
        new_category = input(f"New category: ").strip() or card.category

        card.question = new_question
        card.answer = new_answer
        card.category = new_category

        self.manager.save_flashcards()
        print_success("Flashcard updated!")
        input("Press ENTER to continue...")

    def delete_flashcard(self):
        """
        Delete a flashcard by ID.
        """
        clear_screen()
        print_header("DELETE FLASHCARD")

        card_id = input(f"{Colors.BOLD}Card ID to delete: {Colors.ENDC}").strip()

        if self.manager.delete_flashcard(card_id):
            print_success("Flashcard deleted!")
        else:
            print_error("Card not found!")

        input("Press ENTER to continue...")

    def view_weak_cards(self):
        """
        View cards with low accuracy (below a threshold).
        Useful for targeted review of weak areas.
        """
        clear_screen()
        weak_cards = self.manager.get_weak_cards(threshold=70)

        if not weak_cards:
            print_info("No weak cards found! Great job!")
            input("Press ENTER to continue...")
            return

        print_header(f"WEAK CARDS (Accuracy < 70%)")
        for i, card in enumerate(weak_cards, 1):
            accuracy = f"{Colors.FAIL}{card.get_accuracy():.1f}%{Colors.ENDC}"
            print(f"{i}. {card.question[:40]:40} | {accuracy}")

        input("Press ENTER to continue...")

    def view_statistics(self):
        """
        View study statistics, including overall and per-category stats.
        """
        clear_screen()
        stats = self.manager.get_statistics()
        display_statistics_table(stats)
        input(f"\n{Colors.BOLD}Press ENTER to continue...{Colors.ENDC}")

    def import_menu(self):
        """
        Import/Export menu for flashcards.
        Lets the user import new flashcards from a file or export all flashcards.
        """
        clear_screen()
        print_header("IMPORT/EXPORT")

        print(f"{Colors.BOLD}Options:{Colors.ENDC}")
        print("1. Import Flashcards from File")
        print("2. Export All Flashcards")
        print("3. Back")

        choice = get_user_input("Choose an option (1-3): ", ['1', '2', '3'])

        if choice == '1':
            self.import_flashcards()
        elif choice == '2':
            self.export_flashcards()

    def import_flashcards(self):
        """
        Import flashcards from a JSON file in the data directory.
        """
        clear_screen()
        print_header("IMPORT FLASHCARDS")

        print(f"Place JSON file in: {DATA_DIR}")
        filename = input(f"{Colors.BOLD}Enter filename (e.g., week13.json): {Colors.ENDC}").strip()

        if not filename:
            print_warning("Import cancelled!")
            input("Press ENTER to continue...")
            return

        import_path = DATA_DIR / filename
        if not import_path.exists():
            print_error(f"File not found: {import_path}")
            input("Press ENTER to continue...")
            return

        count = self.manager.add_flashcards_from_file(import_path)
        print_success(f"Successfully imported {count} flashcards!")
        input("Press ENTER to continue...")

    def export_flashcards(self):
        """
        Export all flashcards to a JSON file in the data directory.
        """
        clear_screen()
        print_header("EXPORT FLASHCARDS")

        filename = input(f"{Colors.BOLD}Export filename (default: backup.json): {Colors.ENDC}").strip() or "backup.json"

        export_path = DATA_DIR / filename
        if self.manager.export_to_file(export_path):
            print_success(f"Exported to: {export_path}")
        else:
            print_error("Export failed!")

        input("Press ENTER to continue...")

    def settings_menu(self):
        """
        Settings menu for database info and data clearing.
        """
        clear_screen()
        print_header("SETTINGS")

        print(f"{Colors.BOLD}Database Information:{Colors.ENDC}")
        print(f"Database Path: {self.manager.db_path}")
        print(f"Total Cards: {len(self.manager.flashcards)}")

        print(f"\n{Colors.BOLD}Options:{Colors.ENDC}")
        print("1. Clear All Data (WARNING)")
        print("2. Back")

        choice = get_user_input("Choose an option (1-2): ", ['1', '2'])

        if choice == '1':
            confirm = get_user_input(
                f"{Colors.FAIL}Are you sure? This cannot be undone! (yes/no): {Colors.ENDC}",
                ['yes', 'no']
            )
            if confirm == 'yes':
                self.manager.flashcards = {}
                self.manager.save_flashcards()
                print_success("All data cleared!")
            else:
                print_info("Cancelled!")

        input("Press ENTER to continue...")

    def run(self):
        """
        Main application loop. Handles menu navigation and user actions.
        """
        try:
            while self.running:
                choice = self.main_menu()

                if choice == '1':
                    self.study_menu()
                elif choice == '2':
                    self.manage_menu()
                elif choice == '3':
                    self.view_statistics()
                elif choice == '4':
                    self.import_menu()
                elif choice == '5':
                    self.settings_menu()
                elif choice == '6':
                    print_success("Thank you for studying! Goodbye!")
                    self.running = False

        except KeyboardInterrupt:
            print(f"\n\n{Colors.WARNING}Application interrupted!{Colors.ENDC}")
            sys.exit(0)
        except Exception as e:
            print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
            sys.exit(1)


def main():
    """
    Entry point for running the FlashcardApp CLI.
    """
    app = FlashcardApp()
    app.run()


if __name__ == "__main__":
    main()