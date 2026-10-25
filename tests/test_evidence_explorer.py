from app.services.evidence_explorer_service import (
    EvidenceExplorerService
)


def test_explorer_returns_list():

    result = (
        EvidenceExplorerService()
        .get_all_evidence()
    )

    assert isinstance(
        result,
        list
    )