"""
Interfaces Layer del Bounded Context Proposal.

Este paquete contiene los adapters de entrada mediante los cuales actores o
sistemas externos pueden invocar capacidades expuestas por Application.

Conforme a CORE-015 y CORE-016:

- Interfaces depende de Application y Shared;
- Interfaces no implementa reglas de dominio;
- Interfaces no modifica directamente el Aggregate Proposal;
- Interfaces no accede directamente a Infrastructure para ejecutar casos de uso;
- Interfaces traduce mecanismos externos hacia Commands y contratos de
  Application;
- Interfaces no reproduce Lifecycle, State Machine ni invariantes;
- Interfaces no ejecuta persistencia del Aggregate;
- Interfaces no publica Domain Events en nombre del dominio.

Los adapters concretos pueden corresponder, cuando exista una decisión
arquitectónica aprobada, a mecanismos como:

- HTTP;
- CLI;
- mensajería;
- jobs;
- otros entry points autorizados.

Para VS-001 no se introduce todavía ningún adapter concreto porque no existe
una decisión consolidada sobre el mecanismo de entrada que deba implementar:

    CreateProposalUseCase
    SubmitProposalUseCase

La dependencia esperada permanece:

    External Actor / System
            |
            v
      Inbound Adapter
            |
            v
        Application
            |
            v
          Domain

Un adapter de entrada deberá:

- recibir datos externos;
- traducirlos a estructuras de Application;
- invocar exclusivamente Input Ports;
- transformar ProposalResult a la representación requerida por el canal;
- mantener errores técnicos separados de reglas del dominio.

No deberá:

- construir estados internos arbitrarios de Proposal;
- modificar ProposalStatus;
- modificar ProposalVersion;
- acceder directamente a ProposalRepository para evitar Application;
- introducir dependencias de transporte dentro de Domain;
- convertir Read Models en Write Models.

Los símbolos públicos se exportarán únicamente cuando existan adapters
concretos aprobados y verificados.
"""