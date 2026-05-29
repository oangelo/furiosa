# Furiosa — Diagnóstico e Configuração dos VESCs (abr/2026)

## Resumo executivo

Setup dual VESC do triciclo elétrico Furiosa após incidente de desconexão súbita
de bateria durante operação. Documenta processo de re-flash de firmware,
investigação de problemas de comunicação CAN entre as duas placas, configuração
master/slave, e estado funcional final.

**Status atual:**

- **Flipsky FSESC 75200 Alu (motor traseiro IPM, ID 90)** — operacional.
  Sustenta 80A de phase current a 95% duty sem aquecimento anormal.
- **Makerbase MKSESC 75200 V2 OLD (hub dianteiro SPM, ID 95)** — detecção de
  motor funciona e gira a roda em teste isolado, mas **não está recebendo
  comandos ADC via CAN do master**. Causa raiz não confirmada.
- **Investigação pendente:** testar se Makerbase responde a ADC direto na placa
  (sem CAN forwarding) para isolar dano de hardware vs. configuração.

## Hardware

### Placa 1 — Hub dianteiro

- **Modelo:** Makerbase MKSESC 75200 V2 (revisão antiga, anterior a 15/nov/2023).
- **Compra:** abril/2023, loja oficial Makerbase, R$ 528,18.
- **Hwconf na firmware:** `MKSESC_75200_V2_OLD`.
- **Característica de hardware:** low-side current sensing, **sem phase shunts**
  reais, **sem suporte a phase filtering**. Phase filter ligado nesta revisão
  pode danificar o ESC.
- **VESC ID no CAN:** 95.

### Placa 2 — Motor traseiro

- **Modelo:** Flipsky FSESC 75200 Aluminum PCB (versão original, anterior a Pro V2.0).
- **Hwconf na firmware:** `FSESC_75_200_ALU`.
- **Característica de hardware:** mesma topologia low-side, sem phase filter de
  hardware.
- **VESC ID no CAN:** 90.

### Motores

Resultados da Detection (firmware 6.06):

| Parâmetro | Hub dianteiro (Citycoco) | Motor traseiro (com diferencial) |
|-----------|--------------------------|----------------------------------|
| Motor Current detectado | 94.48 A | 67.64 A |
| Motor R | 29.90 mΩ | 58.30 mΩ |
| Motor L | 96.32 µH | 161.15 µH |
| Motor Lq–Ld | 8.21 µH | **76.42 µH** |
| Motor Flux Linkage (λ) | 18.20 mWb | 22.75 mWb |
| Sensores | Hall | Hall |

**Interpretação:**

- **Hub dianteiro:** SPM clássico (Surface Permanent Magnet). Lq–Ld baixo
  indica rotor isotrópico. Sem reluctance torque significativo. MTPA dará
  ganho marginal.
- **Motor traseiro:** **IPM** (Interior Permanent Magnet) confirmado pela
  saliência alta (Lq–Ld = 76 µH). Tem reluctance torque disponível.
  **MTPA bem configurado pode trazer 10–15% de torque adicional por amp.**

## Bateria

- 16s8p EVE INR18650-35V.
- Histórico anterior: reparo de strip de níquel queimado (positivo).
- **Incidente recente:** desconexão súbita durante operação. Causa raiz da
  desconexão não documentada (BMS, conector, célula?).
- Implicação para os VESCs: spike de sobretensão de back-EMF + capacitância
  parasita pode ter estressado MOSFETs, capacitores eletrolíticos e
  transceivers CAN das duas placas.

## Histórico de firmware

### Origem do problema com firmware

Estas placas (Makerbase 75200 V2 e Flipsky 75200 Alu) foram lançadas com
firmware proprietária dos fabricantes que reportava `Hw: 75_300_R2` (incorreto).
Medições de corrente eram ruidosas, recursos como field weakening estavam
indisponíveis ou bugados. Não havia opção de update via VESC Tool oficial.

### Solução comunitária (2022)

