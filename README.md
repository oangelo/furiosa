# Furiosa

Triciclo elétrico documentado em todos os detalhes.

## Especificações

| Item | Detalhe |
|------|---------|
| Motor dianteiro | Hub motor Citycoco ~3 kW (sensorless FOC) |
| Motor traseiro | Motor com redução + diferencial (Hall) |
| Bateria | 16S8P EVE INR18650-35V, 60V 28Ah |
| BMS | Daly Smart BMS 100A 16S (WiFi + CAN) |
| Controlador | 2x Flipsky FSESC 75200 (CAN bus) |
| Tensão | 60V nominal / 67.2V máx |
| Corrente máx. | ~80A contínuos / 100A prático |
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
