"""
Repository Contracts del Bounded Context Proposal.

Este paquete contiene los contratos de persistencia pertenecientes al dominio
Proposal.

Conforme a CORE-011 y a las reglas arquitectónicas de AURA Core:

- el contrato Repository pertenece a Domain;
- Infrastructure implementa el contrato;
- Application puede utilizarlo para coordinar casos de uso;
- el Repository opera sobre el Aggregate completo;
- Proposal constituye la unidad de consistencia;
- el Repository no expone detalles de ORM, SQL o almacenamiento;
- las consultas complejas pertenecen a Read Models especializados;
- la persistencia debe preservar Version;
- las escrituras deben soportar control de concurrencia optimista mediante
  ExpectedVersion cuando corresponda.

Para VS-001 se incorporará el contrato:

    ProposalRepository

Su implementación física permanecerá fuera de Domain.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""