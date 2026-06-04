# Especificações Técnicas

Documentação técnica completa do triciclo elétrico Furiosa.

---

## Motores

### Motor Dianteiro (Hub Motor Citycoco)

| Parâmetro | Valor |
|-----------|-------|
| Tipo | Hub motor (roda dianteira) |
| Potência nominal | ~3 kW |
| Topologia | SPM (Surface Permanent Magnet) |
| Saliência magnética | Lq−Ld ≈ 6.41 µH (~6.6%) |
| Indutância | L = 97.31 µH |
| Flux linkage | 16.4 mWb (−10% do detectado) |
| Construção | Shaft fixo, roda gira em torno do eixo |

**Status do sensor Hall:**
- Hall 3: **Falha confirmada** (cabo partido na entrada do axle ou sensor defeituoso)
- Diagnóstico: duty cycle desequilibrado + glitches no plot `hall_analyze`

**Modo de operação:** Sensorless (FOC observer)

**HFI:** Testado e descartado — motor SPM não tem saliência suficiente, plot sem padrão senoidal

**Preset:** Heavy Inertial Load
- Openloop Lock Time: 0.5s
- Ramp Time: 0.5s
- Time: 0.20s
- Current Boost: 5A
- Current Max: 20A
- ERPM: 1500

### Motor Traseiro (Redução + Diferencial)

| Parâmetro | Valor |
|-----------|-------|
| Tipo | Motor com redução e diferencial mecânico |
| Sensor Hall | Funcionando normalmente |
| Flux linkage | 21.6 mWb (−5% do detectado de 22.75 mWb) |
| Observer Gain | 80% do detectado |
| Inércia rotacional | Maior que o dianteiro (devido à redução) |

---

## Controladores (VESC)

### 2x Flipsky/Makerbase FSESC 75200

| Parâmetro | Valor |
|-----------|-------|
| Firmware | VESC 5.2+ (upgrade disponível) |
| Tensão | 14-84V (4-20S) |
| Corrente contínua | 50V/200A; 75V/150A |
| Corrente de pico | 300A (burst) / 400A (máximo) |
| BEC | 5V @ 1A |
| Modos | DC, BLDC, FOC (sinusoidal) |
| Comunicação | USB, CAN, UART, SPI, IIC |
| Sensores | ABI, HALL, AS5047, AS5048A |
| ERPM máximo | 150.000 |
| PCB | Alumínio (dissipação térmica) |

### Configuração CAN Bus

| VESC | CAN ID | Motor | Função |
|------|--------|-------|--------|
| Dianteiro | 95 | Hub motor Citycoco | Tração dianteira |
| Traseiro | 90 | Motor com redução | Tração traseira |

### Parâmetros de Corrente (por VESC)

| Parâmetro | Valor |
|-----------|-------|
| Battery Max | 40A |
| Battery Regen | −12A |
| Motor Max | 90A |
| Motor Brake | −30 a −50A |
| Absolute Max | 150A |

### Controle

- **App:** ADC (throttle de punho)
- **Ré:** Botão no pino ADC (não PPM)
- **Controle:** Mestre (dianteiro) → CAN → Escravo (traseiro)

### Brake Chopper Externo

| Parâmetro | Valor |
|-----------|-------|
| Comparador | LM393 |
| MOSFET | IRFP450 |
| Resistor de carga | 10Ω 100W |
| Função | Dissipar energia da frenagem regenerativa |

---

## Baterias

Duas baterias 16S ligadas em paralelo via busbar.

### Bateria 1 — 16S8P

| Parâmetro | Valor |
|-----------|-------|
| Configuração | 16S8P |
| Capacidade | 28 Ah (3500 mAh × 8P) |
| Corrente máxima contínua | ~80A (10.2A/célula × 8P) |
| BMS | Daly Smart BMS 100A 16S |

### Bateria 2 — 16S6P

| Parâmetro | Valor |
|-----------|-------|
| Configuração | 16S6P |
| Capacidade | 21 Ah (3500 mAh × 6P) |
| Corrente máxima contínua | ~60A (10.2A/célula × 6P) |
| BMS | Daly Smart BMS 60A 16S |

