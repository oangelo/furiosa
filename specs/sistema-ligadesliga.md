# Sistema de Liga/Desliga — Furiosa

## O Problema da Faísca

Os controladores VESC possuem capacitores de entrada grandes (~1000µF cada, ~2000µF total no sistema). Quando a bateria é conectada diretamente a capacitores descarregados, a diferença de potencial é máxima e a corrente de surto é limitada apenas pela resistência interna dos capacitores e da fiação — praticamente um curto-circuito momentâneo.

**Corrente de surto estimada:**
```
I = V / R_esr
I = 60V / ~0.05Ω = ~1200A (pico teórico)
```

Na prática a corrente é menor (limitada pela indutância e resistência dos cabos), mas o suficiente para:

- **Arco elétrico** no momento da conexão — degrada conectores e terminais
- **Vaporização de material** nos contatos —Connectores XT90 são projetados para 90A contínuos, não para picos de centenas de ampères
- **Risco de queimadura** se o conector estiver na mão
- **Danos ao BMS** — o surto passa pelo BMS antes de chegar aos capacitores

O problema é idêntico ao de ligar uma chave em um banco de capacitores — sempre que a tensão do capacitor é muito diferente da tensão da fonte, haverá um transiente de corrente proporcional à diferença.

## Anti-Spark Switches Comerciais

Existem switches anti-spark dedicados que resolvem o problema:

- **Flipsky Anti-Spark Switch** (~R$ 200-300)
- **MakerX Anti-Spark Switch** (~R$ 150-250)
- **Vedder Anti-Spark Switch** (open-source, ~R$ 100 em componentes)

Funcionam com um MOSFET que faz a pré-carga gradualmente e depois liga completamente. São compactos e plug-and-play.

**Problemas:**
- Preço elevado para o que fazem
- Limitados em corrente (tipicamente 100-200A)
- Componente adicional que pode falhar
- Difícil reposição no Brasil

## Solução Barata: Pré-Carga com Resistor

A ideia é simples: em vez de conectar a bateria diretamente aos capacitores, conectar primeiro através de um resistor que limita a corrente a um valor seguro. Depois que os capacitores carregam, curto-circuitar o resistor para operação normal.

**Cálculo da corrente de pré-carga:**
```
Com R = 15Ω:
I_inicial = 60V / 15Ω = 4A
P_inicial = 60V × 4A = 240W (por frações de segundo)
```

**Tempo de carga:**
```
τ = R × C = 15Ω × 0.002F = 0.03s
5τ (carga completa) = 0.15s
```

Os capacitores carregam em ~150ms — praticamente instantâneo para um ser humano. Depois disso, a tensão nos capacitores iguala a da bateria e não há mais diferença de potencial significativa.

**Componentes mínimos:**
- Resistor de 15Ω, 50W — suporta o pico de 240W por 150ms sem problemas
- Um meio de curto-circuitar o resistor após a carga (relé, chave manual, etc.)

---

## Sistema Atual

### Componentes Instalados

| Componente | Especificação |
|------------|---------------|
| Relé principal | 12V, 200A |
| Conversor DC-DC | 20-90V → 12V |
| Resistor de pré-carga | Valor desconhecido (instalado em paralelo com o relé) |
| Chave switch | ON/OFF |
| Botão momentâneo | NO (normalmente aberto) |
| Fusíveis (2×) | Spintend Physical Fuse v01, 120A cada (2× 60A paralelo), 100V |

### Como Funciona

```
                         ┌─────────────────┐
  Bateria 60V ──────────┤ Resistor         ├───────── [Fusível 120A] ──► VESC dianteiro
              │          └─────────────────┘              │
              │              │                            │
              │    ┌─────────┴─────────┐         [Fusível 120A] ──► VESC traseiro
              └────┤ Relé 200A         ├─────────┘
                   │ (N.O.)            │
                   └───────┬───────────┘
                           │
                     bobina 12V
                           │
              ┌────────────┴────────────┐
              │                         │
        Chave ON/OFF              Botão N.O.
              │                    (momentâneo)
              │                         │
              └─────┬───────────────────┘
                    │
             Conversor DC-DC
              (60V → 12V)
                    │
                  GND
```
                        ┌─────────────────┐
  Bateria 60V ──────────┤ Resistor         ├──── VESCs (+)
              │          └─────────────────┘     │
              │              │                    │
              │    ┌─────────┴─────────┐         │
              └────┤ Relé 200A         ├─────────┘
                   │ (N.O.)            │
                   └───────┬───────────┘
                           │
                     bobina 12V
                           │
              ┌────────────┴────────────┐
              │                         │
        Chave ON/OFF              Botão N.O.
              │                    (momentâneo)
              │                         │
              └─────┬───────────────────┘
                    │
             Conversor DC-DC
              (60V → 12V)
                    │
                  GND
