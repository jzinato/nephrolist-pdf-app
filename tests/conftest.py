"""
Pytest configuration and shared fixtures for NephroList PDF App tests.
"""
import pytest
import pandas as pd
from io import BytesIO


@pytest.fixture
def sample_clinical_data():
    """Sample clinical data matching expected extraction format."""
    return {
        "Nome": "Vera Ondina Marcos",
        "Setor": "CTG 4",
        "Leito": "19",
        "Idade": "82",
        "Data_Admissao": "2025-06-23",
        "Motivo_Internacao": "Febre e tremores em paciente dialítica",
        "Diagnostico": "Infecção de cateter de hemodiálise",
        "Situacao_Atual": "Afebril, vertigem postural, PA 90x60",
        "Dialise": "Sim / Crônico",
        "Peso": "65",
        "Plano": "Suspender Anlodipino e Furosemida. HD + ATB guiado por vancocinemia.",
        "Preceptor": "Gabriel Silqueira",
        "Residente": "Marcela Oliveira",
        "Desfecho": "Alta",
        "Data_Desfecho": "2025-06-28"
    }


@pytest.fixture
def sample_clinical_data_missing_fields():
    """Sample data with some optional fields missing."""
    return {
        "Nome": "João Silva",
        "Setor": "CTG 2",
        "Leito": "10",
        "Idade": "65",
        "Data_Admissao": "2025-06-20",
        "Motivo_Internacao": "Insuficiência renal aguda",
        "Diagnostico": "IRA pós-renal",
        # Missing: Situacao_Atual
        "Dialise": "Não",
        # Missing: Peso
        "Plano": "Hidratação e monitoramento",
        "Preceptor": "Ana Santos",
        # Missing: Residente
        "Desfecho": "Alta",
        "Data_Desfecho": "2025-06-25"
    }


@pytest.fixture
def sample_dataframe(sample_clinical_data):
    """Sample DataFrame created from clinical data."""
    return pd.DataFrame([sample_clinical_data])


@pytest.fixture
def mock_pdf_file():
    """Mock PDF file object for testing."""
    pdf_content = b"%PDF-1.4\nMock PDF content"
    return BytesIO(pdf_content)


@pytest.fixture
def invalid_pdf_file():
    """Invalid/corrupted PDF file for error testing."""
    return BytesIO(b"This is not a PDF file")


@pytest.fixture
def empty_file():
    """Empty file for edge case testing."""
    return BytesIO(b"")
