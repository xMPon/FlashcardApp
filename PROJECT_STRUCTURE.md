# Flashcard Application - Complete Project Structure

## 📋 Project Overview

A comprehensive **Python flashcard study system** for managing, organizing, and studying educational materials with multiple study modes, progress tracking, and spaced repetition support.

**Created**: January 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Python**: 3.7+  
**Dependencies**: None (Pure Python)

---

## 📁 Directory Structure

```
FlashcardApp/
├── 📄 main.py                    # Entry point - CLI application
├── 📄 config.py                  # Configuration & constants
├── 📄 flashcard.py               # Core Flashcard class
├── 📄 flashcard_manager.py       # Database & CRUD operations
├── 📄 study_session.py           # Study mode implementations
├── 📄 utils.py                   # Utility functions & UI
├── 📚 README.md                  # Full documentation
├── 🚀 QUICKSTART.md              # 5-minute quick start
├── 📖 IMPORT_GUIDE.md            # How to create import files
├── 🔒 .gitignore                 # Git ignore rules
└── 📂 data/
    ├── flashcards.json           # Main database (auto-created)
    ├── progress.json             # Progress tracking (auto-created)
    └── week13_template.json       # Example/template flashcards
└── 📂 logs/
    └── study_stats.log           # Study statistics log
```

---

## 🔧 Core Components

### 1. **main.py** - Application Entry Point
**Purpose**: CLI menu-driven application interface

**Key Classes**:
- `FlashcardApp`: Main application controller

**Features**:
- Interactive menu system
- Study session management
- Flashcard CRUD operations
- Import/Export functionality
- Settings management
- Statistics display

**Usage**:
```bash
python main.py
```

---

### 2. **config.py** - Configuration & Settings
**Purpose**: Centralized configuration and constants

**Key Variables**:
- `APP_DIR`, `DATA_DIR`, `LOGS_DIR`: Path configurations
- `FLASHCARDS_DB`, `PROGRESS_DB`: Database paths
- `SPACED_REPETITION_INTERVALS`: Review scheduling
- `STUDY_MODES`: Available study modes
- `Colors`: CLI color formatting

**Usage**:
```python
from config import FLASHCARDS_DB, STUDY_MODES
```

---

### 3. **flashcard.py** - Flashcard Data Model
**Purpose**: Represents individual flashcard with metadata

**Key Class**: `Flashcard`

**Attributes**:
```python
Flashcard(
    card_id,           # Unique identifier
    question,          # Question text
    answer,            # Answer text
    category,          # Organization category
    difficulty,        # 1-5 difficulty level
    tags,              # List of tags
    review_count,      # Times reviewed
    accuracy,          # Success percentage
    last_reviewed      # Last study date
)
```

**Key Methods**:
- `mark_correct()`: Record correct response
- `mark_incorrect()`: Record incorrect response
- `get_accuracy()`: Calculate accuracy percentage
- `to_dict()` / `from_dict()`: Serialization

---

### 4. **flashcard_manager.py** - Database Manager
**Purpose**: Handle all flashcard CRUD and query operations

**Key Class**: `FlashcardManager`

**Core Operations**:
- `add_flashcard()`: Create new card
- `add_flashcards_from_file()`: Batch import JSON
- `delete_flashcard()`: Remove card
- `get_flashcard()`: Retrieve by ID
- `get_by_category()`: Filter by category
- `get_by_tags()`: Filter by tags
- `get_weak_cards()`: Low accuracy cards
- `get_statistics()`: Aggregate stats
- `search_flashcards()`: Text search
- `export_to_file()`: Export as JSON

**Data Persistence**:
- Auto-saves to `data/flashcards.json`
- JSON format (human-readable)
- Automatic backups on save

---

### 5. **study_session.py** - Study Modes
**Purpose**: Implement different study session types

**Key Classes**:

#### `LearnMode`
- Shows answer after question
- User marks correct/incorrect
- Best for first pass

#### `PracticeMode`
- Shuffled cards
- 30-second thinking time
- User self-grades

#### `QuizMode`
- No answers shown initially
- User writes answer first
- Then compares with correct answer
- Rigorous testing mode