- **jaykup** (esk8.news forum) compilou firmwares customizadas com hwconfs
  corretos (`FSESC_75_200_ALU`, `MKSESC_75_200_V2_OLD`) e disponibilizou
  como `.bin` para upload manual via VESC Tool.
- **casainho** (jan/2024) lançou release `VESCs_fix_noisy_currents-firmware_6.02`
  com filtro de corrente em software, melhorando significativamente a leitura
  ruidosa dos shunts low-side.

### Estado atual (2026)

- Os hwconfs `MKSESC_75_200_V2_OLD`, `MKSESC_75_200_V2`, `FSESC_75_200_ALU`
  estão **mergeados no upstream do Vedder** (`vedderb/bldc`) há tempos.
- Firmware é distribuída via VESC Tool em todas as releases atuais (6.06).
- O "manual change" descrito no tutorial original do jaykup hoje significa
  apenas **selecionar o hwconf correto uma vez** via "Show non-default
  firmwares", não baixar `.bin` de fórum.

### Fluxo de update aplicado

Para cada placa, uma única vez:

1. VESC Tool 6.06, conexão USB direta na placa.
2. Estado inicial: `Hw: 75_300_R2` (errado, mas é o que a fábrica configura).
3. **Firmware → Bootloader → Upload** (genérico).
4. **Firmware → Included Files → "Show non-default firmwares"**.
5. Seleciona o hwconf correto:
   - Makerbase (compra anterior a 15/nov/2023): `MKSESC_75200_V2_OLD`
   - Flipsky 75200 Alu (versão original): `FSESC_75_200_ALU`
6. Upload, reboot.
7. Confirma `HW_NAME` correto no Firmware tab após reboot.

A partir desse ponto, updates de versão (6.06 → 6.07 → ...) acontecem como
update normal — sem mais intervenção manual de hwconf.

### Critério crucial: phase filter

**Ambas as placas (Makerbase V2 OLD e Flipsky 75200 Alu) DEVEM ter
`Enable Phase Filters = False`** em Motor Settings → FOC → Filters.

Razão: nenhuma das duas tem phase shunts reais. Phase filtering em hardware
sem phase sensing é a queixa estrutural do pessoal técnico do esk8 forum
("phase filter joke"). Ligar pode danificar o ESC em ambas as gerações.

A Makerbase V2 nova (pós-Nov/2023) adicionou hardware para phase filter, mas
mantendo low-side sensing. A recomendação da comunidade veterana continua
sendo manter phase filter desligado mesmo na V2 nova.

## Configuração dual VESC via CAN

### Topologia adotada

- **Master:** Flipsky 75200 Alu (ID 90, motor traseiro). Lê ADC do throttle e
  replica comando via CAN para o slave.
- **Slave:** Makerbase 75200 V2 OLD (ID 95, hub dianteiro). Sem app de input
  ativo, apenas obedece comandos CAN do master.

### Configuração esperada — Master (Flipsky)

| Tab | Parâmetro | Valor |
|-----|-----------|-------|
| App Settings → General | App to Use | ADC |
| App Settings → General → CAN | Controller ID | 90 |
| App Settings → General → CAN | CAN Baud Rate | 500k |
| App Settings → General → CAN | CAN Mode | VESC |
| App Settings → General → CAN | Send Status Over CAN | All |
| App Settings → General → CAN | Send CAN Status Rate Hz | 50 |
| App Settings → ADC → General | **Multiple ESCs Over CAN** | **TRUE** |
| App Settings → ADC → General | Control Type | (conforme throttle físico) |
| App Settings → ADC → General | Use Filter | True |

**Crítico:** o toggle **"Multiple ESCs Over CAN"** fica dentro da aba do app
ADC, **não** na aba CAN geral. Erro comum é configurar somente na aba CAN
geral e o forwarding do input não acontecer.

### Configuração esperada — Slave (Makerbase)

| Tab | Parâmetro | Valor |
|-----|-----------|-------|
| App Settings → General | App to Use | **No App** |
| App Settings → General → CAN | Controller ID | 95 |
| App Settings → General → CAN | CAN Baud Rate | 500k |
| App Settings → General → CAN | CAN Mode | VESC |
| App Settings → General → CAN | Send Status Over CAN | All |

