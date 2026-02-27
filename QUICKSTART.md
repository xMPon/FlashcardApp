# Flashcard Study System - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Launch the Application
```bash
cd FlashcardApp
python main.py
```

You'll see the main menu:
```
==================================================
        FLASHCARD STUDY SYSTEM
==================================================

Main Menu:
1. Start Study Session
2. Manage Flashcards
3. View Statistics
4. Import/Export
5. Settings
6. Exit
```

---

## 📝 Three Ways to Add Flashcards

### Option A: Import Pre-Made Flashcards (RECOMMENDED FOR WEEKLY UPDATES)

**Best for**: Adding Week 13, Week 14, etc. materials all at once

1. In main menu, select: **4. Import/Export**
2. Select: **1. Import Flashcards from File**
3. Type filename: `week13_template.json` (or your file name)
4. Done! Cards are now in your database

**File Format** (save as `.json`):
```json
[
    {
        "question": "What is Python?",
        "answer": "A programming language",
        "category": "Week 13",
        "difficulty": 2,
        "tags": ["python", "basics"]
    }
]
```

### Option B: Quick Batch Input

**Best for**: Adding 5-10 cards interactively

1. In main menu, select: **2. Manage Flashcards**
2. Select: **2. Add Multiple Flashcards (Batch)**
3. Enter category (e.g., "Week 13")
4. Enter difficulty (1-5)
5. Enter each Q&A pair, type "DONE" when finished

### Option C: Single Card Input

**Best for**: Adding one card at a time

1. In main menu, select: **2. Manage Flashcards**
2. Select: **1. Add Single Flashcard**
3. Enter details
4. Repeat as needed

---

## 🎓 Start Studying

### The Study Session Workflow

1. **Main menu** → **1. Start Study Session**
2. **Select category** (e.g., "Week 13 - Classification Metrics")
3. **Choose study mode**:
   - **Learn**: See answers, good for first pass
   - **Practice**: Timed (30s per card), shuffled
   - **Quiz**: Self-graded without seeing answers
   - **Spaced Repetition**: Smart review of weak areas

4. **Study each card** and mark correct/incorrect
5. **View results** at end of session

---

## 📊 Check Your Progress

In main menu, select: **3. View Statistics**

You'll see:
- Total flashcards
- Cards reviewed vs unreviewed
- Overall accuracy %
- Performance by category

---

## 💡 Recommended Study Plan

### Week 1 of New Material
1. **Import** new flashcards (Option A above)
2. Use **Learn Mode** to see all cards and answers
3. Use **Practice Mode** to self-test

### Week 2-3: Active Review
1. Use **Quiz Mode** for rigorous self-testing
2. Use **Spaced Repetition** to focus on weak cards
3. Check statistics to track improvement

### Before Exam
1. Review **weak cards** (accuracy < 70%)
2. Use **Quiz Mode** for final prep
3. Export backup for reference

---

## 📁 File Locations

All data stored in `FlashcardApp/data/`:
- `flashcards.json` - Your flashcards (auto-created)
- `progress.json` - Study progress (auto-created)
- Put JSON import files here too!

Example structure:
```
FlashcardApp/
├── data/
│   ├── flashcards.json (auto-created)
│   ├── week13_template.json (pre-made template)
│   ├── week13_flashcards.json (your import)
│   └── week14_flashcards.json (next week)
└── ...
```

---

## ⚡ Common Tasks

### Import Week 13 Materials
```
Main Menu (4) → Import/Export (1) → week13_template.json
```

### Study Classification Metrics
```
Main Menu (1) → Start Study Session
→ Week 13 - Classification Metrics → Learn Mode
```

### Find Weak Cards
```
Main Menu (2) → Manage Flashcards (7) → View Weak Cards
```

### Backup Your Progress
```
Main Menu (4) → Import/Export (2) → backup.json
```

### Search for Cards
```
Main Menu (2) → Manage Flashcards (4) → "precision"
```

---

## 🎯 Study Mode Comparison

| Mode | Best For | Difficulty | Shows Answers |
|------|----------|-----------|---|
| **Learn** | First pass, understanding | ⭐ Easy | Before answering |
| **Practice** | Active recall | ⭐⭐ Medium | After attempt |
| **Quiz** | Self-assessment | ⭐⭐⭐ Hard | After answering |
| **Spaced Rep** | Review weak areas | ⭐⭐⭐ Hard | Optional |

---

## 📚 Example: Week 13 Workflow

### Day 1 - Introduction
```
Launch app → Import → week13_template.json
→ Start Study → Choose "Learn" mode
→ Study all 10 cards with answers shown
```

### Day 2 - Practice
```
Main Menu → Start Study → Choose "Practice" mode
→ 30s per card, try to answer before reveal
```

### Day 3 - Self-Test
```
Main Menu → Start Study → Choose "Quiz" mode
→ Answer without seeing answer first
→ Check statistics
```

### Day 4-7 - Review
```
Main Menu → Start Study → Choose "Spaced Repetition"
→ Focus on cards with accuracy < 70%
```

### Before Exam
```
Main Menu → View Statistics
→ Check weak cards
→ Final review in Quiz mode
```

---

## 🐛 Troubleshooting

### Application won't start
- Make sure you're in `FlashcardApp` directory
- Check Python 3.7+: `python --version`

### Can't import flashcards
- JSON file must be in `data/` folder
- Check JSON is valid (use online JSON validator)
- Verify required fields: "question", "answer"

### No flashcards showing up
- Make sure cards were imported first
- Check statistics to confirm: `Main Menu → 3`

### Accuracy shows as "Unreviewed"
- Study the card in any mode first
- Statistics update after studying

---

## 📖 Keyboard Tips

- **ENTER**: Confirm, proceed to next card
- **Ctrl+C**: Exit session (data saves automatically)
- Type answers naturally in Quiz mode

---

## 💾 Data Backup

### Automatic
- Application saves after every study session

### Manual Export
```
Main Menu → 4. Import/Export → 2. Export All Flashcards
→ Choose filename: backup_jan20.json
```

### Restore
```
Main Menu → 4. Import/Export → 1. Import Flashcards
→ Select backup_jan20.json
```

---

## 🎓 Study Tips

1. **Start with Learn Mode** - Get familiar with concepts
2. **Use Practice Mode** - Test active recall
3. **End with Quiz Mode** - Rigorous self-testing
4. **Track accuracy** - Aim for > 80% before moving on
5. **Review weak areas** - Use Spaced Repetition
6. **Study consistently** - Little and often beats cramming

---

## 📞 Need Help?

1. Check the full **README.md** for comprehensive documentation
2. Look at **data/week13_template.json** for format examples
3. Review error messages shown by the application
4. Check file permissions in `data/` and `logs/` folders

---

## 🚀 Next Steps

1. ✅ Understand the three ways to add cards
2. ✅ Import or add your first set of flashcards
3. ✅ Run a study session to see how it works
4. ✅ Check statistics to track progress
5. ✅ Add Week 13 materials using the template

**Happy studying!** 📚✨

---

**Version**: 1.0.0
**Created**: January 2026
