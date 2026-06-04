# Sistema de Liga/Desliga - Furiosa

## Visão Geral

Sistema de controle de energia para o triciclo elétrico Furiosa, com proteção de pré-carga para os VESCs e operação intuitiva tipo "chave de carro".

**Localização:** Caixa separada próxima à bateria
**Tensão:** 60V nominal (16S Li-ion)
**Corrente máxima:** 100A (limitado pela bateria)
**Status:** Em desenvolvimento

---

## Componentes

| Componente | Especificação | Quantidade | Status |
|------------|---------------|------------|--------|
| Relé Principal | 12V, 200A | 1 | ✅ Tem |
| Relé Pré-Carga | 12V, 40A (automotivo) | 1 | ⬜ Comprar |
| Resistor | 15Ω, 50W | 1 | ⬜ Comprar |
| Conversor DC-DC | 20-90V → 12V | 1 | ✅ Tem |
| Chave Switch | ON/OFF simples | 1 | ✅ Tem |
| Botão Momentâneo | NO (tipo buzina) | 1 | ✅ Tem |
| Fusível | 150A | 1 | ⬜ Comprar |
| Diodo | 1N5408 | 2 | ⬜ Comprar |
| Conectores XT90 | Macho/Fêmea | 4 | ⬜ Comprar |
| Conectores XT60 | Macho/Fêmea | 2 | ⬜ Comprar |
| Caixa | IP65 | 1 | ⬜ Comprar |
| Cabo 2 AWG | Vermelho/Preto | 2m | ⬜ Comprar |
| Cabo 18 AWG | Amarelo/Azul/Verde | 3m | ⬜ Comprar |

---

## Esquema Elétrico

```
┌─────────────────────────────────────────────────────────────┐
│                    CAIXA DE LIGA/DESLIGA                     │
│                         (IP65)                               │
└─────────────────────────────────────────────────────────────┘

[Bateria 60V] XT90
       │
       ├──► [Fusível 150A] ──┐
       │                      │
       ├──► [Relé Principal]  │──► XT90 ──► [VESCs]
       │      (200A)          │
       │                      │
       ├──► [Relé Pré-Carga] ─┘
       │      (40A)           │
       │      +               │
       │   [Resistor 15Ω 50W] │
       │                      │
       └──► [Chave Switch] ───┐
               │              │
               ▼              │
        [Botão Momentâneo] ◄──┘
        (NO - tipo buzina)
               │
               ▼
        [Conversor DC-DC]
           (20-90V → 12V)
               │
               └──► [Bobinas dos Relés]
                        │
                        ▼
                    [GND]
```

---

## Diagrama de Fiação

### Cores dos Fios

| Circuito | Cor | Seção | Função |
|----------|-----|-------|--------|
| Positivo 60V | Vermelho | 2 AWG | Alimentação principal |
| Negativo 60V | Preto | 2 AWG | Retorno principal |
| Positivo 12V | Amarelo | 18 AWG | Alimentação bobinas |
| Negativo 12V | Azul | 18 AWG | Retorno bobinas |
| Sinal botão | Verde | 18 AWG | Acionamento |

### Conexões Detalhadas

```
Bateria (XT90 Fêmea)
    │
    ├── Vermelho 2 AWG ──► Fusível 150A ──► Relé Principal (terminal 30)
    │                                        Relé Principal (terminal 87) ──► XT90 Macho ──► VESCs
    │                                        Relé Principal (terminal 85) ──► Amarelo 18 AWG ──┐
    │                                        Relé Principal (terminal 86) ──► Azul 18 AWG ─────┤
    │                                                                                           │
    ├── Vermelho 2 AWG ──► Relé Pré-Carga (terminal 30)                                         │
    │                      Relé Pré-Carga (terminal 87) ──► Resistor 15Ω ──► Relé Principal (30)│
    │                      Relé Pré-Carga (terminal 85) ──► Amarelo 18 AWG ─────────────────────┤
    │                      Relé Pré-Carga (terminal 86) ──► Azul 18 AWG ────────────────────────┤
    │                                                                                           │
    └── Vermelho 2 AWG ──► Chave Switch (entrada)                                               │
                           Chave Switch (saída) ──► Verde 18 AWG ──► Botão NO (terminal 1)      │
                                                                    Botão NO (terminal 2) ─────► Conversor DC-DC (+)
                                                                                                 │
Conversor DC-DC (-) ──► Azul 18 AWG ─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    [GND comum]
```

---

## Funcionamento

### Sequência de Ligação

1. **Chave Switch → ON**
   - Alimenta conversor DC-DC (60V → 12V)
   - Sistema em standby

2. **Pressionar Botão Momentâneo**
   - Energiza bobina do relé de pré-carga
   - Relé de pré-carga fecha: conecta bateria aos VESCs via resistor
   - Capacitores dos VESCs carregam gradualmente (sem faísca)
   - Tempo de carga: < 1 segundo

3. **Relé Principal Liga**
   - Após pré-carga, relé principal energiza
   - Curto-circuita o resistor (conexão direta)
   - Sistema operando normalmente

4. **Soltar Botão**
   - Relé de pré-carga desliga
   - Relé principal permanece ligado (auto-retenção via contato auxiliar)
   - Sistema continua operando

### Sequência de Desligamento

1. **Chave Switch → OFF**
   - Corta alimentação do conversor DC-DC
   - Relé principal desliga
   - Relé de pré-carga desliga
   - Sistema completamente desligado

---

## Cálculos Elétricos

### Resistor de Pré-Carga

**Dados:**
- Tensão da bateria: 60V
- Capacitância estimada dos VESCs: 2000µF (2x 1000µF)
- Tempo de pré-carga desejado: < 1s

