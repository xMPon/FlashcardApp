"""
Flashcard Manager - handles loading, saving, and querying flashcards

This module provides the FlashcardManager class, which manages the flashcard database,
file import/export, and querying/filtering of flashcards. It is responsible for all
persistent storage and retrieval of flashcard data.
"""

import json
from typing import List, Dict, Optional, Any
from pathlib import Path
from datetime import datetime
from flashcard import Flashcard
from config import FLASHCARDS_DB, PROGRESS_DB



class FlashcardManager:
    """
    Manages the flashcard database and operations.
    Handles loading, saving, importing, exporting, and querying flashcards.
    """

    def load_flashcards_from_file(self, file_path: Path) -> list:
        """
        Load flashcards from a specific JSON file (returns a list of Flashcard objects).
        Used for loading question banks for a session without importing to the main DB.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, list):
                print(f"✗ Invalid format in {file_path.name}. Expected JSON array of flashcards.")
                return []
            cards = []
            for item in data:
                if 'question' in item and 'answer' in item:
                    card = Flashcard(
                        card_id=self._generate_card_id(),
                        question=item['question'],
                        answer=item['answer'],
                        category=item.get('category', 'General'),
                        difficulty=item.get('difficulty', 3),
                        tags=item.get('tags', [])
                    )
                    cards.append(card)
            return cards
        except Exception as e:
            print(f"✗ Error loading flashcards from {file_path.name}: {e}")
            return []

    def __init__(self, db_path: Path = FLASHCARDS_DB):
        """
        Initialize the FlashcardManager, loading the main flashcard database.
        """
        self.db_path = db_path
        self.progress_path = PROGRESS_DB
        self.flashcards: Dict[str, Flashcard] = {}
        self.load_flashcards()

    def load_flashcards(self) -> None:
        """
        Load flashcards from the main JSON database file into memory.
        """
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.flashcards = {
                        card_id: Flashcard.from_dict(card_data)
                        for card_id, card_data in data.items()
                    }
                print(f"✓ Loaded {len(self.flashcards)} flashcards")
            except json.JSONDecodeError:
                print("⚠ Database file corrupted. Starting fresh.")
                self.flashcards = {}
        else:
            print("ℹ No existing database. Starting fresh.")
            self.flashcards = {}

    def save_flashcards(self) -> None:
        """
        Save all flashcards in memory to the main JSON database file.
        """
        try:
            data = {
                card_id: card.to_dict()
                for card_id, card in self.flashcards.items()
            }
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {len(self.flashcards)} flashcards")
        except Exception as e:
            print(f"✗ Error saving flashcards: {e}")

    def add_flashcard(
        self,
        question: str,
        answer: str,
        category: str = "General",
        difficulty: int = 3,
        tags: Optional[List[str]] = None
    ) -> str:
        """
        Add a new flashcard to the database.
        Returns the generated card_id.
        """
        card_id = self._generate_card_id()
        card = Flashcard(
            card_id=card_id,
            question=question,
            answer=answer,
            category=category,
            difficulty=difficulty,
            tags=tags or []
        )
        self.flashcards[card_id] = card
        return card_id

    def add_flashcards_from_file(self, import_path: Path) -> int:
        """
        Import flashcards from a JSON file and add them to the main database.
        File format: list of dicts with question, answer, category, difficulty, tags.
        Returns the number of cards imported.
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("✗ Invalid format. Expected JSON array of flashcards.")
                return 0

            count = 0
            for item in data:
                if 'question' in item and 'answer' in item:
                    self.add_flashcard(
                        question=item['question'],
                        answer=item['answer'],
                        category=item.get('category', 'General'),
                        difficulty=item.get('difficulty', 3),
                        tags=item.get('tags', [])
                    )
                    count += 1

            self.save_flashcards()
            print(f"✓ Imported {count} flashcards from {import_path.name}")
            return count

        except Exception as e:
            print(f"✗ Error importing flashcards: {e}")
            return 0

    def delete_flashcard(self, card_id: str) -> bool:
        """
        Delete a flashcard by card_id. Returns True if deleted, False if not found.
        """
        if card_id in self.flashcards:
            del self.flashcards[card_id]
            self.save_flashcards()
            return True
        return False

    def get_flashcard(self, card_id: str) -> Optional[Flashcard]:
        """
        Get a flashcard by its card_id. Returns the Flashcard or None.
        """
        return self.flashcards.get(card_id)

    def get_all_flashcards(self) -> List[Flashcard]:
        """
        Get all flashcards in the main database as a list.
        """
        return list(self.flashcards.values())

    def get_by_category(self, category: str) -> List[Flashcard]:
        """
        Get all flashcards in the main database matching a category.
        """
        return [
            card for card in self.flashcards.values()
            if card.category.lower() == category.lower()
        ]

    def get_by_tags(self, tags: List[str]) -> List[Flashcard]:
        """
        Get all flashcards in the main database that have any of the given tags.
        """
        return [
            card for card in self.flashcards.values()
            if any(tag in card.tags for tag in tags)
        ]

    def get_by_difficulty(self, difficulty: int) -> List[Flashcard]:
        """
        Get all flashcards in the main database with a given difficulty level.
        """
        return [
            card for card in self.flashcards.values()
            if card.difficulty == difficulty
        ]

    def get_weak_cards(self, threshold: float = 50.0) -> List[Flashcard]:
        """
        Get cards with accuracy below the given threshold (percentage).
        Only includes cards that have been reviewed at least once.
        """
        weak = [
            card for card in self.flashcards.values()
            if card.get_accuracy() < threshold and card.review_count > 0
        ]
        return sorted(weak, key=lambda x: x.get_accuracy())

    def get_unreviewed_cards(self) -> List[Flashcard]:
        """
        Get cards that have never been reviewed.
        """
        return [
            card for card in self.flashcards.values()
            if card.review_count == 0
        ]

    def get_categories(self) -> List[str]:
        """
        Get all unique categories present in the main database.
        """
        return sorted(set(card.category for card in self.flashcards.values()))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get study statistics for the main database, including totals and per-category stats.
        """
        total_cards = len(self.flashcards)
        reviewed_cards = len([c for c in self.flashcards.values() if c.review_count > 0])
        
        total_correct = sum(card.times_correct for card in self.flashcards.values())
        total_attempts = sum(
            card.times_correct + card.times_incorrect
            for card in self.flashcards.values()
        )
        overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        categories = self.get_categories()
        category_stats = {
            cat: {
                'total': len(self.get_by_category(cat)),
                'reviewed': len([c for c in self.get_by_category(cat) if c.review_count > 0])
            }
            for cat in categories
        }

        return {
            'total_cards': total_cards,
            'reviewed_cards': reviewed_cards,
            'unreviewed_cards': total_cards - reviewed_cards,
            'total_attempts': total_attempts,
            'overall_accuracy': round(overall_accuracy, 2),
            'categories': category_stats,
            'last_updated': datetime.now().isoformat()
        }

    def search_flashcards(self, query: str) -> List[Flashcard]:
        """
        Search flashcards by question or answer substring (case-insensitive).
        Returns a list of matching flashcards.
        """
        query_lower = query.lower()
        return [
            card for card in self.flashcards.values()
            if query_lower in card.question.lower() or
               query_lower in card.answer.lower()
        ]

    def _generate_card_id(self) -> str:
        """
        Generate a unique card ID for a new flashcard.
        """
        import uuid
        return f"card_{uuid.uuid4().hex[:8]}"

    def export_to_file(self, export_path: Path) -> bool:
        """
        Export all flashcards in the main database to a JSON file.
        Returns True if successful, False otherwise.
        """
        try:
            data = [card.to_dict() for card in self.flashcards.values()]
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Exported {len(data)} flashcards to {export_path.name}")
            return True
        except Exception as e:
            print(f"✗ Error exporting flashcards: {e}")
            return False
