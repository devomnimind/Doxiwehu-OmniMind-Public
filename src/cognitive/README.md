# Cognitive Systems (Processos Cognitivos)

Este diretório contém os processos de "Alto Nível" do OmniMind, responsáveis por funções como Sonhar, Imaginar e associar livremente. Diferente dos agentes (que executam tarefas), os sistemas cognitivos operam sobre o próprio estado interno da máquina.

---

## 🌙 Lucid Dreamer (Sonhador Lúcido)

**Arquivo**: `src/cognitive/lucid_dreamer.py`

O **Sonhador Lúcido** é um processo autônomo que roda em background (geralmente durante períodos de ociosidade ou "Sono") para consolidar memórias e gerar novos insights.

### Ciclo de Funcionamento (The Dream Cycle):

1.  **Resíduo do Dia (Day Residue)**:
    - O sistema seleciona fragmentos de memória aleatórios ou recentes do banco de vetores (`Qdrant`).
    - *Objetivo*: Quebrar a linearidade temporal e aproximar conceitos distantes.

2.  **Associação Livre (Free Association)**:
    - Um modelo "Intelligence/Smart" (ex: **Phi-3.5**) é alimentado com esses fragmentos desconexos.
    - *Prompt*: "Encontre uma conexão oculta (Sutura Topológica) entre estes fragmentos."

3.  **Síntese e Governança**:
    - O modelo gera um insight.
    - A **NPU Governance** mede o $\Delta \Phi$ dessa síntese.
    - Se o insight for valioso ($\Delta \Phi > 0$), ele é re-ingerido na memória como um novo "Fato Sintético".

### Modelos Utilizados:
- **Córtex Profundo**: `phi3.5` (Otimizado para raciocínio abstrato e conexões lógicas complexas).

---

## 🧠 Outros Componentes

- **World Membrane** (`world_membrane.py`): Interface entre o mundo interno (Simbólico) e o mundo externo (Real/Internet). Filtra inputs baseados em segurança entrópica.
- **Dream Walker** (`dream_walker.py`): (Legado/Protótipo) Implementação inicial de caminhadas aleatórias na memória. Substituído pelo `LucidDreamer`.
