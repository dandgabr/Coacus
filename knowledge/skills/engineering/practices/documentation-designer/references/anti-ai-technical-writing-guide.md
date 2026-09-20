# ✍️ Canonical Guide to Human Technical Prose & Anti-AI Writing (Craft Docs)

This practical guide provides editorial rules, comparative transformation tables ("Before vs After"), and an audit checklist to eliminate "AI Idiolect" and produce technical documentation that is human, direct, and high-density.

---

## 1. Comparison Table: Turning AI Slop into Human Prose

| Before (AI Tic / AI Slop) | After (Human Prose / Craft Writing) | Why the Change Works |
| :--- | :--- | :--- |
| *"No mundo dinâmico e em constante evolução do desenvolvimento de software, é crucial alavancar uma abordagem holística para mitigar riscos."* | *"Para evitar falhas em produção, teste cada integração antes do deploy."* | Removes empty buzzwords (*mundo dinâmico*, *alavancar*, *holístico*, *crucial*). Goes straight to the action and the real consequence. |
| *"Este framework não é apenas uma biblioteca utilitária; é um testemunho vivo do poder transformador da arquitetura orientada a microsserviços."* | *"O framework fornece mensageria assíncrona com confirmação de entrega via RabbitMQ."* | Removes the *Contrastive Reframe* and the hyperbolic adjectives (*testemunho vivo*, *poder transformador*). Describes the exact technical fact. |
| *"Mergulhe a fundo na tapeçaria intrincada de nossos endpoints RESTful para desbloquear sinergias sem precedentes."* | *"Consulte os endpoints em `/v1/orders` para criar e cancelar pedidos."* | Removes grandiose metaphors (*mergulhe a fundo*, *tapeçaria*, *sinergias*). Uses direct, accessible language. |
| *"É importante ressaltar e ter em mente que o arquivo de configuração `.env` deve ser mantido em absoluto segredo para garantir a segurança."* | *"Nunca versione o arquivo `.env`. Adicione-o ao `.gitignore`."* | Cuts the loose preamble (*é importante ressaltar que*). Uses a command in the direct imperative. |
| *"Em suma, pudemos concluir ao longo deste abrangente documento que a ferramenta desempenha um papel fundamental para os desenvolvedores."* | *(Removed entirely)* | Technical documentation does not need a school-essay conclusion. When the technical instruction ends, the text ends. |

---

## 2. The Law of Rhythm in Practice (Gary Provost)

### ❌ Example of Monotonous AI Rhythm (Sentences of the Same Length):
> *"O gateway de pagamentos recebe a requisição criptografada do cliente web. O serviço de autenticação valida os cabeçalhos de segurança do token JWT. O motor de risco calcula a pontuação probabilística de fraude da transação. O banco de dados relacional registra o evento de autorização financeira. A resposta formatada em JSON retorna para a aplicação consumidora."*
*(Every sentence runs about 15 words. The reader switches off from rhythmic boredom.)*

### ✅ Example of Human Rhythm with Dynamic Variation:
> *"A requisição chega. O gateway intercepta o payload, valida o JWT e delega o scoring ao antifraude em menos de 10ms. Se o risco for aceitável, o banco grava a transação e a API responde imediatamente com `201 Created`. Caso contrário, o pagamento é recusado antes de onerar os serviços centrais."*
*(A surgical alternation between short three-word sentences, mid-length flow sentences, and compound conditional sentences. The reading flows with music and energy.)*

---

## 3. Anti-AI Audit Checklist for Documentation

Before publishing any documentation, run this inspection checklist:

1. **[ ] Does the first paragraph start immediately with technical value?**
   - Remove any introduction such as: *"Neste documento abordaremos..."* or *"Com a crescente complexidade dos sistemas..."*.
2. **[ ] Has the blacklist of AI words been banned?**
   - Zero occurrences of: *delve*, *leverage*, *streamline*, *tapestry*, *landscape*, *crucial*, *vital*, *holistic*, *paradigm*, *foster*, *unleash*, *synergy*, *alavancar*, *cenário atual*, *fundamental*.
3. **[ ] Is there conscious variation in sentence length?**
   - Check that there are no more than three consecutive sentences with the same word count.
4. **[ ] Does the document respect the purity of Diátaxis?**
   - If it is a **How-To**, does it give clear steps without giant theoretical explanations?
   - If it is a **Reference**, are the parameters organized neutrally, without prolix narrative?
5. **[ ] Are the code examples 100% testable and free of magic placeholders?**
   - Are all imports and variables needed to run the snippet declared?
6. **[ ] Do the Mermaid diagrams quote labels containing special characters and avoid a bare `end` word?**
