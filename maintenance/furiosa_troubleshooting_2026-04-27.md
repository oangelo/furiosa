# Resumo da sessão de troubleshooting da Furiosa

## Ponto de partida

Você queria controlar o motor pelo VESC Tool e tinha um VESC dianteiro que não funcionava enquanto o traseiro rodava perfeitamente.

## Sequência do diagnóstico

**1. Controle pelo VESC Tool e interferência do ADC.** Descobrimos que o app ADC ativo sobrescreve os comandos da interface (setas, botões play/pause), mesmo via USB/CAN — bug conhecido no firmware. Solução: mudar temporariamente "App to Use" para "No App" durante testes pela interface. Você desativou o ADC e conseguiu testar livremente.

**2. Problema do VESC dianteiro — hipótese inicial: mosfet queimado?** O traseiro funcionava, o dianteiro não. Eu te dei o procedimento de teste de mosfets pelos fios de fase com multímetro em modo diodo, mas ressaltei que a 75200 tem 6 mosfets paralelos por fase, dificultando diagnóstico de mosfet individual.

**3. Refinamento do diagnóstico — não era mosfet.** Você descreveu o sintoma certo: "vibra loucamente mas não gira, sendo que na detection gira perfeitamente". Esse padrão exclui mosfet — detection roda em open-loop, então se uma fase estivesse comprometida, falharia ali. O problema estava no closed-loop (observer ou sensor).

**4. Investigação do hall sensor.** A tabela de hall do dianteiro estava numericamente correta (deltas de ~33 unidades, sequência monotônica), mas o motor vibrava com hall ativo. Você fez `hall_analyze` e o plot mostrou:
- Hall 3 com duty cycle absurdamente desbalanceado (ficava em 1 quase o tempo todo)
- Glitches impossíveis nos canais individuais
- Sequência caótica do "Combined"

Diagnóstico: hall sensor com problema elétrico — possivelmente sensor 3 com defeito, ou cabo de hall com mau contato/quebrado na entrada do eixo do hub motor.

**5. Tentativa de HFI como alternativa.** Medimos a saliência do motor: **L = 97,31 µH, Lq-Ld = 6,41 µH (~6,6%)**. Saliência marginal, típica de hub motor SPM (ímãs colados na superfície). Você ativou HFI e o plot mostrou ruído quase uniforme sem padrão senoidal — tracking inviável. **HFI descartado** para esse motor.

**6. Decisão: sensorless puro.** Você confirmou que sem hall, em modo sensorless, o motor da Furiosa funciona super forte. Diagnóstico fechado: VESC e motor estão íntegros, problema isolado ao hall sensor do dianteiro (mas você decidiu não abrir o motor).

**7. Tuning do open-loop pra melhorar a partida.** Aplicou o preset "Heavy Inertial Load" e ajustou parâmetros. Configuração final aceita:
- Openloop ERPM = 1500
- Openloop Hysteresis = 0,15 S
- Openloop Lock Time = 0,5 S
- Openloop Ramp Time = 0,5 S
- Openloop Time = 0,20 S
- Openloop Current Boost = 5 A
- Openloop Current Max = 20 A

**8. Problema do botão de ré.** O botão de ré não funcionava no modo "Current Reverse ADC2 Brake Button" — bug conhecido no firmware. Como teu manete é unidirecional (estilo moto), você precisava escolher entre regen variável e ré.

**9. Resolução final do botão de ré.** O problema real era o pino: você estava com **App to Use = "ADC and UART"** mas o botão estava conectado no pino que correspondia ao modo "ADC". Mudou para "ADC" puro e funcionou.

## Estado final da Furiosa

- **VESC traseiro:** modo Hall, funcionando perfeitamente.
- **VESC dianteiro:** modo Sensorless com tuning Heavy Inertial Load, partida aceitável.
- **Controle:** ADC com botão de ré funcionando, App to Use = "ADC".
- **Bateria 16S8P:** OK.
- **Pendência futura (sem urgência):** abrir o cubo do dianteiro um dia pra investigar o cabo de hall na entrada do eixo (ponto clássico de quebra por flexão). Se o sensor 3 estiver morto, troca por SS41 ou A3144 latching.

## Nota sobre o setup de conexão usado no diagnóstico

Durante esta sessão, o VESC Tool estava rodando no PC conectado via IP bridge a um celular, que por sua vez conectava ao VESC por Bluetooth. Segundo relatos no [fórum pev.dev](https://pev.dev/t/diagnosing-hall-sensors/1795/3), essa cadeia de conexão (Bluetooth + bridge) pode introduzir latência e ruído que comprometem ferramentas de diagnóstico como `hall_analyze`. O `hall_analyze` não rodou corretamente neste setup — possivelmente seria necessário conectar o cabo USB direto ao VESC para resultados confiáveis. Isso não invalida o diagnóstico de hall com defeito (os sintomas de vibração e os plots com glitches são consistentes), mas o resultado do `hall_analyze` deveria ser confirmado com conexão direta antes de conclusões definitivas sobre qual sensor está falhando.

## Aprendizados técnicos da sessão

- ADC ativo bloqueia controle pela interface do VESC Tool (mudar pra "No App" pra testar).
- Detection rodando bem + motor vibrando no controle = problema de sensor/observer, não de mosfet.
- Tabela de hall correta numericamente não garante hall funcional sob carga — sinal pode estar sujo, com glitches, ou intermitente.
- HFI exige saliência ≥15% pra funcionar bem; hub motor SPM raramente atende.
- O pino do botão de reverse depende do "App to Use" — erro comum trocar entre "ADC" e "ADC and UART" sem religar o botão no pino correto.
- Bug conhecido: "Current Reverse ADC2 Brake Button" ignora o botão de reverse no firmware atual.

## Para guardar

Salva o XML da config final do dianteiro como `furiosa_dianteiro_sensorless_2026-04-27.xml` e do traseiro como `furiosa_traseiro_hall_2026-04-27.xml`. Da próxima vez que mexer ou atualizar firmware, você tem o ponto de partida bom guardado.

Boa pilotada na Furiosa. 🏍️
