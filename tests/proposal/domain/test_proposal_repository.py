from abc import ABC

from arada_core.proposal.domain.repositories.proposal_repository import (
    ProposalRepository,
)


def test_proposal_repository_is_abstract_domain_contract() -> None:
    """
    ProposalRepository debe permanecer como contrato abstracto perteneciente
    a Domain.

    La implementación concreta corresponde a Infrastructure y no forma parte
    del Vertical Slice VS-001 mientras no se introduzca una tecnología de
    persistencia específica.
    """
    assert issubclass(ProposalRepository, ABC)
    assert ProposalRepository.__abstractmethods__ == {
        "get_by_id",
        "exists",
        "save",
    }


def test_repository_contract_does_not_define_query_model_operations() -> None:
    """
    ProposalRepository debe permanecer orientado al Aggregate completo.

    Las consultas complejas, listados, filtros, búsquedas y estadísticas
    pertenecen a Read Models y no deben incorporarse al Repository del
    Aggregate.
    """
    repository_operations = {
        name
        for name in ProposalRepository.__dict__
        if not name.startswith("_")
    }

    forbidden_query_operations = {
        "find_all",
        "list",
        "search",
        "filter",
        "paginate",
        "statistics",
        "find_by_organization",
        "find_by_territory",
        "find_by_status",
        "find_by_proposer",
    }

    assert repository_operations.isdisjoint(forbidden_query_operations)


def test_repository_contract_exposes_only_aggregate_persistence_capabilities() -> None:
    """
    El contrato mínimo de VS-001 debe limitarse a las capacidades necesarias
    para recuperar, verificar existencia y persistir Proposal.
    """
    public_operations = {
        name
        for name, value in ProposalRepository.__dict__.items()
        if callable(value) and not name.startswith("_")
    }

    assert public_operations == {
        "get_by_id",
        "exists",
        "save",
    }


def test_repository_contract_contains_no_infrastructure_specific_api() -> None:
    """
    El contrato de Domain no debe filtrar conceptos propios de una tecnología
    concreta de persistencia.
    """
    repository_members = set(ProposalRepository.__dict__)

    forbidden_terms = {
        "sql",
        "orm",
        "session",
        "cursor",
        "collection",
        "document",
        "table",
        "mongo",
        "postgres",
        "redis",
        "commit",
        "rollback",
    }

    for member in repository_members:
        normalized_member = member.lower()

        assert all(
            forbidden_term not in normalized_member
            for forbidden_term in forbidden_terms
        )