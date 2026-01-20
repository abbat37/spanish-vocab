# Testing Guide

## Overview
Comprehensive test suite for the Spanish Vocabulary Learning App using pytest.

## Test Coverage

### ✅ 17 Tests - All Passing

#### 1. Route Tests (4 tests)
- **test_home_page_loads**: Verifies home page loads successfully (200 status)
- **test_home_page_has_form**: Checks form elements are present (theme selector, word type selector, submit button)
- **test_generate_sentences_post**: Tests POST request generates sentences correctly
- **test_invalid_theme**: Ensures app handles invalid themes gracefully without crashing

#### 2. Sentence Generation Tests (6 tests)
- **test_generate_sentences_returns_list**: Verifies function returns a list
- **test_generate_sentences_count**: Checks correct number of sentences (1-5)
- **test_generate_sentences_structure**: Validates sentence object structure (spanish, english, word_id, is_learned)
- **test_generate_sentences_has_highlighted_words**: Confirms words are highlighted with `<mark>` tags
- **test_generate_sentences_invalid_theme**: Handles invalid theme gracefully (returns empty list)
- **test_generate_sentences_invalid_word_type**: Handles invalid word type gracefully (returns empty list)

#### 3. Progress Tracking Tests (5 tests)
- **test_record_word_practice**: Verifies word practice is recorded in database
- **test_record_word_practice_no_duplicates**: Ensures duplicate practices aren't recorded
- **test_get_user_stats_empty**: Tests stats for new user (all zeros)
- **test_get_user_stats_with_practice**: Validates stats calculation with practice data
- **test_mark_learned_api**: Tests API endpoint for marking words as learned

#### 4. Database Tests (2 tests)
- **test_vocabulary_word_creation**: Verifies vocabulary words can be created and saved
- **test_sentence_template_creation**: Verifies sentence templates can be created and saved

---

## Running Tests

### Run All Tests
```bash
python3 -m pytest tests/ -v
```

### Run Specific Test File
```bash
python3 -m pytest tests/test_app.py -v
```

### Run Specific Test
```bash
python3 -m pytest tests/test_app.py::TestRoutes::test_home_page_loads -v
```

### Run with Coverage Report
```bash
python3 -m pytest tests/ --cov=app --cov=database --cov-report=html
```

---

## Test Setup

### Test Database
- Uses in-memory SQLite database (`sqlite:///:memory:`)
- Database is created fresh for each test
- Test data is seeded automatically
- Database is cleaned up after each test

### Test Data
The test suite includes:
- **5 vocabulary words** (cooking, work, sports themes)
- **5 sentence templates** for different themes and word types

### Test Client
- Flask test client with `TESTING=True`
- Session management enabled
- Isolated from production database

---

## What's Being Tested

### Core Functionality
✅ Page loading and rendering
✅ Form submission and validation
✅ Sentence generation logic
✅ Word highlighting
✅ Error handling (invalid inputs)

### Database Operations
✅ Creating vocabulary words
✅ Creating sentence templates
✅ Recording practice sessions
✅ Preventing duplicate records
✅ Querying and filtering

### Progress Tracking
✅ Session tracking
✅ Practice recording
✅ Statistics calculation
✅ Marking words as learned
✅ API endpoints

### Edge Cases
✅ Invalid theme/word type combinations
✅ Empty database queries
✅ New user with no data
✅ Duplicate practice attempts

---

## Adding New Tests

### Example Test Structure
```python
def test_new_feature(client):
    """Test description"""
    with app.app_context():
        # Setup
        # ... your setup code ...

        # Execute
        result = your_function()

        # Assert
        assert result == expected_value
```

### Test Naming Convention
- Use descriptive names: `test_feature_behavior`
- Group related tests in classes
- One assertion per test (when possible)

---

## Continuous Integration

These tests can be easily integrated into CI/CD pipelines:

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v
```

---

## Test Results Summary

```
============================= test session starts ==============================
collected 17 items

tests/test_app.py::TestRoutes::test_home_page_loads PASSED               [  5%]
tests/test_app.py::TestRoutes::test_home_page_has_form PASSED            [ 11%]
tests/test_app.py::TestRoutes::test_generate_sentences_post PASSED       [ 17%]
tests/test_app.py::TestRoutes::test_invalid_theme PASSED                 [ 23%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_returns_list PASSED [ 29%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_count PASSED [ 35%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_structure PASSED [ 41%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_has_highlighted_words PASSED [ 47%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_invalid_theme PASSED [ 52%]
tests/test_app.py::TestGenerateSentences::test_generate_sentences_invalid_word_type PASSED [ 58%]
tests/test_app.py::TestProgressTracking::test_record_word_practice PASSED [ 64%]
tests/test_app.py::TestProgressTracking::test_record_word_practice_no_duplicates PASSED [ 70%]
tests/test_app.py::TestProgressTracking::test_get_user_stats_empty PASSED [ 76%]
tests/test_app.py::TestProgressTracking::test_get_user_stats_with_practice PASSED [ 82%]
tests/test_app.py::TestProgressTracking::test_mark_learned_api PASSED    [ 88%]
tests/test_app.py::TestDatabase::test_vocabulary_word_creation PASSED    [ 94%]
tests/test_app.py::TestDatabase::test_sentence_template_creation PASSED  [100%]

============================== 17 passed in 2.01s ==============================
```

✅ **All tests passing!**

---

## Benefits of This Test Suite

1. **Catches Bugs Early**: Automated tests catch issues before deployment
2. **Safe Refactoring**: Confidence to change code without breaking functionality
3. **Documentation**: Tests serve as executable documentation
4. **Quality Assurance**: Ensures all features work as expected
5. **CI/CD Ready**: Can be integrated into deployment pipelines

---

## Next Steps

- Add more edge case tests
- Add performance tests
- Add integration tests for deployment
- Set up test coverage reporting
- Add tests for new features as they're developed
