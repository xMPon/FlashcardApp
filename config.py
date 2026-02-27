"""
Configuration settings for Flashcard Application
"""

import os
from pathlib import Path

# Application paths
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
LOGS_DIR = APP_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Data files
FLASHCARDS_DB = DATA_DIR / "flashcards.json"
PROGRESS_DB = DATA_DIR / "progress.json"
STATS_LOG = LOGS_DIR / "study_stats.log"

# Flashcard settings
DEFAULT_DIFFICULTY = 3  # 1-5 scale
SPACED_REPETITION_INTERVALS = {
    1: 1,      # 1 day
    2: 3,      # 3 days
    3: 7,      # 1 week
    4: 14,     # 2 weeks
    5: 30      # 1 month
}

# Study modes
STUDY_MODES = {
    'learn': 'Learn mode - Study all cards',
    'practice': 'Practice mode - Timed cards',
    'quiz': 'Quiz mode - Test yourself',
    'spaced': 'Spaced Repetition - Smart review'
}

# CLI colors (for better UX)
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Disable colors on Windows CMD
if os.name == 'nt':
    class Colors:
        HEADER = ''
        OKBLUE = ''
        OKCYAN = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''
