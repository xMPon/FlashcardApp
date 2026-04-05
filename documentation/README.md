# Flashcard Study System

A comprehensive Python application for creating, managing, and studying flashcards with multiple study modes.

## Features

### 📚 Study Modes
- **Learn Mode**: Study all cards with answers shown. Mark each as correct/incorrect.
- **Practice Mode**: Timed study (30s per card) with shuffled deck. Tests real understanding.
- **Quiz Mode**: No peeking! Answer first, then see correct answer. Best for self-assessment.
- **Spaced Repetition**: Intelligently prioritizes weak areas and recently missed cards.

### 🎯 Flashcard Management
- Add single or batch flashcards
- Organize by categories and difficulty levels (1-5)
- Tag-based organization for better navigation
- Search across questions and answers
- Edit and delete existing cards
- View detailed card statistics (accuracy, review count, dates)

### 📊 Statistics & Progress Tracking
- Overall accuracy calculation
- Per-card accuracy tracking
- Review count and attempt history
- Category-based performance breakdown
- Weak card identification (accuracy < threshold)
- Automatic date tracking (created, last reviewed)

### 💾 Data Management
- JSON-based storage (human-readable, easy to backup)
- Import flashcards from JSON files
- Export all flashcards for backup
- Automatic data persistence
- Batch import capability

---

## Installation

### Requirements
- Python 3.7+
- No external dependencies required! (Uses only Python standard library)

### Setup
1. Navigate to the FlashcardApp directory:
```bash
cd FlashcardApp
```

2. Run the application:
```bash
python main.py
```

---

## Quick Start

### First Time Setup
1. Launch the application: `python main.py`
2. Choose "Manage Flashcards" → "Add Multiple Flashcards (Batch)" to create your first cards
3. Or import existing cards: "Import/Export" → "Import Flashcards from File"

### Adding Flashcards

#### Method 1: Single Card
```
Main Menu → 2. Manage Flashcards → 1. Add Single Flashcard
```

#### Method 2: Batch Import (Recommended for weekly updates)
```
Main Menu → 4. Import/Export → 1. Import Flashcards from File
```

#### Method 3: Interactive Batch Input
```
Main Menu → 2. Manage Flashcards → 2. Add Multiple Flashcards (Batch)
```

### Studying
```
Main Menu → 1. Start Study Session
→ Select Category (or "All Categories")
→ Choose Study Mode (Learn/Practice/Quiz/Spaced Repetition)
```

---

## Data Format

### Flashcard JSON Format
To import flashcards, create a JSON file with the following structure:

```json
[
    {
        "question": "What is Python?",
        "answer": "Python is a high-level programming language.",
        "category": "Programming",
        "difficulty": 2,
        "tags": ["basics", "python"]
    },
    {
        "question": "What is a class?",
        "answer": "A class is a blueprint for creating objects in OOP.",
        "category": "Programming",
        "difficulty": 3,
        "tags": ["oop", "classes", "python"]
    }
]
```

### Fields
- **question** (required): The question text
- **answer** (required): The answer text
- **category** (optional): Category name (default: "General")
- **difficulty** (optional): 1-5 scale (default: 3)
- **tags** (optional): List of tag strings for organization

---

## File Structure

```
FlashcardApp/
├── main.py                 # Entry point - CLI application
├── flashcard.py            # Flashcard class definition
├── flashcard_manager.py    # Database management and operations
├── study_session.py        # Study mode implementations
├── utils.py                # Utility functions and UI helpers
├── config.py               # Configuration and constants
├── data/                   # Data storage directory
│   ├── flashcards.json     # Main database (auto-created)
│   ├── progress.json       # Study progress (auto-created)
│   └── week13_template.json # Example flashcards
├── logs/                   # Logging directory
│   └── study_stats.log     # Study statistics log
└── README.md              # This file
```

---

## Usage Guide

### Main Menu Options

#### 1. Start Study Session
Launch a study session. Choose category, then study mode:
- **Learn**: See answer after attempting
- **Practice**: Timed (30s) with shuffled cards
- **Quiz**: Self-graded (you decide correctness)
- **Spaced Repetition**: Smart prioritization

#### 2. Manage Flashcards
- Add, edit, delete, search, or view cards
- Identify weak areas
- View detailed card information

#### 3. View Statistics
See overall performance:
- Total cards and review counts
- Overall accuracy percentage
- Performance by category
- Last update timestamp

#### 4. Import/Export
- **Import**: Load flashcards from JSON files
- **Export**: Backup all flashcards

#### 5. Settings
- View database information
- Clear all data (with confirmation)

#### 6. Exit
Save and exit the application

---

## Workflow for Weekly Updates

### Adding New Week's Materials

1. **Prepare JSON file** with flashcards for new week:
```bash
# Create file: week14_flashcards.json in FlashcardApp/data/
```

