# Creating Import Files for Flashcard Application

## Overview

To add materials from a new week, create a JSON file with flashcard data and import it into the application.

## File Format

Create a `.json` file with an array of flashcard objects:

```json
[
    {
        "question": "Question text here?",
        "answer": "Answer text here",
        "category": "Week 14 - Topic Name",
        "difficulty": 3,
        "tags": ["tag1", "tag2"]
    },
    {
        "question": "Another question?",
        "answer": "Another answer",
        "category": "Week 14 - Topic Name",
        "difficulty": 2,
        "tags": ["concept"]
    }
]
```

## Field Descriptions

### Required Fields
- **question** (string): The question text
  - Can include markdown formatting
  - Should end with "?" for questions
  - Examples: "What is accuracy?", "Explain precision"

- **answer** (string): The answer text
  - Can be multiple lines (use `\n` for line breaks)
  - Can include formulas, code, or formatted text
  - Be concise but complete

### Optional Fields
- **category** (string, default: "General"): Organizational category
  - Recommended format: "Week X - Topic Name"
  - Examples: "Week 13 - Classification", "Week 14 - Regression"
  - Use consistent naming across weeks

- **difficulty** (integer 1-5, default: 3): Question difficulty
  - 1: Simple definitions
  - 2: Basic concepts
  - 3: Moderate (default)
  - 4: Complex relationships
  - 5: Advanced/synthesis

- **tags** (array of strings): Searchable tags
  - Use lowercase with underscores
  - Examples: ["classification", "metrics", "important"]
  - Helps organize and search cards

## Examples

### Simple Example
```json
[
    {
        "question": "What is the F1 score?",
        "answer": "The harmonic mean of precision and recall, combining both metrics into one value.",
        "category": "Week 13 - Classification",
        "difficulty": 2,
        "tags": ["f1_score"]
    }
]
```

### With Formula
```json
[
    {
        "question": "What is the formula for accuracy?",
        "answer": "Accuracy = (TP + TN) / (TP + TN + FP + FN)\n\nWhere: TP=True Positives, TN=True Negatives, FP=False Positives, FN=False Negatives",
        "category": "Week 13 - Classification",
        "difficulty": 2,
        "tags": ["accuracy", "formula"]
    }
]
```

### Complex Answer
```json
[
    {
        "question": "Explain the precision vs recall trade-off",
        "answer": "Precision and recall often have an inverse relationship:\n\n- High Precision, Low Recall: Few false positives, but miss many cases. Good for: spam filters\n- Low Precision, High Recall: Catch most cases, but many false alarms. Good for: disease screening\n- Balanced: Use F1 score to find middle ground\n\nThe choice depends on the cost of each error type in your application.",
        "category": "Week 13 - Classification",
        "difficulty": 4,
        "tags": ["precision", "recall", "tradeoff"]
    }
]
```

## How to Use These Files

### Step 1: Create the File
1. Open text editor (Notepad, VS Code, etc.)
2. Copy JSON template above
3. Add your flashcards
4. Save as `week14_flashcards.json` (or your week number)

### Step 2: Place File
- Save to: `FlashcardApp/data/` folder
- File should be in the same folder as other data files

### Step 3: Import in Application
```
Main Menu → 4. Import/Export → 1. Import Flashcards from File
→ Enter filename: week14_flashcards.json
```

## Tips for Creating Good Flashcards

### Question Design
✓ **Good**: "What is the formula for calculating accuracy?"
✗ **Bad**: "Formula?"

✓ **Good**: "Explain the difference between precision and recall"
✗ **Bad**: "Explain precision and recall"

### Answer Design
✓ **Good**: Concise but complete, includes key concepts
✗ **Bad**: Too long, rambling explanation

✓ **Good**: Use line breaks for complex answers
✗ **Bad**: Run-on paragraphs

### Tagging Strategy
```json
{
    "tags": ["week13", "classification", "metrics", "important"]
}
```
- Include week number
- Include topic area
- Include concept name
- Add importance tags

### Category Naming
- Consistent: `"Week 13 - Classification Metrics"`
- Not: `"Week 13"` or `"Classification"` (use as tags instead)
- Not: `"week_13_classification"` (use - separator)