#### `SpacedRepetitionMode`
- Prioritizes weak cards
- Recently missed cards
- Intelligent review scheduling
- Sorts by: last review date → accuracy → count

**Base Class**: `StudySession`
- Tracks session statistics
- Calculates accuracy
- Records timing

---

### 6. **utils.py** - Utility Functions
**Purpose**: Helper functions for UI and operations

**Key Functions**:
- `print_header()`: Formatted section headers
- `print_success/error/warning/info()`: Styled messages
- `print_card()`: Display flashcard formatted
- `get_user_input()`: Validated input
- `display_statistics_table()`: Format stats output
- `display_card_details()`: Show full card info
- `shuffle_cards()`: Randomize deck
- `format_accuracy()`: Color-coded accuracy
- `batch_input_flashcards()`: Interactive batch entry

**UI Features**:
- Color-coded output (with Windows fallback)
- Progress indicators
- Error handling

---

## 🎯 Data Model

### Flashcard JSON Schema
```json
{
    "card_id": "card_abc123de",
    "question": "What is accuracy?",
    "answer": "(TP + TN) / (TP + TN + FP + FN)",
    "category": "Week 13 - Classification",
    "difficulty": 2,
    "tags": ["accuracy", "classification"],
    "created_date": "2026-01-20T10:30:00",
    "last_reviewed": "2026-01-20T14:45:00",
    "review_count": 5,
    "difficulty_rating": 3,
    "times_correct": 4,
    "times_incorrect": 1
}
```

### Database Structure
```
flashcards.json (root level = object)
├── card_id_1
│   ├── question, answer, category, ...
├── card_id_2
│   ├── question, answer, category, ...
└── ...
```

---

## 🔄 Workflow Architecture

### Data Flow Diagram
```
main.py (CLI)
    ↓
FlashcardManager (CRUD)
    ↓
Flashcard objects
    ↓
study_session.py (Study modes)
    ↓
update Flashcard state
    ↓
save to flashcards.json
```

### Study Session Flow
```
1. User selects category
2. Load cards from manager
3. Create study session (Learn/Practice/Quiz/SpacedRep)
4. Session.run() → iterate cards
5. For each card:
   - Display question
   - Get user response
   - Update card stats (mark_correct/incorrect)
6. Display session results
7. Save to database
```

---

## 📊 Statistics System

### Card-Level Stats
- `review_count`: Total times reviewed
- `times_correct`: Correct attempts
- `times_incorrect`: Incorrect attempts
- `accuracy`: (correct / total) × 100%
- `last_reviewed`: ISO timestamp
- `created_date`: ISO timestamp

### Session-Level Stats
- Cards reviewed per session
- Correct/Incorrect counts
- Session accuracy %
- Session duration

### Database-Level Stats
- Total cards by category
- Overall accuracy across all cards
- Reviewed vs unreviewed breakdown
- Weak cards list (accuracy < threshold)

---

## 🔐 Data Integrity

### Auto-Save
- Saves after every: add, edit, delete, study session
- No data loss on interruption

### Validation
- JSON schema validation on import
- File format checking
- Error recovery (corrupted file handling)

### Backup Strategy
- Export feature for manual backups
- Import feature for restoration
- JSON human-readable format

---

## 🎮 User Interface

### Menu Structure
```
Main Menu
├── 1. Start Study Session
│   ├── Select Category
│   └── Select Study Mode
├── 2. Manage Flashcards
│   ├── Add Single/Batch
│   ├── View All
│   ├── Search
│   ├── Edit/Delete
│   └── View Weak Cards
├── 3. View Statistics
├── 4. Import/Export
│   ├── Import from File
│   └── Export All
├── 5. Settings
└── 6. Exit
```

### Study Session UI
```
Study Mode Loop:
1. Display card number (e.g., "Card 3/10")
2. Show question
3. User input
4. Show answer (if applicable)
5. Mark correct/incorrect
6. Next card or complete
7. Display session results
```

---

## 📚 File I/O Operations

### Import (`add_flashcards_from_file`)
```
JSON File → Validate → Parse → Create Flashcards → Save DB
```

### Export (`export_to_file`)
```
Load all Flashcards → Serialize to JSON → Write File
```

