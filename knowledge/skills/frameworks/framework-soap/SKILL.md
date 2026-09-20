---
name: "framework-soap"
description: "Provides engineering and integration patterns for web services based on the W3C SOAP 1.1/1.2 and WSDL 1.1/2.0 standards. Covers the XML Envelope structure, message security with WS-Security (WSS), digital signatures (XML-Signature), XSD validation, and enterprise integration."
---

# AI Skill: SOAP Service Engineering and Integration (framework-soap)

This skill guides the AI to act as a specialist in the message-oriented communication protocols **SOAP (Simple Object Access Protocol)** and **WSDL (Web Services Description Language)** service definitions, aligned with the W3C recommendations ([w3.org/TR/soap/](https://www.w3.org/TR/soap/)) and the WS-* specifications. It covers legacy enterprise integrations, banking, XML schema governance, and message security standards.

---

## 🧭 SOAP Message Structure and WSDL Contract

### 1. SOAP Envelope Structure (1.1 / 1.2)
Every SOAP message must be a valid XML document structured into an `Envelope`, an optional `Header` (used for credentials and WS-Addressing), and a `Body` containing the method data or the error (`Fault`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:web="http://services.empresa.com/banking">
   <soapenv:Header>
      <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
         <wsse:UsernameToken>
            <wsse:Username>usuario_api</wsse:Username>
            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">senha_segura</wsse:Password>
         </wsse:UsernameToken>
      </wsse:Security>
   </soapenv:Header>
   <soapenv:Body>
      <web:ConsultarSaldoRequest>
         <web:NumeroConta>123456-7</web:NumeroConta>
      </web:ConsultarSaldoRequest>
   </soapenv:Body>
</soapenv:Envelope>
```

### 2. Contract-First Development (WSDL & XSD)
- Develop strict contracts in **WSDL** defining `types`, `message`, `portType` (or `interface`), `binding`, and `service`.
- Define complex data types in separate **XSD (XML Schema Definition)** schemas for reuse and strong validation in the XML parser before business logic runs.

---

## 🔒 Enterprise Message Security (WS-Security)

Unlike REST/gRPC, which rely primarily on transport-level TLS, SOAP supports encryption and security signing at the **message level** (WS-Security):

- **UsernameToken Profile**: User authentication and password digest hash in the `Header`.
- **X.509 Certificate Token Profile**: Use of asymmetric keys for digital signatures (`XML-Signature`) on specific parts of the `Body` for non-repudiation.
- **XML Encryption**: Encryption of specific message nodes for secure traffic across multiple intermediary proxies (ESBs).

---

## 🚨 Error Handling with SOAP Fault

Errors during processing must return the standardized `<soapenv:Fault>` structure inside `<soapenv:Body>`:

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Body>
      <soapenv:Fault>
         <faultcode>soapenv:Client</faultcode>
         <faultstring>Número de conta inválido ou não encontrado</faultstring>
         <faultactor>http://services.empresa.com/banking</faultactor>
         <detail>
            <err:ErrorDetail xmlns:err="http://services.empresa.com/errors">
               <err:ErrorCode>ACCOUNT_NOT_FOUND</err:ErrorCode>
            </err:ErrorDetail>
         </detail>
      </soapenv:Fault>
   </soapenv:Body>
</soapenv:Envelope>
```

---

## 🔗 Integration with Other Skills

- For enterprise integration architecture (ESB, legacy, and banking systems), see [backend-developer](../../roles/backend-developer/SKILL.md), [financial-transaction-processing](../../domains/industry/financial-transaction-processing/SKILL.md), and [software-architect](../../roles/software-architect/SKILL.md).
- To audit vulnerabilities in SOAP and XML services (XXE, XML Bomb, WS-Security bypass), see [pentester-owasp-wstg](../../security/appsec/pentester-owasp-wstg/SKILL.md) and [appsec-owasp-asvs](../../security/appsec/appsec-owasp-asvs/SKILL.md).