Slave não precisa de input próprio configurado. Status continua sendo enviado
via CAN para que o master possa monitorar (RT data, traction control).

### Tunagem inicial recomendada (não totalmente aplicada)

| Parâmetro | Hub Citycoco (ID 95) | IPM Traseiro (ID 90) |
|-----------|----------------------|----------------------|
| Flux Linkage detectado | 18.20 mWb | 22.75 mWb |
| Flux Linkage inicial sugerido | 16.4 mWb (–10%) | 21.6 mWb (–5%) |
| Observer Gain | 50% do detectado | 80% do detectado |
| Inductance (L) | manter detectado | manter detectado |
| Resistance (R) | manter detectado | manter detectado |
| MTPA | habilitar (ganho marginal) | **habilitar (ganho real)** |
| Field Weakening | 10–15A inicial | 10–20A inicial |
| Phase Filter | **False** (obrigatório) | **False** (obrigatório) |
| Sensor Mode | Hybrid | Hybrid |
| Sensorless ERPM threshold | 2000–3000 | 2000–3000 |

### Limites de corrente sugeridos

Considerando bateria 16s8p EVE INR18650-35V (capacidade nominal de pico ao
redor de 280A teóricos, mas conservativo para vida útil ~160–200A):

Por VESC, ponto de partida:

- **Motor (phase) max:** 80A em cada.
- **Battery max:** 50A em cada VESC, totalizando 100A de pack draw.
- **Battery min (regen):** −20A em cada, totalizando −40A regen.

Subir gradualmente após validação térmica e estabilidade de controle.

## Eventos e diagnóstico (cronológico)

### Incidente — desconexão de bateria sob carga

Bateria desconectou subitamente durante operação no triciclo. Causa raiz
exata não documentada. Possíveis riscos para os VESCs:

1. **Voltage spike de back-EMF + indutância parasita** — pode exceder breakdown
   dos MOSFETs (HYG015N10NS1TA, 100V).
2. **Loop de regen sem destino** — corrente regenerativa sem bateria como sink,
   capacitor de barramento absorve tudo, possível overvoltage.
3. **Faísca no reconnect** — inrush current alto se bateria reconectou com
   motor ainda em movimento.

### Resultado da Detection pós-incidente

Detection bem-sucedida em ambas as placas (resultado documentado acima).
Isso confirma:

- MCU funcional em ambas.
- USB e CAN físico operacionais para discovery.
- Pelo menos um par de gate drivers funcional por placa.
- Current sensing funcional nas três fases (caso contrário R, L, λ não seriam
  medidos coerentemente).
- Sensores Hall lidos corretamente.

**Detection NÃO testa:** MOSFETs sob alta corrente sustentada, capacitores
sob stress térmico, gate drivers degradados, sensores de Vbus descalibrados,
trilhas de PCB parcialmente danificadas.

### Sintoma 1 — "trancos estranhos" durante movimentação

Hub dianteiro apresentou movimento aos trancos. Hipóteses levantadas
(em ordem de probabilidade):

1. Tabela de Hall sensors não detectada/recalibrada após mudanças.
2. Ordem de fases vs. ordem de Halls inconsistente.
3. Sensor Mode em Sensorless puro em vez de Hybrid.
4. Openloop ruim na partida.

**Não totalmente investigado** antes da próxima descoberta.

### Sintoma 2 — Makerbase "sumindo" no CAN

Slave Makerbase desapareceu do dropdown de VESCs no VESC Tool durante
investigação dos trancos.

**Causa raiz identificada:** as duas VESCs estavam configuradas com o
**mesmo Controller ID**. Em CAN bus, IDs duplicados causam colisão de
pacotes e o VESC Tool não consegue distinguir as placas.

**Ação:** alterado um dos IDs para tornar único (95 e 90).

### Sintoma 3 — Comando manual de current via teclado não responde

