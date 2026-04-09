"""
Utility functions for the flashcard application
"""

import random
from typing import List
from datetime import datetime
from flashcard import Flashcard
from config import Colors


def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(text: str, width: int = 60):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * width}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(width)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * width}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_card(card: Flashcard, show_answer: bool = False):
    """Pretty print a flashcard"""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}Q: {card.question}{Colors.ENDC}")
    if show_answer:
        print(f"{Colors.OKGREEN}A: {card.answer}{Colors.ENDC}")


def shuffle_cards(cards: List[Flashcard]) -> List[Flashcard]:
    """Shuffle flashcards"""
    shuffled = cards.copy()
    random.shuffle(shuffled)
    return shuffled


def get_user_input(prompt: str, valid_options: List[str] = None) -> str:
    """Get validated user input"""
    while True:
        user_input = input(f"\n{Colors.BOLD}{prompt}{Colors.ENDC}").strip()
        if valid_options is None or user_input.lower() in [opt.lower() for opt in valid_options]:
            return user_input
        print_error(f"Invalid input. Please choose from: {', '.join(valid_options)}")


def get_multiline_input(prompt: str) -> str:
    """Get multiline user input (type 'END' on new line to finish)"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.ENDC}")
    print("(Type 'END' on a new line when finished)")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)


def format_accuracy(accuracy: float) -> str:
    """Format accuracy with color coding"""
    if accuracy >= 80:
        color = Colors.OKGREEN
    elif accuracy >= 60:
        color = Colors.WARNING
    else:
        color = Colors.FAIL
    return f"{color}{accuracy:.1f}%{Colors.ENDC}"


def format_date(iso_date: str) -> str:
    """Format ISO date to readable format"""
    if not iso_date:
        return "Never"
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%d %H:%M")
    except:
        return "Invalid date"


def display_statistics_table(stats: dict):
    """Display statistics in a formatted table"""
    print(f"\n{Colors.BOLD}{'OVERALL STATISTICS':-^60}{Colors.ENDC}")
    print(f"Total Cards:        {stats['total_cards']}")
    print(f"Reviewed:           {stats['reviewed_cards']}")
    print(f"Unreviewed:         {stats['unreviewed_cards']}")
    print(f"Total Attempts:     {stats['total_attempts']}")
    print(f"Overall Accuracy:   {format_accuracy(stats['overall_accuracy'])}")
    
    if stats['categories']:
        print(f"\n{Colors.BOLD}{'CATEGORY BREAKDOWN':-^60}{Colors.ENDC}")
        for category, cat_stats in sorted(stats['categories'].items()):
            print(f"{category:20} {cat_stats['total']:3} total, {cat_stats['reviewed']:3} reviewed")


def batch_input_flashcards() -> List[dict]:
    """Interactive batch input for multiple flashcards"""
    flashcards = []
    print_header("BATCH FLASHCARD INPUT")
    
    category = input(f"{Colors.BOLD}Category for all cards: {Colors.ENDC}").strip() or "General"
    difficulty = input(f"{Colors.BOLD}Difficulty (1-5, default 3): {Colors.ENDC}").strip() or "3"
    
    try:
        difficulty = int(difficulty)
        if not 1 <= difficulty <= 5:
            difficulty = 3
    except ValueError:
        difficulty = 3
    
    count = 0
    while True:
        print(f"\n{Colors.BOLD}--- Flashcard {len(flashcards) + 1} ---{Colors.ENDC}")
        question = input("Question (or 'DONE' to finish): ").strip()
        
        if question.upper() == 'DONE':
            break
        
        if not question:
            print_warning("Question cannot be empty!")
            continue
        
        answer = input("Answer: ").strip()
        if not answer:
            print_warning("Answer cannot be empty!")
            continue
        
        tags_input = input("Tags (comma-separated, optional): ").strip()
        tags = [t.strip() for t in tags_input.split(',') if t.strip()]
        
        flashcards.append({
            "question": question,
            "answer": answer,
            "category": category,
            "difficulty": difficulty,
            "tags": tags
        })
        print_success(f"Flashcard added!")
        count += 1
    
    return flashcards


def display_card_details(card: Flashcard):
    """Display detailed information about a flashcard"""
    print(f"\n{Colors.BOLD}{'CARD DETAILS':-^60}{Colors.ENDC}")
    print(f"ID:                {card.card_id}")
    print(f"Question:          {card.question}")
    print(f"Answer:            {card.answer}")
    print(f"Category:          {card.category}")
    print(f"Difficulty:        {card.difficulty}/5")
    print(f"Tags:              {', '.join(card.tags) if card.tags else 'None'}")
    print(f"Created:           {format_date(card.created_date)}")
    print(f"Last Reviewed:     {format_date(card.last_reviewed)}")
    print(f"Review Count:      {card.review_count}")
    print(f"Correct:           {card.times_correct}")
    print(f"Incorrect:         {card.times_incorrect}")
    print(f"Accuracy:          {format_accuracy(card.get_accuracy())}")
