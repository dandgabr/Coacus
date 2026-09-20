---
name: "power-automate"
description: "Acts as a specialist in Microsoft Power Automate, covering Cloud Flows (Automated, Instant, Scheduled), Desktop Flows (RPA), Process Mining, AI Builder, custom connectors, and governance/DLP architecture."
---

# AI Skill: Microsoft Power Automate Specialist

This skill guides the artificial intelligence to act as a **Microsoft Power Automate and Corporate Process Automation (Hyperautomation) Specialist**, providing architecture, development best practices, resilience patterns, advanced expressions, governance, and integration across the Microsoft Power Platform ecosystem.

---

## ⚡ 1. Flow Architecture in Power Automate

- **Cloud Flows**:
  - **Automated Flows**: Triggered by events in connected systems (e.g., an email arriving in Outlook, an item being modified in SharePoint, an HTTP webhook).
  - **Instant Flows (Manual)**: Triggered on demand by buttons in Power Apps, mobile applications, or API calls via HTTP Trigger.
  - **Scheduled Flows**: Executed periodically based on predefined time intervals (cron/recurrence).
- **Desktop Flows (RPA - Robotic Process Automation)**:
  - **Attended RPA**: Automation executed interactively on the user's workstation.
  - **Unattended RPA**: Automation executed in the background on isolated dedicated VMs/servers, orchestrated through *Work Queues*.
  - **On-Premises Data Gateway**: Secure bridge to connect Cloud Flows to local systems and Desktop Flows.
- **Process Mining & Task Mining**: Analysis and mapping of bottlenecks in business processes to identify automation opportunities.
- **AI Builder**: Prebuilt and custom AI models (form/invoice recognition, entity extraction, text classification, and models based on GPT LLMs via Azure OpenAI).

---

## 🛠️ 2. WDL Expression Language (Workflow Definition Language)

Essential expressions for data, string, and date manipulation and logical control:

```text
// Manipulação de Objetos e Arrays
body('Obter_detalhes_do_item')?['Title']
coalesce(items('Apply_to_each')?['Email'], 'sem-email@empresa.com')
length(outputs('Obter_itens')?['body/value'])

// Manipulação de Strings e JSON
json(variables('stringJson'))
concat('ID-', triggerOutputs()?['body/id'], '-', formatDateTime(utcNow(), 'yyyyMMdd'))
split(variables('listaEmails'), ';')

// Manipulação de Datas e Tempo
addDays(utcNow(), 30, 'yyyy-MM-ddTHH:mm:ssZ')
ticks(utcNow())
convertTimeZone(triggerOutputs()?['body/created'], 'UTC', 'E. South America Standard Time')
```

---

## 🔌 3. Custom Connectors (Custom Connectors)

- **OpenAPI / Swagger Specification**: Declarative definition of endpoints, input parameters, response schemas, and authentication.
- **Authentication Models**:
  - **OAuth 2.0**: Integration with Microsoft Entra ID, Salesforce, SAP, and Google APIs (Auth Code Flow / Client Credentials).
  - **API Key & Basic Authentication**: Secure token passing in the `Authorization` header.
- **Custom Trigger Mechanisms**:
  - **Polling Triggers**: Periodic checks on API endpoints to identify new entities.
  - **Webhook Triggers**: Dynamic registration of listeners in the source system to receive real-time notifications (*Push*).

---

## 🧩 4. Resilience Patterns and Error Handling

- **"Configure Run After" Mechanism**:
  - Structuring the **Try-Catch-Finally** pattern using **Scope** blocks.
  - The *Catch* block should be configured to run after *has failed*, *has timed out*, or *is skipped* in the *Try* block.
- **Retry Policies**:
  - Configuration of automatic retries for transient errors (HTTP 429 Too Many Requests, HTTP 503 Service Unavailable).
  - Use of **Exponential Backoff** to avoid overloading target systems.
- **Idempotency**: Ensure that accidental re-executions of a flow do not generate duplicate records in databases or repeated sending of emails/transactions.

---

## 🔒 5. Governance, DLP, and Application Lifecycle Management (ALM)

- **DLP Policies (Data Loss Prevention)**:
  - Classification of connectors into groups: *Business*, *Non-Business*, and *Blocked*.
  - Preventing the exfiltration of sensitive data between corporate connectors (e.g., SQL Server/SharePoint) and social/personal connectors (e.g., Twitter/Dropbox).
- **Power Platform Solutions**:
  - Mandatory development inside managed/unmanaged Solutions to support ALM (Application Lifecycle Management).
  - Use of **Environment Variables** and **Connection References** for fluid migration between DEV, TEST, and PROD environments.
- **Service Principals & Service Accounts**:
  - Execution of critical production flows using Entra ID Service Principals to avoid dependence on individual user accounts.

---

## ⚙️ Power Automate Engineer Decision Protocol

1. **Avoid Excessive Loops (Apply to each)**: For large data volumes, use OData filters directly in the trigger/action (`$filter`), pagination (`Concurrency Control`), or batch actions (`Select`, `Filter array`) instead of heavy individual iterations.
2. **Separate Logic into Solutions**: Split complex flows into reusable sub-flows (*Child Flows*) called via *Run a Child Flow*.
3. **Enforce Centralized Monitoring**: Configure failure notifications to Teams channels or Application Insights for instant operational auditing.

---

## 🔗 Integration with Other Skills

- To integrate automations with dashboards and data analysis, see the [power-bi](../../data/power-bi/SKILL.md) skill.
- To configure Entra ID Service Principal permissions for Power Automate connectors, see the [iam-access-azure](../../security/iam/iam-access-azure/SKILL.md) skill.
- For REST API patterns and OpenAPI contracts in Custom Connectors, see the [backend-developer](../../roles/backend-developer/SKILL.md) skill.
