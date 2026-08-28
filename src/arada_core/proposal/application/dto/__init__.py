"""
Data Transfer Objects de la Application Layer del Bounded Context Proposal.

Este paquete contiene representaciones de datos utilizadas para comunicar
resultados de casos de uso sin exponer directamente el Aggregate Proposal.

Conforme a CORE-013 y a las reglas de Application Services de AURA Core:

- los DTO pertenecen a Application;
- no representan Aggregates;
- no contienen comportamiento de dominio;
- no contienen invariantes;
- no ejecutan persistencia;
- no dependen de Infrastructure;
- no contienen detalles HTTP;
- no contienen detalles de ORM;
- no sustituyen Read Models especializados;
- no permiten modificar Proposal;
- pueden representar resultados estables de casos de uso.

Para VS-001, los DTO deberán permitir representar los resultados necesarios
de los casos de uso:

    CreateProposal
    SubmitProposal

sin devolver el Aggregate Proposal como contrato público de Application.

Los símbolos públicos se exportarán únicamente cuando sus implementaciones
correspondientes hayan sido creadas y verificadas.
"""