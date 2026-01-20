# Test Debugging Guide

## Understanding Test Failures

When tests fail, pytest provides detailed information to help you debug. This guide shows common failure types and how to fix them.

---

## Coverage Reporting

### Current Coverage: 92%
- **app.py**: 95% coverage (91 statements, 5 missed)
- **database.py**: 87% coverage (54 statements, 7 missed)

### Viewing Coverage Reports

**Terminal Report:**
```bash
python3 -m pytest tests/ --cov=app --cov=database --cov-report=term-missing
```

**HTML Report (Interactive):**
```bash
python3 -m pytest tests/ --cov=app --cov=database --cov-report=html
open htmlcov/index.html  # Opens in browser
```

The HTML report shows:
- Line-by-line coverage (green = covered, red = missed)
- Which functions/branches aren't tested
- Exact lines that need test coverage

---

## Common Test Failure Types

### 1. Assertion Error - Wrong Expected Value

**Example Failure:**
```
AssertionError: Expected 10 sentences but got 2
assert 2 == 10
```

**What This Means:**
- Your test expected one value, but got something different
- The actual behavior doesn't match your expectation

**How to Debug:**
1. Read the assertion message carefully
2. Check if your expectation is correct
3. Verify the actual value makes sense
4. Update either the code or the test

**Fix:**
```python
# Before (failing):
assert len(sentences) == 10

# After (passing):
assert len(sentences) <= 2  # Based on test data
```

---

### 2. Type Mismatch

**Example Failure:**
```
AssertionError: Expected dict but got <class 'list'>
assert False
```

**What This Means:**
- You're checking for the wrong data type
- The function returns a different type than expected

**How to Debug:**
1. Check the function's return type
2. Look at the actual data structure
3. Update your type check or fix the function

**Fix:**
```python
# Before (failing):
assert isinstance(sentences, dict)

# After (passing):
assert isinstance(sentences, list)
```

---

### 3. KeyError - Missing Dictionary Key

**Example Failure:**
```
KeyError: 'spanish_text'
```

**What This Means:**
- You're trying to access a dictionary key that doesn't exist
- Common cause: typo in key name

**How to Debug:**
1. Print the dictionary keys: `print(sentences[0].keys())`
2. Check for typos
3. Verify the data structure is what you expect

**Fix:**
```python
# Before (failing):
spanish_text = sentences[0]['spanish_text']

# After (passing):
spanish_text = sentences[0]['spanish']  # Correct key name
```

---

### 4. Content Mismatch

**Example Failure:**
```
AssertionError: Expected 'freír' in sentence
assert 'freír' in 'Me gusta <mark>hornear</mark>.'
```

**What This Means:**
- You're checking for specific content that's not there
- Often happens with random or dynamic data

**How to Debug:**
1. Don't test for specific random values
2. Test for patterns or structure instead
3. Make assertions more flexible

**Fix:**
```python
# Before (failing - too specific):
assert 'freír' in sentences[0]['spanish']

# After (passing - checks pattern):
assert '<mark>' in sentences[0]['spanish']  # Any highlighted word
```

---

### 5. HTTP Status Code Mismatch

**Example Failure:**
```
AssertionError: Expected 404 but got 400
assert 400 == 404
```

**What This Means:**
- API returned a different status code than expected
- 400 = Bad Request, 404 = Not Found

**How to Debug:**
1. Understand HTTP status codes
2. Check what the endpoint actually returns
3. Verify your test matches the actual behavior

**Fix:**
```python
# Before (failing):
assert response.status_code == 404  # Wrong code

# After (passing):
assert response.status_code == 400  # Correct for bad request
```

---

## Debugging Workflow

### Step 1: Read the Error Message
```
FAILED tests/test_app.py::test_name - AssertionError: Expected...
```
- Which test failed?
- What was the error type?
- What was expected vs actual?

### Step 2: Look at the Traceback
```python
tests/test_failures.py:65: AssertionError
E  assert 2 == 10
```
- Which line failed?
- What values were compared?

### Step 3: Reproduce Locally
Run just that test:
```bash
python3 -m pytest tests/test_file.py::test_name -v
```

### Step 4: Add Debug Output
```python
def test_something(client):
    result = my_function()
    print(f"DEBUG: result = {result}")  # Add debugging
    print(f"DEBUG: type = {type(result)}")
    assert result == expected
```

Run with output visible:
```bash
python3 -m pytest tests/test_file.py::test_name -v -s
```
The `-s` flag shows print statements!

### Step 5: Fix the Issue
Options:
1. **Fix the test**: Your assertion was wrong
2. **Fix the code**: The function has a bug
3. **Fix both**: Test and code both had issues

---

## Useful Pytest Commands

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test file
python3 -m pytest tests/test_app.py -v

# Run specific test
python3 -m pytest tests/test_app.py::TestClass::test_method -v

# Show print statements
python3 -m pytest tests/ -v -s

# Stop on first failure
python3 -m pytest tests/ -x

# Run tests matching a keyword
python3 -m pytest tests/ -k "progress" -v

# Show local variables on failure
python3 -m pytest tests/ -l

# Run with coverage
python3 -m pytest tests/ --cov=app --cov=database --cov-report=html

