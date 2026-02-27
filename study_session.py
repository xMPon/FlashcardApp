"""
Study session modes - Learn, Practice, Quiz, Spaced Repetition
"""

import random
import time
from typing import List, Tuple
from flashcard import Flashcard
from utils import (
    print_header, print_card, print_success, print_error, 
    print_info, get_user_input, clear_screen, shuffle_cards,
    format_accuracy, Colors
)


class StudySession:
    """Base class for study sessions"""

    def __init__(self, cards: List[Flashcard], mode: str):
        self.cards = cards
        self.mode = mode
        self.current_index = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.start_time = None

    def run(self):
        """Run the study session"""
        raise NotImplementedError

    def get_results(self) -> dict:
        """Get session results"""
        total = self.correct_count + self.incorrect_count
        accuracy = (self.correct_count / total * 100) if total > 0 else 0
        
        return {
            'mode': self.mode,
            'total_cards': len(self.cards),
            'cards_reviewed': total,
            'correct': self.correct_count,
            'incorrect': self.incorrect_count,
            'accuracy': round(accuracy, 2),
            'duration': time.time() - self.start_time if self.start_time else 0
        }

    def display_results(self):
        """Display session results"""
        results = self.get_results()
        print_header(f"SESSION COMPLETE - {self.mode.upper()}")
        print(f"Cards Reviewed:    {results['cards_reviewed']} / {results['total_cards']}")
        print(f"Correct:           {results['correct']}")
        print(f"Incorrect:         {results['incorrect']}")
        print(f"Accuracy:          {format_accuracy(results['accuracy'])}")
        duration = int(results['duration'])
        print(f"Duration:          {duration // 60}m {duration % 60}s")


class LearnMode(StudySession):
    """Learn mode - Study all cards with answers shown"""

    def run(self):
        """Run learn mode session"""
        if not self.cards:
            print_error("No flashcards available!")
            return

        self.start_time = time.time()
        print_header(f"LEARN MODE - {len(self.cards)} Cards")

        for i, card in enumerate(self.cards, 1):
            print(f"\n{Colors.BOLD}Card {i}/{len(self.cards)}{Colors.ENDC}")
            print_card(card, show_answer=False)

            response = get_user_input(
                "Press ENTER to reveal answer, or (s)kip: ",
                ['', 's']
            )

            if response.lower() != 's':
                print_card(card, show_answer=True)
                mark = get_user_input(
                    "Mark as (c)orrect, (i)ncorrect, or skip marking: ",
                    ['c', 'i', '']
                )

                if mark.lower() == 'c':
                    card.mark_correct()
                    self.correct_count += 1
                    print_success("Marked correct!")
                elif mark.lower() == 'i':
                    card.mark_incorrect()
                    self.incorrect_count += 1
                    print_error("Marked incorrect!")

        self.display_results()


class PracticeMode(StudySession):
    """Practice mode - Timed study with answer reveal"""

    def run(self):
        """Run practice mode session"""
        if not self.cards:
            print_error("No flashcards available!")
            return

        self.start_time = time.time()
        self.cards = shuffle_cards(self.cards)
        print_header(f"PRACTICE MODE - {len(self.cards)} Cards (Shuffled)")

        time_per_card = 30  # seconds

        for i, card in enumerate(self.cards, 1):
            print(f"\n{Colors.BOLD}Card {i}/{len(self.cards)}{Colors.ENDC}")
            print(f"{Colors.WARNING}Think for {time_per_card}s...{Colors.ENDC}")
            print_card(card, show_answer=False)

            start = time.time()
            try:
                input(f"\nPress ENTER when ready to reveal (after {time_per_card}s)")
            except KeyboardInterrupt:
                print("\nSession interrupted!")
                return

            print_card(card, show_answer=True)
            elapsed = time.time() - start

            response = get_user_input(
                "Was your answer (c)orrect, (i)ncorrect, or (s)kip: ",
                ['c', 'i', 's']
            )

            if response.lower() == 'c':
                card.mark_correct()
                self.correct_count += 1
                print_success("Correct!")
            elif response.lower() == 'i':
                card.mark_incorrect()
                self.incorrect_count += 1
                print_error("Incorrect!")

        self.display_results()


class QuizMode(StudySession):
    """Quiz mode - Test yourself without seeing answers first"""

    def run(self):
        """Run quiz mode session"""
        if not self.cards:
            print_error("No flashcards available!")
            return

        self.start_time = time.time()
        self.cards = shuffle_cards(self.cards)
        print_header(f"QUIZ MODE - {len(self.cards)} Cards (No Peaking!)")

        for i, card in enumerate(self.cards, 1):
            print(f"\n{Colors.BOLD}Card {i}/{len(self.cards)}{Colors.ENDC}")
            print_card(card, show_answer=False)

            user_answer = input(f"{Colors.BOLD}Your answer: {Colors.ENDC}").strip()

            if not user_answer:
                print_warning = lambda x: print(f"{Colors.WARNING}⚠ {x}{Colors.ENDC}")
                print_warning("No answer provided!")
                self.incorrect_count += 1
            else:
                print(f"\n{Colors.OKGREEN}Correct Answer:{Colors.ENDC}")
                print(f"{card.answer}")

                correct = get_user_input(
                    "Was your answer (c)orrect or (i)ncorrect: ",
                    ['c', 'i']
                )

                if correct.lower() == 'c':
                    card.mark_correct()
                    self.correct_count += 1
                    print_success("Great job!")
                else:
                    card.mark_incorrect()
                    self.incorrect_count += 1
                    print_error("Incorrect!")

        self.display_results()


class SpacedRepetitionMode(StudySession):
    """Spaced Repetition - Review cards optimized by accuracy"""

    def run(self):
        """Run spaced repetition session"""
        if not self.cards:
            print_error("No flashcards available!")
            return

        self.start_time = time.time()

        # Sort by: least recently reviewed, then by lowest accuracy
        sorted_cards = sorted(
            self.cards,
            key=lambda c: (c.last_reviewed is None, -c.get_accuracy(), -c.review_count)
        )

        print_header(f"SPACED REPETITION - Focus on weak areas")
        print(f"Cards prioritized by review date and accuracy\n")

        for i, card in enumerate(sorted_cards, 1):
            accuracy = format_accuracy(card.get_accuracy())
            print(f"\n{Colors.BOLD}Card {i}/{len(sorted_cards)}{Colors.ENDC}")
            print(f"Previous Accuracy: {accuracy} | Reviews: {card.review_count}")

            print_card(card, show_answer=False)

            response = get_user_input(
                "Show answer (y/n): ",
                ['y', 'n']
            )

            if response.lower() == 'y':
                print_card(card, show_answer=True)

                correct = get_user_input(
                    "Mark as (c)orrect or (i)ncorrect: ",
                    ['c', 'i']
                )

                if correct.lower() == 'c':
                    card.mark_correct()
                    self.correct_count += 1
                    print_success("Correct!")
                else:
                    card.mark_incorrect()
                    self.incorrect_count += 1
                    print_error("Incorrect! This will be reviewed again soon.")

        self.display_results()


def create_study_session(cards: List[Flashcard], mode: str) -> StudySession:
    """Factory function to create study session"""
    modes = {
        'learn': LearnMode,
        'practice': PracticeMode,
        'quiz': QuizMode,
        'spaced': SpacedRepetitionMode
    }

    session_class = modes.get(mode.lower(), LearnMode)
    return session_class(cards, mode)