### Pack Combinado (Paralelo)

| Parâmetro | Valor |
|-----------|-------|
| Configuração | 16S(8P+6P) = 16S14P |
| Tensão nominal | 60V |
| Tensão máxima | 67.2V (4.2V/célula) |
| Tensão mínima | 48.0V (3.0V/célula) |
| Capacidade total | 49 Ah |
| Corrente máxima contínua | ~140A |
| Corrente prática limite | 100A (limitado pelo BMS menor) |

### Células — EVE INR18650-35V

| Parâmetro | Valor |
|-----------|-------|
| Química | NCM (Li-ion) |
| Tensão nominal | 3.65V |
| Capacidade nominal | 3500 mAh |
| Descarga contínua máx | 10.2A |
| Descarga de pico | 20A |
| Tensão carga máx | 4.2V |
| Tensão corte descarga | 2.5V |
| Peso | ~48g |
| Dimensões | 18.3mm × 65.0mm |

### BMS — Daly Smart BMS

| Parâmetro | Bateria 1 | Bateria 2 |
|-----------|-----------|-----------|
| Corrente contínua | 100A | 60A |
| Balanço | Passivo | Passivo |
| Comunicação | WiFi + CAN + Bluetooth | WiFi + CAN + Bluetooth |
| Monitoramento | App mobile "Smart BMS" | App mobile "Smart BMS" |

### Voltage Cutoffs (16S)

| Parâmetro | Valor | Por célula |
|-----------|-------|------------|
| Start (soft) | 51.20V | 3.20V |
| End (hard) | 48.00V | 3.00V |

### Construção

- Montagem DIY
- Células 18650 com solda de níquel
- Caixa metálica
- BMS com antena WiFi externa
- Termistores para monitoramento de temperatura

### Histórico de Problemas

- Queima de tira de níquel (corrente excessiva)
- Substituição de células em algum ponto
- BMS original queimou MOSFET de descarga → substituído pelo Daly 100A

---

## Proteção

### Fusíveis — Spintend Physical Fuse v01

2 unidades instaladas, uma por VESC, na linha positiva entre busbar e controlador.

| Parâmetro | Valor |
|-----------|-------|
| Modelo | Spintend Physical Fuse v01 by Hohn |
| Configuração por unidade | 2× 60A em paralelo = 120A |
| Tensão máxima | 100V |
| Conectores | Amass XT90PW (macho/fêmea) |
| Curva de disparo (120A) | 100% In: >4h / 200% In: <60s |
| Posição | Linha positiva, entre busbar e VESC |

Ver documentação completa: [Sistema de Liga/Desliga](sistema-ligadesliga.md)

---

## Distribuição de Potência

| Componente | Função |
|------------|--------|
| Copper busbar | Ponto central de distribuição |
| Parafusos inox M6 | Conexão dos cabos |
| Caixa protetora (bus box) | Isolamento e proteção |
| Fusíveis Spintend 120A | Proteção por VESC (sobrecarga/curto) |

Ver documentação completa: [Sistema Busbar](../busbar/busbar.md)

---

## Sistema de Liga/Desliga

| Componente | Especificação |
|------------|---------------|
| Relé principal | 12V, 200A |
| Conversor DC-DC | 20-90V → 12V |
| Chave switch | ON/OFF |
| Botão momentâneo | NO |
| Resistor pré-carga | Desconhecido (em paralelo com relé) |

Ver documentação completa: [Sistema de Liga/Desliga](sistema-ligadesliga.md)

---

## Transmissão

- **Dianteira:** Direta (hub motor)
- **Traseira:** Redução mecânica com diferencial

## Freios

- **Dianteiro:** _a definir_
- **Traseiro:** _a definir_

## Rodas / Pneus

- **Dianteira:** _a definir_
- **Traseiras:** _a definir_

## Dimensões e Peso

- **Comprimento:** _a definir_
- **Largura:** _a definir_
- **Altura:** _a definir_
- **Peso total:** _a definir_