## Converting Existing Notes

If you have notes you want to convert to flashcards:

### From Revision Guide
```
Key Concept: Accuracy
Definition: Proportion of correct predictions overall
Formula: (TP + TN) / (TP + TN + FP + FN)
Limitation: Misleading with imbalanced datasets
```

Becomes:
```json
{
    "question": "Define accuracy and state its main limitation",
    "answer": "Accuracy = (TP + TN) / (TP + TN + FP + FN)\n\nMeasures proportion of correct predictions overall.\n\nLimitation: Misleading with imbalanced datasets - if one class dominates, high accuracy is easy to achieve without good performance on minority class.",
    "category": "Week 13 - Classification",
    "difficulty": 2,
    "tags": ["accuracy", "classification", "limitation"]
}
```

## Validating Your JSON

Before importing, validate your JSON:

1. **Online validator**: Copy content to https://jsonlint.com/
2. **Common errors**:
   - Missing commas between objects: `}, {`
   - Extra commas after last item: `"tags": ["a", "b",]` ❌
   - Unescaped quotes in strings: use `\"` or use single quotes
   - Missing quotes around keys: `"question":` ✓

3. **Check format**:
   - Must start with `[`
   - Must end with `]`
   - Each item wrapped in `{}`
   - Commas between items

## Creating from Scratch

### Minimal File
```json
[
    {
        "question": "Question 1?",
        "answer": "Answer 1"
    },
    {
        "question": "Question 2?",
        "answer": "Answer 2"
    }
]
```

### Full-Featured File
```json
[
    {
        "question": "What is machine learning?",
        "answer": "Machine learning is a subset of AI where systems learn from data without being explicitly programmed. Key types: supervised, unsupervised, reinforcement learning.",
        "category": "Week 14 - Machine Learning",
        "difficulty": 2,
        "tags": ["ml", "ai", "fundamentals", "definitions"]
    },
    {
        "question": "What is the bias-variance tradeoff?",
        "answer": "The bias-variance tradeoff describes the balance between:\n\nBias: Error from oversimplified model (underfitting)\nVariance: Error from overly complex model (overfitting)\n\nGoal: Find optimal complexity minimizing total error (bias² + variance + noise)",
        "category": "Week 14 - Model Evaluation",
        "difficulty": 4,
        "tags": ["bias_variance", "model_selection", "advanced"]
    }
]
```

## Batch Operations

### Combining Multiple Files
If you have multiple source files:

1. Create separate files for different topics
2. Import each one separately in the app
3. Use categories and tags to organize

### Backing Up Your Import Files
Keep copies of JSON files in version control:
```
FlashcardApp/
├── data/
│   ├── week13_flashcards.json (your import)
│   ├── week14_flashcards.json (your import)
│   └── flashcards.json (auto-generated database)
```

## Special Characters

For special characters in answers:

| Character | Escape | Example |
|-----------|--------|---------|
| Quote | `\"` | `"The term \"accuracy\" means..."` |
| Newline | `\n` | `"Line 1\nLine 2"` |
| Backslash | `\\` | `"Path: C:\\Users"` |

### Example with Math
```json
{
    "question": "What is the formula for MSE?",
    "answer": "MSE = (1/n) × Σ(y_i - ŷ_i)²\n\nWhere:\n- y_i = actual value\n- ŷ_i = predicted value\n- n = number of observations"
}
```

## Troubleshooting

### "Invalid format" Error
- Check JSON syntax using jsonlint.com
- Ensure file is valid JSON array `[...]`
- Verify all required fields present

### Cards not appearing after import
- Check file location: `FlashcardApp/data/`
- Verify JSON format
- Check import message for error details

### Special characters causing issues
- Ensure file is saved as UTF-8
- Escape special characters: `\"` for quotes
- Avoid non-ASCII characters if possible

## Resources

- **JSON Format**: https://www.json.org/
- **JSON Validator**: https://jsonlint.com/
- **JSON Tutorial**: https://www.w3schools.com/js/js_json_intro.asp

---

**Next**: Create your first import file and add cards to the application!