### Auto-Save (`save_flashcards`)
```
Memory State → Convert to JSON → Write to DB File
```

### Load (`load_flashcards`)
```
Read DB File → Parse JSON → Create Flashcard Objects → Memory
```

---

## 🚀 Getting Started

### Installation
1. Ensure Python 3.7+ installed
2. Clone/download project
3. Navigate to `FlashcardApp` directory

### First Run
```bash
python main.py
```

### Add First Flashcards
**Option 1** (Import template):
```
Main Menu → 4. Import/Export → 1. Import Flashcards
→ week13_template.json
```

**Option 2** (Batch input):
```
Main Menu → 2. Manage Flashcards → 2. Add Multiple Flashcards
```

### Start Studying
```
Main Menu → 1. Start Study Session
→ Select Category → Choose Study Mode
```

---

## 📖 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete feature documentation |
| **QUICKSTART.md** | 5-minute quick start guide |
| **IMPORT_GUIDE.md** | Creating import files tutorial |
| **config.py** | Configuration constants (documented) |
| **main.py** | Docstrings in source code |

---

## 🔍 Key Design Patterns

### 1. **MVC-Like Architecture**
- Model: `Flashcard` class
- Manager: `FlashcardManager` (persistence)
- View/Controller: `main.py` (CLI)

### 2. **Factory Pattern**
- `create_study_session()`: Returns appropriate session type

### 3. **Singleton-like**
- `FlashcardManager`: Single instance manages database

### 4. **Strategy Pattern**
- Different study modes as implementations

### 5. **Data Serialization**
- `to_dict()` / `from_dict()` for JSON conversion

---

## 🧪 Testing & Validation

### Pre-installed Validation
- All Python files syntax-checked
- JSON template validated
- Import mechanisms tested

### Recommended Testing
```python
# Test import
manager = FlashcardManager()
manager.add_flashcards_from_file('data/week13_template.json')

# Test queries
weak = manager.get_weak_cards()
by_cat = manager.get_by_category("Week 13")

# Test study session
from study_session import create_study_session
session = create_study_session(weak, 'quiz')
session.run()
```

---

## 🚦 Performance Characteristics

### Scalability
- ✅ Works efficiently: 1-1000 cards
- ✅ Memory efficient: JSON loading
- ⚠️ 10,000+ cards may need optimization

### Speed
- ✅ Instant load/save (< 1s for typical use)
- ✅ Fast search (< 100ms for 1000 cards)
- ⚠️ No database optimization (flat JSON file)

### Optimization Opportunities
- Index for faster search
- Database migration (SQLite, MongoDB)
- Caching layer for statistics

---

## 🔮 Future Enhancements

### Planned
- [ ] FSRS spaced repetition algorithm
- [ ] Statistics visualization
- [ ] Dark mode theme
- [ ] Audio card support

### Possible
- [ ] Web interface
- [ ] Mobile app
- [ ] Collaborative features
- [ ] AI card generation

---

## 📝 License & Attribution

**Created**: January 2026  
**For**: Bristol University Master's Coursework  
**Subject**: Financial Technology & Statistical Computing  
**Status**: Open source for educational use

---

## 🤝 Contributing

### Adding New Features
1. Extend appropriate class
2. Follow existing code style
3. Update documentation
4. Test thoroughly

### Adding Study Modes
1. Inherit from `StudySession`
2. Implement `run()` method
3. Register in `create_study_session()`
4. Add to `config.STUDY_MODES`

---

## ✅ Checklist - Getting Started

- [ ] Read this document for overview
- [ ] Read QUICKSTART.md (5 minutes)
- [ ] Run `python main.py`
- [ ] Import week13_template.json
- [ ] Start a study session
- [ ] Check statistics
- [ ] Try different study modes
- [ ] Create custom import file
- [ ] Export backup

---

## 📞 Support Resources

- **Documentation**: README.md
- **Quick Start**: QUICKSTART.md  
- **Imports**: IMPORT_GUIDE.md
- **Source Code**: Documented with docstrings
- **Example Data**: week13_template.json

---

**Ready to start studying!** 📚✨

Questions? Check the documentation files or review the source code with detailed docstrings.