Após config de IDs, descoberto que ADC funciona normalmente (motor gira
suavemente movendo o throttle), mas comando manual de "set current" via
teclado/slider do VESC Tool não faz o motor girar mesmo com valores altos.

**Hipótese provável:** comandos manuais de "Set Current" via VESC Tool têm
**timeout interno de ~1 segundo** — se não reenviado dentro do timeout, o
controle volta para zero. Comandos via app (ADC) são contínuos por design.

**Hipótese secundária:** valores baixos (5–10A) podem estar abaixo do
threshold de atrito estático do hub motor parado, que precisa tipicamente
de 15–25A para iniciar rotação.

**Não-bloqueador para operação real** — ADC funcionando é o caminho
operacional desejado.

### Sintoma 4 (atual) — Slave Makerbase não responde a comandos via CAN forwarding

Estado atual após todas as configurações acima:

- Master (Flipsky) recebe ADC e gira motor traseiro normalmente.
- Slave (Makerbase) aparece no scan CAN, Detection roda com sucesso, motor
  gira em testes isolados.
- Quando master está acelerando via ADC, **slave permanece parado**.
- Não confirmado se Iq do slave está chegando a zero (comando não
  propagou) ou está com valor mas sem efeito (problema de execução
  no slave).

**Investigação pendente:**

1. Conectar ADC direto na Makerbase (sem CAN) para testar se input físico
   gira o motor isoladamente. Se sim → problema é específico de CAN
   forwarding. Se não → problema é mais profundo no slave.
2. Verificar Iq, Duty Cycle e Current Setpoint do slave em RT Data
   simultâneo enquanto master comanda.
3. Testar comando direto via terminal do master:
   `fwd_can 95 motor_current` (ou sintaxe equivalente).
4. Substituir cabo CAN por outro para descartar mau contato físico.
5. Medir resistência entre CAN_H e CAN_L com tudo desligado:
   - Esperado: ~60Ω (dois terminadores de 120Ω em paralelo).
   - 120Ω: faltou um terminador.
   - Infinito: faltam ambos.
6. Wipe Configuration completo das duas placas e reconfigurar do zero.

## Status operacional validado

### Flipsky 75200 Alu — APROVADO para operação

Teste de carga sustentado:

- Throttle aplicado via ADC.
- Sustentou **80A de phase current a 95% duty cycle**.
- **Sem aquecimento anormal**.
- **Sem fault** durante o teste.

Indica MOSFETs, gate drivers, current sensing e dissipação térmica em
condição operacional pós-incidente. Placa pode ser considerada saudável.

### Makerbase 75200 V2 OLD — STATUS PARCIAL

- Detection: OK.
- Motor gira em teste isolado (movimento mostrado).
- **Não responde a comandos do master via CAN forwarding** (causa raiz
  pendente).
- Saúde de hardware sob carga sustentada **não validada** (testes de carga
  progressiva não realizados isoladamente nesta placa).

## Próximos passos

### Curto prazo (diagnóstico)

1. **Conectar ADC direto na Makerbase** e testar se input físico gira o motor.
   Resultado isola se problema é só CAN forwarding ou mais profundo.
2. **RT Data simultâneo** das duas placas durante operação ADC do master.
   Olhar Iq, Duty Cycle, Current Setpoint do slave.
3. **Substituir cabo CAN** por cabo de teste novo.
4. **Multímetro** entre CAN_H e CAN_L (tudo desligado): esperado ~60Ω.
5. **Wipe + reconfigure** se nada acima resolver.

### Médio prazo (validação completa)

1. Teste de carga progressiva (20A → 40A → 60A → 80A) na Makerbase
   isoladamente, mesmo padrão validado na Flipsky.
2. Teste de regen estático (`foc_openloop 30 3000` seguido de
   `foc_openloop -20 3000`) em ambas para validar tolerância a regen
   pós-incidente.
3. Logging metr.at em trajeto curto real para detectar assimetrias
   (temperatura, corrente, RPM, regen).

### Longo prazo (decisão de upgrade)

