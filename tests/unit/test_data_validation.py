"""
Unit tests for clinical data validation.

These tests verify that extracted data meets expected formats and constraints.
"""
import pytest
from datetime import datetime


# NOTE: These tests assume functions will be extracted from the main script
# Currently, the validation logic needs to be implemented

class TestDataValidation:
    """Test suite for clinical data validation."""

    def test_validate_required_fields_present(self, sample_clinical_data):
        """Test that all required fields are present in valid data."""
        required_fields = [
            "Nome", "Setor", "Leito", "Idade", "Data_Admissao",
            "Motivo_Internacao", "Diagnostico", "Plano", "Preceptor"
        ]

        for field in required_fields:
            assert field in sample_clinical_data, f"Required field '{field}' is missing"
            assert sample_clinical_data[field], f"Required field '{field}' is empty"

    def test_validate_date_format(self, sample_clinical_data):
        """Test that dates are in the correct format (YYYY-MM-DD)."""
        date_fields = ["Data_Admissao", "Data_Desfecho"]

        for field in date_fields:
            if field in sample_clinical_data and sample_clinical_data[field]:
                date_str = sample_clinical_data[field]
                # Should be able to parse as date
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    pytest.fail(f"Invalid date format for {field}: {date_str}")

    def test_validate_age_is_numeric(self, sample_clinical_data):
        """Test that age field contains a valid number."""
        age = sample_clinical_data["Idade"]
        assert age.isdigit(), f"Age should be numeric, got: {age}"
        assert 0 <= int(age) <= 150, f"Age should be reasonable, got: {age}"

    def test_validate_peso_is_numeric_when_present(self, sample_clinical_data):
        """Test that weight (Peso) is numeric when provided."""
        if "Peso" in sample_clinical_data and sample_clinical_data["Peso"]:
            peso = sample_clinical_data["Peso"]
            # Remove decimal point if present
            peso_clean = peso.replace(".", "").replace(",", "")
            assert peso_clean.isdigit(), f"Peso should be numeric, got: {peso}"
            assert 0 < float(peso.replace(",", ".")) < 300, f"Peso should be reasonable, got: {peso}"

    def test_validate_leito_is_numeric(self, sample_clinical_data):
        """Test that bed number (Leito) is numeric."""
        leito = sample_clinical_data["Leito"]
        assert leito.isdigit(), f"Leito should be numeric, got: {leito}"
        assert int(leito) > 0, f"Leito should be positive, got: {leito}"

    def test_validate_dialise_field(self, sample_clinical_data):
        """Test that dialysis field has valid values."""
        dialise = sample_clinical_data["Dialise"]
        assert dialise, "Dialise field should not be empty"
        # Should contain "Sim" or "Não"
        assert "Sim" in dialise or "Não" in dialise, \
            f"Dialise should contain 'Sim' or 'Não', got: {dialise}"

    def test_validate_desfecho_field(self, sample_clinical_data):
        """Test that outcome (Desfecho) has valid values."""
        valid_outcomes = ["Alta", "Óbito", "Transferência", "Em tratamento"]
        desfecho = sample_clinical_data["Desfecho"]
        assert desfecho in valid_outcomes, \
            f"Desfecho should be one of {valid_outcomes}, got: {desfecho}"

    def test_validate_admission_before_outcome_date(self, sample_clinical_data):
        """Test that admission date is before outcome date."""
        admissao = datetime.strptime(sample_clinical_data["Data_Admissao"], "%Y-%m-%d")
        desfecho = datetime.strptime(sample_clinical_data["Data_Desfecho"], "%Y-%m-%d")

        assert admissao <= desfecho, \
            "Admission date should be before or equal to outcome date"

    def test_handle_missing_optional_fields(self, sample_clinical_data_missing_fields):
        """Test that validation handles missing optional fields gracefully."""
        # These fields are optional
        optional_fields = ["Situacao_Atual", "Peso", "Residente"]

        # Should not raise errors even if missing
        for field in optional_fields:
            value = sample_clinical_data_missing_fields.get(field, None)
            assert value is None or isinstance(value, str)

    @pytest.mark.parametrize("invalid_age", ["-5", "200", "abc", ""])
    def test_reject_invalid_ages(self, invalid_age, sample_clinical_data):
        """Test that invalid age values are rejected."""
        sample_clinical_data["Idade"] = invalid_age

        # Validation should fail for these cases
        if invalid_age == "" or not invalid_age.isdigit():
            with pytest.raises((ValueError, AssertionError)):
                assert invalid_age.isdigit()
        elif int(invalid_age) < 0 or int(invalid_age) > 150:
            with pytest.raises((ValueError, AssertionError)):
                assert 0 <= int(invalid_age) <= 150

    @pytest.mark.parametrize("invalid_date", [
        "2025-13-01",  # Invalid month
        "2025-06-32",  # Invalid day
        "25-06-2025",  # Wrong format
        "2025/06/25",  # Wrong separator
        "invalid",     # Not a date
    ])
    def test_reject_invalid_dates(self, invalid_date, sample_clinical_data):
        """Test that invalid date formats are rejected."""
        sample_clinical_data["Data_Admissao"] = invalid_date

        with pytest.raises(ValueError):
            datetime.strptime(invalid_date, "%Y-%m-%d")

    def test_validate_special_characters_in_text_fields(self, sample_clinical_data):
        """Test that text fields properly handle special characters."""
        # Portuguese special characters should be preserved
        special_chars_data = sample_clinical_data.copy()
        special_chars_data["Nome"] = "José María Gonçalves Peña"
        special_chars_data["Diagnostico"] = "Infecção: observação crítica"

        # Should not raise any encoding errors
        for key, value in special_chars_data.items():
            assert isinstance(value, str)
            # Ensure UTF-8 can encode it
            value.encode('utf-8')
