---
name: "lang-powershell"
description: "Provides software engineering patterns in PowerShell (Windows PowerShell 5.1 and PowerShell 7+ Core). Covers automation, object pipeline management, modularization (script modules/manifests), defensive error handling (Try/Catch/Finally, ErrorActionPreference), strong typing, PSCustomObject, and security best practices (ExecutionPolicy, remoting, and credentials)."
---

# AI Skill: PowerShell Engineering (PowerShell Specialist)

This skill guides the AI to act as a specialist in the **PowerShell** ecosystem (supporting both Windows PowerShell 5.1 and PowerShell 7+ Cross-Platform), with a focus on robust, modular, testable scripts with high performance in infrastructure and systems automation.

---

## 🧭 PowerShell Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Object Orientation and Pipeline Usage
- **Return Objects, Not Text**: Avoid formatting output as raw text or using `Write-Host` for structured data. Instead, emit objects using `[PSCustomObject]` or `Write-Output`.
- **`Write-Host` vs `Write-Information` / `Write-Verbose`**: Use `Write-Verbose` for detailed logs, `Write-Warning` for alerts, and `Write-Error` for failures. Avoid `Write-Host` unless you are building a specific interactive console interface.
- **Pipeline-Awareness**: Design advanced functions to accept input via the pipeline (`ValueFromPipeline` or `ValueFromPipelineByPropertyName`).

### 2. Error Handling and Defensive Execution
- **Stop on Errors**: Use `$ErrorActionPreference = 'Stop'` at the top of scripts or use `-ErrorAction Stop` on specific cmdlets to ensure non-critical errors (*non-terminating errors*) are converted into catchable exceptions.
- **Try / Catch / Finally Blocks**: Always wrap calls to native .NET APIs or I/O operations in typed `Try/Catch` blocks:
  ```powershell
  try {
      [System.IO.File]::ReadAllText($filePath)
  } catch [System.IO.FileNotFoundException] {
      Write-Error "Arquivo não encontrado: $filePath"
  } catch {
      Write-Error "Erro inesperado: $_"
  }
  ```

### 3. Advanced Functions and CmdletBinding
- **Use of `[CmdletBinding()]`**: All reusable functions must declare `[CmdletBinding()]` to support common parameters such as `-Verbose`, `-Debug`, `-ErrorAction`, and `-WhatIf` / `-Confirm` (when `SupportsShouldProcess` is implemented).
- **Strict Parameter Validation**: Add validation attributes such as `[ValidateNotNullOrEmpty()]`, `[ValidateSet()]`, or `[ValidateRange()]`.

### 4. Performance and Strong Typing
- **Avoid Array Concatenation (`+=`)**: The `+=` operator recreates the whole array in memory on each iteration. For large collections, use `[System.Collections.Generic.List[PSObject]]` or assign the loop result directly to a variable:
  ```powershell
  $results = foreach ($item in $items) {
      [PSCustomObject]@{
          Id   = $item.Id
          Name = $item.Name
      }
  }
  ```
- **Parameter Typing**: Declare the types of all parameters explicitly (`[string]`, `[int]`, `[switch]`, `[datetime]`) to avoid implicit coercion and unexpected behavior.

### 5. Security and Best Practices
- **Avoid `Invoke-Expression` (iex)**: Never use `Invoke-Expression` with dynamically constructed strings or strings from untrusted sources, to prevent code injection.
- **Credential Management**: Never insert passwords or tokens as plain text (*hardcoded*). Use `[PSCredential]`, the `SecretManagement` module, or secure environment variables.

---

## 🧰 Recommended Code Patterns

### Complete Advanced Function with Pipeline and Validation Support

```powershell
function Get-SystemServiceReport {
    [CmdletBinding(SupportsShouldProcess = $false)]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [string[]]$ServiceName,

        [Parameter(Mandatory = $false)]
        [ValidateSet('Running', 'Stopped', 'All')]
        [string]$StatusFilter = 'All'
    )

    begin {
        Write-Verbose "Iniciando relatório de serviços..."
        $results = [System.Collections.Generic.List[PSCustomObject]]::new()
    }

    process {
        foreach ($name in $ServiceName) {
            Write-Verbose "Processando serviço: $name"
            try {
                $service = Get-Service -Name $name -ErrorAction Stop
                
                if ($StatusFilter -eq 'All' -or $service.Status -eq $StatusFilter) {
                    $results.Add([PSCustomObject]@{
                        ServiceName = $service.Name
                        DisplayName = $service.DisplayName
                        Status      = $service.Status.ToString()
                        StartType   = $service.StartType.ToString()
                        Timestamp   = [DateTime]::UtcNow
                    })
                }
            } catch [Microsoft.PowerShell.Commands.ServiceCommandException] {
                Write-Warning "Serviço não encontrado: $name"
            } catch {
                Write-Error "Erro ao consultar o serviço $name: $_"
            }
        }
    }

    end {
        Write-Verbose "Relatório concluído com $($results.Count) item(ns)."
        return $results
    }
}

# Exemplo de Uso via Pipeline:
# @('wuauserv', 'Spooler', 'NonExistentService') | Get-SystemServiceReport -StatusFilter Running -Verbose
```

### Automation Script with Robustness and Structured Logs

```powershell
# Requires -Version 5.1
$ErrorActionPreference = 'Stop'

function Invoke-MaintenanceTask {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$TargetDirectory,

        [Parameter(Mandatory = $false)]
        [int]$DaysOld = 30
    )

    if (-not (Test-Path -Path $TargetDirectory -PathType Container)) {
        throw [System.IO.DirectoryNotFoundException]::new("O diretório de destino não existe: $TargetDirectory")
    }

    $cutoffDate = (Get-Date).AddDays(-$DaysOld)
    Write-Verbose "Limpando arquivos anteriores a $cutoffDate em $TargetDirectory"

    $filesToRemove = Get-ChildItem -Path $TargetDirectory -File -Recurse | 
        Where-Object { $_.LastWriteTime -lt $cutoffDate }

    $removedCount = 0
    foreach ($file in $filesToRemove) {
        try {
            Remove-Item -Path $file.FullName -Force -ErrorAction Stop
            $removedCount++
            Write-Verbose "Arquivo removido: $($file.FullName)"
        } catch {
            Write-Warning "Falha ao remover $($file.FullName): $_"
        }
    }

    return [PSCustomObject]@{
        TargetDirectory = $TargetDirectory
        FilesEvaluated  = $filesToRemove.Count
        FilesRemoved    = $removedCount
        ExecutionTime   = [DateTime]::Now
    }
}
```

## 🔒 Security Issues and Safe Practices

- **Script Injection (`Invoke-Expression`)**: Avoid using `Invoke-Expression` or `iex` with user input. Use strongly typed objects or pass parameters via a parameterized `ScriptBlock`.
- **Execution Bypasses and EDR**: Remember that the execution policy (`ExecutionPolicy`) is protection against accidents, not a security boundary; attackers can easily bypass it (e.g., `-ExecutionPolicy Bypass`).
- **Hardcoded Secrets**: Never store passwords or tokens in script variables. Use the `SecretManagement` utility or DPAPI encryption (`SecureString`).
