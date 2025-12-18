# Testing Guide for NephroList PDF App

## Quick Start

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage report.

### Run Specific Test Files

```bash
# Unit tests only
pytest tests/unit/

# Specific test file
pytest tests/unit/test_data_validation.py

# Specific test function
pytest tests/unit/test_csv_export.py::TestCSVExport::test_csv_utf8_encoding
```

### Run Tests in Parallel

```bash
pytest -n auto
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (isolated components)
│   ├── test_data_validation.py
│   ├── test_csv_export.py
│   └── test_dataframe_creation.py
├── integration/             # Integration tests (component interaction)
│   └── test_streamlit_app.py
└── fixtures/                # Test data files
    └── (PDF samples will go here)
```

## Current Test Status

⚠️ **Note**: The test infrastructure is set up, but many tests are currently **skipped** because:

1. The main application code needs to be refactored into testable functions
2. PDF parsing functionality is not yet implemented (currently uses mock data)
3. Streamlit testing framework integration is pending

## What's Currently Testable

The example tests demonstrate:

✅ **Data Validation** - How to test clinical data validation
✅ **CSV Export** - How to test DataFrame to CSV conversion
✅ **DataFrame Creation** - How to test data structure creation
✅ **Edge Cases** - How to test error conditions and special cases

## Next Steps to Enable Testing

### 1. Refactor Application Code

Extract functions from `Baixar app_nephrolist_pdf.py`:

```python
# Create new file: nephrolist_core.py

def extract_data_from_pdf(pdf_file) -> dict:
    """Extract clinical data from PDF file."""
    # TODO: Implement real PDF parsing
    pass

def validate_clinical_data(data: dict) -> tuple[bool, list[str]]:
    """Validate extracted data."""
    # Implement validation logic
    pass

def create_clinical_dataframe(data: dict) -> pd.DataFrame:
    """Create DataFrame from clinical data."""
    return pd.DataFrame([data])

def export_to_csv(df: pd.DataFrame) -> bytes:
    """Export DataFrame to CSV bytes."""
    return df.to_csv(index=False).encode('utf-8')
```

Then update `Baixar app_nephrolist_pdf.py` to use these functions:

```python
import streamlit as st
from nephrolist_core import (
    extract_data_from_pdf,
    validate_clinical_data,
    create_clinical_dataframe,
    export_to_csv
)

# ... Streamlit UI code using the functions
```

### 2. Implement PDF Parsing

Replace the mock data (lines 14-30) with real PDF parsing:

```python
from pdfplumber import open as open_pdf

def extract_data_from_pdf(pdf_file) -> dict:
    with open_pdf(pdf_file) as pdf:
        # Extract text from PDF
        text = "\n".join(page.extract_text() for page in pdf.pages)

        # Parse text to extract fields
        data = parse_clinical_text(text)
        return data
```

### 3. Add Test Fixtures

Create sample PDF files in `tests/fixtures/`:

- `sample_valid.pdf` - Valid clinical evolution document
- `sample_missing_fields.pdf` - Document with some missing data
- `sample_malformed.pdf` - Corrupted or invalid PDF
- `sample_multipage.pdf` - Multi-page document

### 4. Update Tests to Use Real Functions

Once functions are extracted, update tests:

```python
# Before (current):
def test_validate_required_fields_present(self, sample_clinical_data):
    required_fields = ["Nome", "Setor", ...]
    for field in required_fields:
        assert field in sample_clinical_data

# After (with real validation):
from nephrolist_core import validate_clinical_data

def test_validate_required_fields_present(self, sample_clinical_data):
    is_valid, errors = validate_clinical_data(sample_clinical_data)
    assert is_valid
    assert len(errors) == 0
```

### 5. Enable Integration Tests

Install Streamlit testing tools and update integration tests:

```python
from streamlit.testing.v1 import AppTest

def test_app_loads_without_errors():
    at = AppTest.from_file("Baixar app_nephrolist_pdf.py")
    at.run()
    assert not at.exception
```

## Coverage Goals

| Component | Current | Target |
|-----------|---------|--------|
| Data Validation | 0% | 100% |
| CSV Export | 0% | 100% |
| PDF Extraction | 0% | 90% |
| Error Handling | 0% | 85% |
| UI Components | 0% | 70% |
| **Overall** | **0%** | **85%** |

## Writing New Tests

### Test Naming Convention

- Test files: `test_<feature>.py`
- Test classes: `Test<Feature>`
- Test functions: `test_<specific_behavior>`

### Example Test

```python
def test_validate_age_is_numeric(self, sample_clinical_data):
    """Test that age field contains a valid number."""
    age = sample_clinical_data["Idade"]
    assert age.isdigit(), f"Age should be numeric, got: {age}"
    assert 0 <= int(age) <= 150, f"Age should be reasonable, got: {age}"
```

### Using Fixtures

```python
def test_csv_export_basic(self, sample_dataframe):
    """sample_dataframe is defined in conftest.py"""
    csv_output = sample_dataframe.to_csv(index=False)
    assert csv_output is not None
```

### Parametrized Tests

```python
@pytest.mark.parametrize("invalid_date", [
    "2025-13-01",  # Invalid month
    "2025-06-32",  # Invalid day
    "invalid",     # Not a date
])
def test_reject_invalid_dates(self, invalid_date):
    with pytest.raises(ValueError):
        datetime.strptime(invalid_date, "%Y-%m-%d")
```

## Continuous Integration

To run tests automatically on every commit, add to `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. You're in the correct directory
2. Virtual environment is activated
3. Dependencies are installed: `pip install -r requirements-dev.txt`

### Coverage Not Showing

Make sure you're running with coverage:
```bash
pytest --cov=. --cov-report=term-missing
```

### Tests Skipped

Many tests are currently skipped intentionally. Remove `@pytest.mark.skip` after implementing the required functionality.

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Streamlit Testing Guide](https://docs.streamlit.io/develop/api-reference/app-testing)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

For more details on what to test, see `TEST_COVERAGE_ANALYSIS.md`.
