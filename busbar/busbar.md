# Sistema Busbar - Conexão de Alta Amperagem

## Descrição

Sistema de conexão elétrica de alta potência para o triciclo elétrico Furiosa. 
Consiste em uma barra de cobre com múltiplos terminais para conexão dos cabos de 
alimentação, protegida por uma caixa impressa em 3D.

## Componentes

### 1. Barra de Cobre

| Parâmetro | Valor |
|-----------|-------|
| Material | Cobre eletrolítico |
| Espessura | 5 mm |
| Largura | 25 mm |
| Comprimento | ~50 mm (por segmento) |
| Quantidade | 3 segmentos |
| Acabamento | Furos e rosca M6 |

**Observações:**
- Barra cortada em pedaços de pouco menos de 50mm
- Furos roscados para fixação dos cabos
- Cobre por excelente condutividade elétrica

### 2. Fixação - Parafusos

| Parâmetro | Valor |
|-----------|-------|
| Material | Aço inox |
| Tamanho | M6 |
| Quantidade | 3 por barra |
| Acabamento | Rosca completa |

**Por que inox?**
- Resistência à oxidação e corrosão
- Manutenção da condutividade ao longo do tempo
- Ideal para ambiente com vibração (veículo elétrico)

### 3. Porcas e Arruelas

| Componente | Especificação |
|------------|---------------|
| Porcas | M6 auto-travantes com nylon |
| Arruelas | Inox M6 |

**Por que porcas com nylon?**
- Trava química que impede afrouxamento
- Resistente à vibração do veículo
- Não requer manutenção periódica de aperto

### 4. Caixa Protetora (Bus Box)

| Parâmetro | Valor |
|-----------|-------|
| Material | _a definir_ (impressão 3D / usinagem) |
| Função | Proteção e isolamento da barra |
| Acesso | Tampa com parafusos |
| Status | Em desenvolvimento |

## Funcionamento

```
[ Bateria ] ──► [ Cabo ] ──► [ Busbar ] ──► [ Cabo ] ──► [ Controlador ]
                                    │
                                    ├──► [ Cabo ] ──► [ Motor ]
                                    │
                                    └──► [ Cabo ] ──► [ Acessórios ]
```

A barra de cobre serve como ponto central de distribuição da corrente, permitindo
múltiplas conexões de forma organizada e segura.

## Especificações Elétricas

| Parâmetro | Valor |
|-----------|-------|
| Tensão nominal | _a definir_ (provavelmente 48V ou 72V) |
| Corrente máxima | _a definir_ |
| Seção do cabo | _a definir_ |
| Tipo de conexão | Parafuso M6 com terminal olhal |

## Materiais Necessários

- [x] Barra de cobre 5x25mm
- [x] Parafusos inox M6 (9 unidades - 3 por barra)
- [x] Porcas auto-travantes M6 com nylon (9 unidades)
- [x] Arruelas inox M6 (9 unidades)
- [ ] Caixa protetora (em desenvolvimento)
- [ ] Cabos de alta corrente com terminais olhal M6

## Status do Projeto

**Em desenvolvimento (WIP)**

- [x] Definição da barra de cobre
- [x] Definição dos parafusos e fixações
- [x] Corte e preparação da barra
- [ ] Finalização da caixa protetora
- [ ] Testes de montagem
- [ ] Testes elétricos sob carga

## Notas de Desenvolvimento

- Barra de cobre cortada manualmente em segmentos de ~50mm
- Furos roscados M6 para fixação segura dos cabos
- Uso de inox em toda a fixação para evitar corrosão galvânica
- Porcas com nylon essenciais para ambiente com vibração

## Próximos Passos

1. Finalizar modelo 3D da caixa protetora
2. Imprimir/testar caixa
3. Definir seção e tipo dos cabos de conexão
4. Realizar testes de carga
5. Verificar aquecimento sob operação

## Arquivos Relacionados

- `busbar/bus-box/bus-box.FCStd` - Modelo FreeCAD da caixa (em desenvolvimento)
- `busbar/bus-box/exports/` - Arquivos exportados (STEP, STL, etc.)

## Referências

- [Especificações Técnicas](../specs/)
- [Modificações e Upgrades](../mods/)