**Cálculo:**
```
Tempo de carga (5τ) = 5 × R × C
Para 0.5s: R = 0.5 / (5 × 0.002) = 50Ω
Para 0.1s: R = 0.1 / (5 × 0.002) = 10Ω

Corrente de pico: I = V / R = 60V / 15Ω = 4A
Potência de pico: P = V² / R = 60² / 15 = 240W (muito breve)
Potência média durante carga: ~50W
```

**Valor escolhido:** 15Ω, 50W (margem de segurança)

### Relé de Pré-Carga

- Corrente de pré-carga: 4A (pico)
- Relé automotivo 40A: mais que suficiente
- Tensão da bobina: 12V

### Fusível

- Corrente máxima do sistema: 100A
- Fusível escolhido: 150A (margem de 50%)
- Protege contra curto-circuito

---

## Instruções de Montagem

### Passo 1: Preparar a Caixa

1. Furar entradas para cabos (PG13 ou PG16)
2. Instalar conectores XT90 e XT60
3. Preparar suportes para relés
4. Instalar chave e botão no painel frontal

### Passo 2: Instalar Relés

1. **Relé Principal (200A):**
   - Fixar na base da caixa
   - Conectar terminals 30 e 87 (alta corrente)
   - Conectar bobina (85 e 86)

2. **Relé Pré-Carga (40A):**
   - Fixar ao lado do relé principal
   - Conectar terminal 30 (entrada)
   - Conectar terminal 87 ao resistor
   - Conectar bobina (85 e 86)

### Passo 3: Instalar Resistor

1. Conectar entre relé pré-carga (87) e relé principal (30)
2. Fixar em suporte metálico (dissipação de calor)
3. Manter afastado de componentes plásticos

### Passo 4: Instalar Conversor DC-DC

1. Entrada: 60V (conectar após chave switch)
2. Saída: 12V para bobinas dos relés
3. Fixar na parede da caixa

### Passo 5: Instalar Chave e Botão

1. **Chave Switch:**
   - Furar painel frontal
   - Instalar com porca de fixação
   - Conectar fios de controle

2. **Botão Momentâneo:**
   - Furar painel frontal
   - Instalar com porca de fixação
   - Conectar fios NO (Normalmente Aberto)

### Passo 6: Fazer Conexões

1. Conectar fiação de alta corrente (2 AWG)
2. Conectar fiação de controle (18 AWG)
3. Instalar diodos de proteção nas bobinas
4. Verificar todas as conexões

### Passo 7: Testar

#### Teste 1 - Sem Carga
1. Conectar bateria
2. Ligar chave
3. Pressionar botão
4. Verificar se relés acionam
5. Medir tensão de saída

#### Teste 2 - Com Carga
1. Conectar VESCs
2. Repetir sequência de ligação
3. Verificar se não há faísca
4. Medir corrente de pré-carga

#### Teste 3 - Desligamento
1. Desligar chave
2. Verificar se sistema desliga imediatamente
3. Verificar se não há faísca

---

## Lista de Compras

### Eletrônica

| Item | Especificação | Estimativa de Preço | Onde Comprar |
|------|---------------|---------------------|--------------|
| Relé pré-carga | 12V 40A automotivo | R$ 15-25 | Mercado Livre |
| Resistor | 15Ω 50W | R$ 10-15 | Mercado Livre |
| Fusível 150A | Com suporte | R$ 20-30 | Mercado Livre |
| Diodo 1N5408 | 3A 1000V (pacote 10) | R$ 5-10 | Mercado Livre |

### Conectores

| Item | Quantidade | Estimativa de Preço |
|------|------------|---------------------|
| XT90 macho | 2 | R$ 10-15 |
| XT90 fêmea | 2 | R$ 10-15 |
| XT60 macho | 1 | R$ 5-8 |
| XT60 fêmea | 1 | R$ 5-8 |

### Caixa e Acessórios

| Item | Especificação | Estimativa de Preço |
|------|---------------|---------------------|
| Caixa | IP65 200x150x100mm | R$ 30-50 |
| Prensa-cabo | PG13 (2x) | R$ 5-10 |
| Terminal de conexão | 2 AWG (4x) | R$ 10-15 |
| Fita isolante | Preta | R$ 5-10 |

**Total estimado:** R$ 130-210

---

## Manutenção

### Verificações Periódicas (a cada 3 meses)

- [ ] Verificar aperto dos terminais
- [ ] Verificar estado dos conectores XT90/XT60
- [ ] Verificar funcionamento da chave e botão
- [ ] Verificar sinais de aquecimento nos relés
- [ ] Medir tensão de saída do conversor DC-DC

### Possíveis Problemas

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| Faísca na ligação | Resistor de pré-carga defeituoso | Substituir resistor |
| Relé não aciona | Bobina queimada | Substituir relé |
| Sistema não desliga | Chave switch defeituosa | Substituir chave |
| Aquecimento excessivo | Conexão frouxa | Apertar terminais |

---

## Melhorias Futuras

- [ ] Adicionar LED indicador de status
- [ ] Adicionar voltímetro digital
- [ ] Implementar proteção térmica
- [ ] Adicionar contador de ciclos (para manutenção preventiva)

---

## Referências

- [Especificações Técnicas Gerais](especificacoes.md)
- [Sistema Busbar](../busbar/busbar.md)
- [Bateria e BMS](../specs/bateria.md) (a criar)

---

## Histórico de Revisões

| Data | Versão | Alterações |
|------|--------|------------|
| 2026-06-04 | 1.0 | Documento inicial criado |

---

**Nota:** Este documento está em desenvolvimento. Atualizações serão feitas conforme a montagem e testes do sistema.
