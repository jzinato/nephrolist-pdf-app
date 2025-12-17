"""
Unit tests for DataFrame creation from extracted clinical data.

These tests verify that clinical data dictionaries are properly converted to DataFrames.
"""
import pytest
import pandas as pd


class TestDataFrameCreation:
    """Test suite for DataFrame creation."""

    def test_create_dataframe_from_dict(self, sample_clinical_data):
        """Test basic DataFrame creation from clinical data dictionary."""
        df = pd.DataFrame([sample_clinical_data])

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert len(df.columns) == len(sample_clinical_data)

    def test_dataframe_has_correct_columns(self, sample_clinical_data):
        """Test that DataFrame has all expected columns."""
        df = pd.DataFrame([sample_clinical_data])

        expected_columns = list(sample_clinical_data.keys())
        actual_columns = list(df.columns)

        assert actual_columns == expected_columns

    def test_dataframe_has_correct_values(self, sample_clinical_data):
        """Test that DataFrame contains correct values."""
        df = pd.DataFrame([sample_clinical_data])

        for column, expected_value in sample_clinical_data.items():
            actual_value = df.loc[0, column]
            assert actual_value == expected_value, \
                f"Column {column}: expected {expected_value}, got {actual_value}"

    def test_dataframe_column_order_preserved(self, sample_clinical_data):
        """Test that column order is preserved from input dictionary."""
        # Python 3.7+ preserves dict order
        df = pd.DataFrame([sample_clinical_data])

        expected_order = list(sample_clinical_data.keys())
        actual_order = list(df.columns)

        assert actual_order == expected_order

    def test_dataframe_single_row(self, sample_clinical_data):
        """Test that DataFrame created from single record has one row."""
        df = pd.DataFrame([sample_clinical_data])

        assert len(df) == 1
        assert df.shape[0] == 1

    def test_dataframe_with_missing_fields(self, sample_clinical_data_missing_fields):
        """Test DataFrame creation with missing optional fields."""
        df = pd.DataFrame([sample_clinical_data_missing_fields])

        assert isinstance(df, pd.DataFrame)
        # Should still create DataFrame even with missing fields
        assert len(df) == 1

    def test_dataframe_handles_empty_strings(self):
        """Test that DataFrame handles empty string values."""
        data = {
            "Nome": "João Silva",
            "Peso": "",
            "Observacoes": ""
        }
        df = pd.DataFrame([data])

        assert df.loc[0, "Peso"] == ""
        assert df.loc[0, "Observacoes"] == ""

    def test_dataframe_all_string_types(self, sample_clinical_data):
        """Test that all DataFrame values are strings (as in original app)."""
        df = pd.DataFrame([sample_clinical_data])

        for column in df.columns:
            value = df.loc[0, column]
            assert isinstance(value, str), \
                f"Column {column} should be string, got {type(value)}"

    def test_dataframe_multiple_records(self, sample_clinical_data):
        """Test DataFrame creation with multiple patient records."""
        # Simulate multiple patients
        data = [sample_clinical_data] * 3
        df = pd.DataFrame(data)

        assert len(df) == 3
        assert df.shape[0] == 3
        # All rows should have same values (since we duplicated)
        assert all(df["Nome"] == "Vera Ondina Marcos")

    def test_dataframe_special_characters(self):
        """Test DataFrame handles Portuguese special characters."""
        data = {
            "Nome": "José María Gonçalves",
            "Diagnostico": "Situação crítica: infecção",
            "Plano": "Prescrição de medicação"
        }
        df = pd.DataFrame([data])

        assert df.loc[0, "Nome"] == "José María Gonçalves"
        assert "ç" in df.loc[0, "Diagnostico"]
        assert "ã" in df.loc[0, "Plano"]

    def test_dataframe_index_starts_at_zero(self, sample_clinical_data):
        """Test that DataFrame index starts at 0."""
        df = pd.DataFrame([sample_clinical_data])

        assert df.index[0] == 0

    def test_dataframe_preserves_whitespace(self):
        """Test that DataFrame preserves whitespace in values."""
        data = {
            "Nome": "João  Silva",  # Double space
            "Plano": "  Prescrição com espaços  "  # Leading/trailing spaces
        }
        df = pd.DataFrame([data])

        # Pandas preserves whitespace
        assert "  " in df.loc[0, "Nome"]

    def test_dataframe_memory_efficiency(self, sample_clinical_data):
        """Test DataFrame memory usage is reasonable."""
        df = pd.DataFrame([sample_clinical_data])

        # Memory usage should be reasonable for small dataset
        memory_bytes = df.memory_usage(deep=True).sum()
        assert memory_bytes < 10000  # Less than 10KB for single record
