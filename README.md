# Furiosa

Triciclo elétrico documentado em todos os detalhes.

## Especificações

| Item | Detalhe |
|------|---------|
| Motor dianteiro | Hub motor Citycoco ~3 kW (sensorless FOC) |
| Motor traseiro | Motor com redução + diferencial (Hall) |
| Baterias | 2x 16S em paralelo: 8P (28Ah, BMS 100A) + 6P (21Ah, BMS 60A) |
| Células | EVE INR18650-35V (3500 mAh, 10.2A) |
| Controlador | 2x Flipsky FSESC 75200 (CAN bus) |
| Tensão | 60V nominal / 67.2V máx |
| Capacidade total | 49 Ah |
| Corrente máx. | ~140A contínuos / 100A prático (BMS menor) |
| Autonomia | _a definir_ |
| Velocidade máx. | _a definir_ |
| Peso total | _a definir_ |

## Estrutura do repositório

```
furiosa/
├── busbar/          # Sistema de conexão de alta amperagem
│   ├── busbar.md    # Documentação geral do sistema
│   └── bus-box/     # Caixa protetora da busbar
│       └── exports/ # Arquivos exportados (STEP, STL, etc.)
├── specs/           # Especificações técnicas detalhadas
├── maintenance/     # Histórico de manutenções e reparos
├── mods/            # Modificações e upgrades realizados
└── media/           # Fotos, vídeos e imagens
```

## Documentação

- [Sistema Busbar](busbar/)
- [Especificações Técnicas](specs/)
- [Histórico de Manutenção](maintenance/)
- [Modificações e Upgrades](mods/)
- [Mídia](media/)