```

**Para ligar:**

1. Chave → ON
2. Corrente flui pelo resistor → carrega capacitores dos VESCs (sem faísca)
3. Conversor DC-DC gera 12V → energiza bobina do relé
4. Relé fecha → curto-circuita o resistor → conexão direta bateria↔VESCs
5. Sistema operacional

**Para desligar:**

1. Pressionar botão momentâneo → corta alimentação da bobina do relé
2. Relé abre → sistema desligado
3. A chave ON/OFF sozinha **não desliga** o sistema

### Problemas do Sistema Atual

1. **Resistor permanentemente no circuito** — embora a maioria da corrente passe pelo relé (resistência ~mΩ), o resistor em paralelo dissipa energia continuamente quando o relé está fechado
2. **Sequência de desligamento confusa** — a chave liga mas não desliga, é necessário usar o botão
3. **Se o botão falhar, não há como desligar** — a não ser desconectar a bateria
4. **Sem indicador visual** — impossível saber se o sistema está ligado ou desligado sem medição

---

## Melhorias Possíveis

### Opção A: Dois Relés (Pré-Carga Dedicada)

Adicionar um segundo relé (automotivo 12V 40A, ~R$ 15-25) dedicado exclusivamente à pré-carga. O resistor só fica no circuito durante os ~150ms de carga.

**Esquema proposto:**
```
  Bateria 60V ──────┬──────────────────────────────── VESCs (+)
                    │                                    │
          ┌─────────┴──────────┐                         │
          │ Relé Pré-Carga 40A ├──── Resistor 15Ω 50W ───┤
          │ (N.O.)             │                         │
          └─────────┬──────────┘                         │
                    │                                    │
          ┌─────────┴──────────┐                         │
          │ Relé Principal 200A ├────────────────────────┘
          │ (N.O.)             │
          └─────────┬──────────┘
                    │
              bobinas 12V
```

**Lógica de operação:**
1. Chave ON → pressiona botão → relé de pré-carga liga → capacitores carregam via resistor
2. Relé principal liga (manualmente ou com delay) → curto-circuita resistor
3. Solta botão → relé de pré-carga desliga → resistor fora do circuito
4. Relé principal permanece ligado (auto-retenção)
5. Chave OFF → corta alimentação → relé principal desliga → sistema off

**Vantagens:**
- Resistor fora do circuito durante operação normal
- Desligamento simples: basta a chave OFF
- Componentes baratos e fáceis de encontrar

**Desvantagens:**
- Mais fiação e complexidade
- Dois relés para gerenciar
- Necessita lógica de auto-retenção no relé principal

### Opção B: Chave Seletora (Manual)

Substituir o sistema de relés por uma chave seletora de 3 posições: OFF → PRÉ-CARGA → ON.

Na posição PRÉ-CARGA, a corrente passa pelo resistor. Na posição ON, a corrente passa direto. Sem eletrônica, sem relés.

**Vantagens:**
- Extremamente simples e robusto
- Sem eletrônica que pode falhar
- Operação intuitiva

**Desvantagens:**
- Precisa de uma chave de alta corrente (carregadora de bateria ou similar)
- Operação manual em dois passos
- Difícil encontrar chave adequada para 100A+ no Brasil

### Opção C: Anti-Spark Switch Comercial

Substituir todo o sistema por um anti-spark switch dedicado (ex: Flipsky, ~R$ 200-300).

**Vantagens:**
- Plug-and-play, sem projeto
- Compacto
- Pré-carga automática via MOSFET

**Desvantagens:**
- Caro
- Limitado em corrente
- Se queimar, é componente único sem reposição fácil

### Opção D: MOSFET com Pré-Carga (DIY)

Circuito com MOSFET de alta corrente (ex: IRFP4468) controlado por um RC para ramp de gate lenta, fazendo a pré-carga automaticamente.

**Vantagens:**
- Sem partes mecânicas (sem desgaste de contatos)
- Pré-carga automática e controlada
- Barato em componentes (~R$ 30-50)

**Desvantagens:**
- Complexidade eletrônica significativa
- Necessita dissipador grande
- Falha em MOSFET pode ser perigosa (curto permanente)
- Exige conhecimento de eletrônica de potência para projetar

### Comparação

| Critério | A: 2 Relés | B: Chave Seletora | C: Comercial | D: MOSFET DIY |
|----------|------------|-------------------|--------------|----------------|
| Custo | ~R$ 50 | ~R$ 30-80 | ~R$ 200-300 | ~R$ 30-50 |
| Complexidade | Média | Baixa | Baixa | Alta |
| Robustez | Alta | Muito alta | Média | Baixa |
| Desligamento simples | Sim | Sim | Sim | Sim |
| Reposição fácil | Sim | Sim | Não | Parcial |
| Sem resistor permanente | Sim | Sim | N/A | N/A |

---

## Referências

- [Especificações Técnicas Gerais](especificacoes.md)
- [Sistema Busbar](../busbar/busbar.md)
