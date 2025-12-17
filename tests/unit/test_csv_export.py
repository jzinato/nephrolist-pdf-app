"""
Unit tests for CSV export functionality.

These tests verify that DataFrame to CSV conversion works correctly.
"""
import pytest
import pandas as pd
from io import StringIO


class TestCSVExport:
    """Test suite for CSV export functionality."""

    def test_csv_export_basic(self, sample_dataframe):
        """Test basic CSV export functionality."""
        csv_output = sample_dataframe.to_csv(index=False)

        assert csv_output is not None
        assert len(csv_output) > 0
        assert "Nome,Setor,Leito" in csv_output

    def test_csv_contains_all_columns(self, sample_dataframe):
        """Test that CSV contains all expected columns."""
        csv_output = sample_dataframe.to_csv(index=False)

        expected_columns = [
            "Nome", "Setor", "Leito", "Idade", "Data_Admissao",
            "Motivo_Internacao", "Diagnostico", "Situacao_Atual",
            "Dialise", "Peso", "Plano", "Preceptor", "Residente",
            "Desfecho", "Data_Desfecho"
        ]

        for column in expected_columns:
            assert column in csv_output, f"Column '{column}' missing from CSV"

    def test_csv_contains_data_values(self, sample_dataframe):
        """Test that CSV contains the actual data values."""
        csv_output = sample_dataframe.to_csv(index=False)

        assert "Vera Ondina Marcos" in csv_output
        assert "CTG 4" in csv_output
        assert "2025-06-23" in csv_output

    def test_csv_utf8_encoding(self, sample_dataframe):
        """Test that CSV properly handles UTF-8 encoding."""
        # Add Portuguese special characters
        test_df = sample_dataframe.copy()
        test_df.loc[0, "Nome"] = "José María Gonçalves Peña"
        test_df.loc[0, "Diagnostico"] = "Infecção de cateter: situação crítica"

        csv_bytes = test_df.to_csv(index=False).encode('utf-8')

        # Should decode properly
        decoded = csv_bytes.decode('utf-8')
        assert "José María" in decoded
        assert "Gonçalves" in decoded
        assert "situação" in decoded

    def test_csv_handles_commas_in_data(self):
        """Test that CSV properly escapes commas in data."""
        data = {
            "Nome": ["Silva, João"],
            "Diagnostico": ["Febre, tremores, dor abdominal"]
        }
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)

        # Commas in data should be quoted
        assert '"Silva, João"' in csv_output or 'Silva, João' in csv_output

    def test_csv_handles_quotes_in_data(self):
        """Test that CSV properly escapes quotes in data."""
        data = {
            "Nome": ['João "Zé" Silva'],
            "Plano": ['Prescrição "urgente" de antibiótico']
        }
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)

        # Should not break CSV format
        # Re-read it to verify
        df_read = pd.read_csv(StringIO(csv_output))
        assert df_read.loc[0, "Nome"] == 'João "Zé" Silva'

    def test_csv_handles_newlines_in_data(self):
        """Test that CSV properly handles newlines in data."""
        data = {
            "Nome": ["João Silva"],
            "Plano": ["Linha 1\nLinha 2\nLinha 3"]
        }
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)

        # Re-read to verify data integrity
        df_read = pd.read_csv(StringIO(csv_output))
        assert "Linha 1" in df_read.loc[0, "Plano"]
        assert "Linha 2" in df_read.loc[0, "Plano"]

    def test_csv_no_index_column(self, sample_dataframe):
        """Test that CSV export does not include index column."""
        csv_output = sample_dataframe.to_csv(index=False)
        lines = csv_output.strip().split('\n')

        # First line should be headers, not starting with index
        headers = lines[0]
        assert not headers.startswith("0,")
        assert headers.startswith("Nome,")

    def test_csv_empty_dataframe(self):
        """Test CSV export with empty DataFrame."""
        empty_df = pd.DataFrame()
        csv_output = empty_df.to_csv(index=False)

        # Should return empty string or just newline
        assert len(csv_output.strip()) == 0

    def test_csv_single_row(self, sample_clinical_data):
        """Test CSV export with single row (typical case)."""
        df = pd.DataFrame([sample_clinical_data])
        csv_output = df.to_csv(index=False)
        lines = csv_output.strip().split('\n')

        # Should have 2 lines: header + 1 data row
        assert len(lines) == 2

    def test_csv_multiple_rows(self, sample_clinical_data):
        """Test CSV export with multiple patient records."""
        data = [sample_clinical_data] * 5
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)
        lines = csv_output.strip().split('\n')

        # Should have 6 lines: header + 5 data rows
        assert len(lines) == 6

    def test_csv_bytes_encoding(self, sample_dataframe):
        """Test CSV bytes encoding as done in the app."""
        # This mimics line 36 of the original app
        csv_bytes = sample_dataframe.to_csv(index=False).encode('utf-8')

        assert isinstance(csv_bytes, bytes)
        assert len(csv_bytes) > 0

        # Should be decodable
        decoded = csv_bytes.decode('utf-8')
        assert "Vera Ondina Marcos" in decoded

    def test_csv_preserves_data_types(self, sample_dataframe):
        """Test that CSV export preserves string data correctly."""
        csv_output = sample_dataframe.to_csv(index=False)
        df_read = pd.read_csv(StringIO(csv_output))

        # Compare original and re-read data
        assert df_read.loc[0, "Nome"] == sample_dataframe.loc[0, "Nome"]
        assert df_read.loc[0, "Idade"] == sample_dataframe.loc[0, "Idade"]
        assert df_read.loc[0, "Setor"] == sample_dataframe.loc[0, "Setor"]

    def test_csv_handles_none_values(self):
        """Test CSV export with None/NaN values."""
        data = {
            "Nome": ["João Silva"],
            "Peso": [None],
            "Residente": [""]
        }
        df = pd.DataFrame(data)
        csv_output = df.to_csv(index=False)

        # Should handle None gracefully
        df_read = pd.read_csv(StringIO(csv_output))
        assert pd.isna(df_read.loc[0, "Peso"])