Se confirmado dano persistente na Makerbase ou problema irreparável de CAN:

| Opção | Custo aprox. (BR) | Ganho real |
|-------|-------------------|-----------|
| MKSESC 75200 V2 OLD usado | ~R$ 400–500 | Lateral, mesmo problema potencial |
| MKSESC 75200 V2 nova (pós-Nov/2023) | ~R$ 600 | Marginal |
| **MKSESC 84200HP** (INA241, phase shunts reais) | **~R$ 700–1200** | **Significativo: resolve estruturalmente o ruído de current sensing** |
| Spintend UBOX V2 75V | ~R$ 700–1000 | Lateral |
| Trampa VESC 75/300 | R$ 2500+ | Excelente, overkill |

**Recomendação se for trocar:** Makerbase 84200HP. Resolve estruturalmente
o problema original de leitura de corrente que motivou todo o histórico
de firmware customizada (jaykup, casainho). Mantém compatibilidade de
tensão (84V = 16s full charge). Permite usar phase filter corretamente.
MTPA mais efetivo no motor traseiro IPM.

Decisão recomendada de escopo:

- Substituição de UMA placa (R$ ~900): mantém setup heterogêneo, requer
  tuning separado das duas.
- Substituição de AMBAS (R$ ~1800): setup simétrico, fácil de tunar,
  Makerbase V2 OLD e Flipsky Alu antigas viram peças para Maldita ou
  Gárgula.

## Observações técnicas relevantes

### Sobre a "vadicus strategy"

Para hub motors grandes que apresentam ABS overcurrent ou cogging em
baixa rotação, a abordagem documentada no esk8 forum recomenda:

- Reduzir Observer Gain para 30–50% do valor detectado.
- Reduzir Flux Linkage em 10–15% do detectado.
- Subir `Slow ABS Current Limit` para True (usa magnitude vetorial em vez
  de shunt individual, mais robusto a ruído).
- Aumentar `Max Absolute Current` 20–30% acima do `Motor Max` configurado.

### Sobre detection com dual VESC

**Sempre rodar Motor Detection com apenas uma VESC ativa por vez.**
Há relatos no fórum de placas danificadas por detection paralela em CAN
bus simultâneo. Desconectar fisicamente o motor da outra VESC durante
detection é a prática recomendada.

### Sobre CAN forwarding e timeout

Comandos enviados via CAN têm timeout de ~1 segundo no receptor. O master
deve enviar comandos em frequência maior que isso (50 Hz padrão).
Send CAN Status Rate baixo demais (1–5 Hz) causa o slave receber comando,
expirar, voltar a zero, receber próximo, expirar novamente — comportamento
"engata-larga" indistinguível de problema de hardware.

### Sobre IDs CAN duplicados

VESC Tool não detecta IDs duplicados de forma explícita. Sintoma é placa
"sumir" intermitentemente do dropdown ou comportamento errático no
forwarding. Sempre verificar manualmente que IDs são únicos quando
configurar dual ou multi-VESC.

## Referências

- Tópico original do jaykup no esk8.news:
  <https://forum.esk8.news/t/how-to-update-firmware-on-the-flipsky-75100-75200-foc-esc/61819>
- Release do casainho com filtro de corrente:
  <https://github.com/casainho/bldc/releases> (tag
  `VESCs_fix_noisy_currents-firmware_6.02`)
- Wiki da Makerbase (desatualizada, escrita em 2022):
  <https://github.com/makerbase-mks/VESC-MKS/wiki/Makerbase-VESC75-Series-Upgrade-Instructions>
- Hwconf MKSESC_75_200_V2_OLD no upstream do Vedder:
  <https://github.com/vedderb/bldc/blob/master/hwconf/makerbase/75_200_V2/hw_mksesc_75_200_v2_old.h>
- Archive de firmwares compiladas históricas:
  <https://github.com/vedderb/vesc_fw_archive>

---

*Documento gerado em abril/2026 como registro técnico do projeto Furiosa
para o repositório no GitHub.*