2. **Import in application**:
```
Main Menu → 4. Import/Export → 1. Import Flashcards from File
→ Enter filename: week14_flashcards.json
```

3. **Study immediately**:
```
Main Menu → 1. Start Study Session
→ Select Week 14 category
→ Choose preferred study mode
```

4. **Track progress**:
```
Main Menu → 3. View Statistics
```

---

## Study Tips

### Recommended Study Workflow
1. **First Pass**: Use **Learn Mode** to see all cards and answers
2. **Practice**: Use **Practice Mode** to self-assess
3. **Self-Testing**: Use **Quiz Mode** for rigorous testing
4. **Review**: Use **Spaced Repetition** to focus on weak areas
5. **Final Check**: Review weak cards until accuracy > 80%

### Difficulty Levels
- **1**: Basic definitions/terminology
- **2**: Simple concepts
- **3**: Moderate difficulty (default)
- **4**: Complex relationships
- **5**: Advanced/synthesis questions

### Effective Tagging
```
Tags suggest: ["concept_name", "course_module", "difficulty_indicator"]
Examples: ["precision", "classification", "important"]
          ["regression", "week13", "formula"]
```

---

## Keyboard Shortcuts & Tips

### During Study Sessions
- **ENTER**: Confirm/proceed to next card
- **Ctrl+C**: Interrupt session (data is saved)
- Type carefully: Answers are case-insensitive for user-graded modes

### For Batch Input
- Type questions and answers naturally
- Type "END" on new line to finish batch
- Leave optional fields blank to skip

---

## Statistics Explained

### Per-Card Metrics
- **Accuracy**: (Correct / Total Attempts) × 100%
- **Review Count**: Total times card has been reviewed
- **Last Reviewed**: Most recent study session date

### Overall Metrics
- **Overall Accuracy**: Sum of all correct / sum of all attempts
- **Weak Cards**: Cards with accuracy < 70%
- **Category Performance**: Breakdown by organization category

---

## Data Storage & Backup

### Automatic Storage
All data is automatically saved to:
- **Flashcards**: `data/flashcards.json`
- **Progress**: `data/progress.json`

### Manual Backup
```
Main Menu → 4. Import/Export → 2. Export All Flashcards
→ Enter backup filename (e.g., backup_jan20.json)
```

### Restore from Backup
```
Main Menu → 4. Import/Export → 1. Import Flashcards from File
→ Select backup file
```

---

## Troubleshooting

### No flashcards appear after import
- Check JSON file format (must be valid JSON array)
- Ensure file is in `FlashcardApp/data/` directory
- Verify required fields: "question" and "answer"

### Application crashes on import
- Check for special characters (ensure UTF-8 encoding)
- Validate JSON syntax using online JSON validator
- Check terminal error message for details

### Accuracy showing as "Unreviewed"
- Card hasn't been studied yet
- Study the card in any mode to generate metrics

### Colors not displaying on Windows
- This is normal and expected
- Functionality is unchanged

---

## Example Workflow

### Week 13 Classification Metrics
1. Copy `week13_template.json` content to create `week13_flashcards.json`
2. Add custom cards or modify existing ones
3. Save to `FlashcardApp/data/`
4. In app: Import → select file
5. Study → Choose "Week 13 - Classification Metrics" category
6. Use Spaced Repetition for weak areas
7. Export backup when done

---

## API for Advanced Users

### Import Programmatically
```python
from flashcard_manager import FlashcardManager

manager = FlashcardManager()
manager.add_flashcards_from_file('data/week13.json')
weak_cards = manager.get_weak_cards(threshold=60)
stats = manager.get_statistics()
```

### Create Custom Study Sessions
```python
from study_session import create_study_session
from flashcard_manager import FlashcardManager

manager = FlashcardManager()
cards = manager.get_by_category("Week 13")
session = create_study_session(cards, 'quiz')
session.run()
```

---

## Future Enhancement Ideas

- [ ] Spaced repetition algorithm (FSRS)
- [ ] Progress visualization (charts/graphs)
- [ ] Voice/audio card support
- [ ] Mobile app integration
- [ ] Collaborative study groups
- [ ] AI-powered card generation
- [ ] Dark mode theme
- [ ] Performance analytics

---

## Notes

- All data stored locally (no cloud sync)
- Application saves automatically after each study session
- No internet required
- Works offline entirely
- Pure Python - no complex dependencies

---

## Support & Questions

For issues or questions:
1. Check the troubleshooting section above
2. Review the JSON format in data/ directory
3. Check file permissions in data/ and logs/ directories
4. Ensure Python 3.7+ is installed

---

**Created**: January 2026
**Last Updated**: January 20, 2026
**Version**: 1.0.0
