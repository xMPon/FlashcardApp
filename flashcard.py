"""
Core Flashcard class and data structures

Defines the Flashcard data model, including all fields, serialization,
accuracy tracking, and review logic. Used throughout the app for all card operations.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json


class Flashcard:
    """
    Represents a single flashcard with question, answer, and study metadata.
    Provides methods for serialization, accuracy tracking, and review updates.
    """

    def __init__(
        self,
        card_id: str,
        question: str,
        answer: str,
        category: str = "General",
        difficulty: int = 3,
        tags: Optional[list] = None,
        created_date: Optional[str] = None,
        last_reviewed: Optional[str] = None,
        review_count: int = 0,
        difficulty_rating: int = 3
    ):
        """
        Initialize a Flashcard object with all metadata and stats.
        """
        self.card_id = card_id
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.tags = tags or []
        self.created_date = created_date or datetime.now().isoformat()
        self.last_reviewed = last_reviewed
        self.review_count = review_count
        self.difficulty_rating = difficulty_rating  # User's perceived difficulty (1-5)
        self.times_correct = 0  # Number of correct answers
        self.times_incorrect = 0  # Number of incorrect answers

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert flashcard to dictionary for JSON serialization.
        """
        return {
            'card_id': self.card_id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'created_date': self.created_date,
            'last_reviewed': self.last_reviewed,
            'review_count': self.review_count,
            'difficulty_rating': self.difficulty_rating,
            'times_correct': self.times_correct,
            'times_incorrect': self.times_incorrect
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Flashcard':
        """
        Create a Flashcard object from a dictionary (typically loaded from JSON).
        """
        card = Flashcard(
            card_id=data.get('card_id'),
            question=data.get('question'),
            answer=data.get('answer'),
            category=data.get('category', 'General'),
            difficulty=data.get('difficulty', 3),
            tags=data.get('tags', []),
            created_date=data.get('created_date'),
            last_reviewed=data.get('last_reviewed'),
            review_count=data.get('review_count', 0),
            difficulty_rating=data.get('difficulty_rating', 3)
        )
        card.times_correct = data.get('times_correct', 0)
        card.times_incorrect = data.get('times_incorrect', 0)
        return card

    def mark_correct(self):
        """
        Mark card as answered correctly. Updates stats and last reviewed date.
        """
        self.times_correct += 1
        self.review_count += 1
        self.last_reviewed = datetime.now().isoformat()

    def mark_incorrect(self):
        """
        Mark card as answered incorrectly. Updates stats and last reviewed date.
        """
        self.times_incorrect += 1
        self.review_count += 1
        self.last_reviewed = datetime.now().isoformat()

    def get_accuracy(self) -> float:
        """
        Get accuracy percentage for this card (0-100).
        """
        total = self.times_correct + self.times_incorrect
        if total == 0:
            return 0.0
        return (self.times_correct / total) * 100

    def get_next_review_date(self, interval_days: int) -> str:
        """
        Calculate next review date based on spaced repetition interval.
        Returns ISO date string.
        """
        next_date = datetime.now() + timedelta(days=interval_days)
        return next_date.isoformat()

    def __repr__(self) -> str:
        """
        String representation for debugging.
        """
        return f"Flashcard(id={self.card_id}, question={self.question[:30]}...)"