# Run in parallel (faster, needs pytest-xdist)
python3 -m pytest tests/ -n auto
```

---

## Reading Test Output

### Successful Test
```
tests/test_app.py::test_home_page_loads PASSED [100%]
```
✅ Green dot, PASSED status

### Failed Test
```
tests/test_app.py::test_wrong_thing FAILED [50%]

=================================== FAILURES ===================================
__________________ test_wrong_thing __________________

def test_wrong_thing():
>       assert 1 == 2
E       assert 1 == 2

tests/test_app.py:10: AssertionError
```

**Key Parts:**
1. **Test name**: `test_wrong_thing`
2. **Location**: `tests/test_app.py:10`
3. **Failure line**: `>` indicates where it failed
4. **Error type**: `AssertionError`
5. **Details**: `E` lines show what went wrong

---

## Best Practices

### ✅ DO:
- Write clear, descriptive test names
- Test one thing per test
- Use clear assertion messages
- Keep tests independent
- Use fixtures for common setup
- Test edge cases

### ❌ DON'T:
- Test implementation details
- Have tests depend on each other
- Test random data with exact values
- Write overly complex tests
- Ignore failing tests
- Test third-party libraries

---

## Example Debugging Session

**Scenario**: Test fails with "AssertionError: Expected 5 but got 2"

**Step 1 - Identify:**
```bash
$ python3 -m pytest tests/test_app.py::test_sentence_count -v
FAILED tests/test_app.py::test_sentence_count - AssertionError: Expected 5 but got 2
```

**Step 2 - Add Debug Output:**
```python
def test_sentence_count(client):
    sentences = generate_sentences('cooking', 'verb')
    print(f"\nDEBUG: Got {len(sentences)} sentences")
    print(f"DEBUG: Sentences: {sentences}")
    assert len(sentences) == 5
```

**Step 3 - Run with Output:**
```bash
$ python3 -m pytest tests/test_app.py::test_sentence_count -v -s

DEBUG: Got 2 sentences
DEBUG: Sentences: [{'spanish': '...', ...}, {'spanish': '...', ...}]
```

**Step 4 - Analyze:**
"Oh! The test data only has 2 words, so we can only generate 2 sentences!"

**Step 5 - Fix:**
```python
def test_sentence_count(client):
    sentences = generate_sentences('cooking', 'verb')
    # Fixed: expect number based on test data
    assert len(sentences) <= 5  # Maximum 5
    assert len(sentences) > 0    # At least 1
```

**Step 6 - Verify:**
```bash
$ python3 -m pytest tests/test_app.py::test_sentence_count -v
PASSED ✓
```

---

## Understanding Coverage

### What is Code Coverage?
Percentage of code lines executed during tests.

**Coverage Report:**
```
Name          Stmts   Miss  Cover   Missing
-------------------------------------------
app.py           91      5    95%   89, 122, 177, 194, 198
database.py      54      7    87%   21, 25, 46, 50, 69, 88, 92
-------------------------------------------
TOTAL           145     12    92%
```

**What This Means:**
- **Stmts**: Total lines of code
- **Miss**: Lines not executed by tests
- **Cover**: Percentage covered
- **Missing**: Specific line numbers not tested

### Good Coverage Goals
- **80%+**: Good baseline
- **90%+**: Excellent
- **100%**: Ideal but not always necessary

### Lines to Focus On
Check the `Missing` column - these lines aren't tested:
- `app.py:89` - What does this line do?
- `app.py:122` - Is this an error handler?
- Add tests to cover these lines

---

## Tools & Resources

**Installed Packages:**
```
pytest==8.4.2          # Test framework
pytest-cov==7.0.0      # Coverage reporting
```

**VS Code Extensions:**
- Python Test Explorer
- Coverage Gutters (shows coverage in editor)

**Documentation:**
- pytest: https://docs.pytest.org/
- Coverage.py: https://coverage.readthedocs.io/

---

## Quick Reference Card

| Problem | Command | Purpose |
|---------|---------|---------|
| Run all tests | `pytest tests/ -v` | Verbose output |
| One test | `pytest tests/file.py::test_name -v` | Single test |
| See prints | `pytest -v -s` | Show stdout |
| Stop on fail | `pytest -x` | Exit on first failure |
| Coverage | `pytest --cov=app --cov-report=html` | HTML report |
| Keyword match | `pytest -k "api"` | Tests with "api" |
| Show locals | `pytest -l` | Variable values |

---

## Practice Exercise

Try breaking and fixing a test yourself!

1. Edit `tests/test_app.py`
2. Change an assertion to something wrong
3. Run the test and see it fail
4. Read the error message carefully
5. Fix the assertion
6. Watch it pass!

**Example:**
```python
# Break it:
assert response.status_code == 999  # Wrong!

# Run it:
$ pytest tests/test_app.py::test_home_page_loads -v
# See it fail!

# Fix it:
assert response.status_code == 200  # Correct!

# Run it again:
$ pytest tests/test_app.py::test_home_page_loads -v
# See it pass!
```

---

**Remember**: Failing tests are **good**! They catch bugs before users do. 🐛✅
