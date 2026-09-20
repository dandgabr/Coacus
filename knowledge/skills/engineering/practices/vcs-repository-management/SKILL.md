---
name: vcs-repository-management
description: Acts as a specialist in Version Control Systems (VCS) and advanced repository management. Masters low-level Git (DAG, objects, reflog, worktrees, sparse-checkout, LFS, submodules, bisect, filter-repo), Subversion/SVN (FSFS architecture, trunk/branches/tags, svn:mergeinfo, svn:externals, svnadmin, hooks), Mercurial (Hg), branching strategies (Trunk-based, GitFlow), migration of legacy repositories to Git, and monorepo scalability (Scalar).
---

# 🛠️ vcs-repository-management: Advanced Version Control Engineering and Repository Management

This skill supplies the engineering standards, version-control data architecture, repository administration, and migration techniques across distributed (Git, Mercurial) and centralized (Subversion, Perforce) VCS ecosystems.

---

## 1. Git Fundamentals and Internal Mechanics

### 1.1 Directed Acyclic Graph (DAG) Data Structure
Git is a content-addressable filesystem. All information is stored in the object database (`.git/objects/`) and identified by a cryptographic hash: SHA-1 (40 hexadecimal characters) or SHA-256 (64 hexadecimal characters):
- **`blob` (Binary Large Object)**: Stores only a file's raw data, with no name, permissions, or date.
- **`tree`**: Represents a directory. Maps object identifiers (`blob` or sub-`tree`), POSIX permission modes (`100644`, `100755`, `040000`), and file names.
- **`commit`**: Points to a snapshot's root `tree`, references zero or more parent commits (`parent`), identifies the author and committer (with timestamp and time zone), and contains the explanatory message.
- **`tag` (Annotated)**: A permanent object pointing to a specific commit, containing the tagger, timestamp, message, and optionally a GPG/SSH cryptographic signature.

```text
  [Commit C2] ──── parent ────> [Commit C1]
      │                             │
    tree                          tree
      ▼                             ▼
   [Tree T2]                    [Tree T1]
   ├── blob B1 (modificado)     ├── blob B1 (versão inicial)
   └── tree Sub                 └── blob B2
        └── blob B3
```

### 1.2 The Index (Staging Area) and Commit Mechanism
The index (`.git/index`) is an on-disk binary structure representing the next planned snapshot. Changes move between three fundamental states:
1. **Working Tree**: Files in the local working directory.
2. **Index / Staging**: The intermediate tree prepared via `git add`.
3. **Repository (HEAD)**: The immutable history of snapshots committed on the current branch.

### 1.3 Storage Optimization and Delta Compression (Packfiles)
Git initially stores objects as loose objects (compressed via zlib). When the volume grows, it triggers packing:
- **Packfile (`.pack`)**: A consolidated file where similar objects are stored using delta compression (bidirectional deltas based on the Rabin Fingerprint algorithm).
- **Packfile Index (`.idx`)**: A hash table mapping SHA to exact offsets inside the `.pack`, enabling $O(1)$ lookup.
- **Maintenance Commands**:
  ```bash
  # Verificação de integridade estrutural e objetos órfãos
  git fsck --full --strict
  
  # Repacotamento agressivo com compactação máxima
  git gc --aggressive --prune=now
  git repack -a -d -f --depth=250 --window=250
  ```

---

## 2. Advanced History Manipulation and Forensics

### 2.1 Interactive Rebase and History Cleanup
Refines commits before sharing them with the team, ensuring atomic and descriptive commits:
```bash
# Iniciar rebase interativo dos últimos 5 commits
git rebase -i HEAD~5
```
**Interactive Rebase Commands**:
- `pick`: Keeps the commit unchanged.
- `reword`: Changes only the commit message.
- `edit`: Pauses execution to allow code amendments (`git commit --amend`).
- `squash`: Merges the commit with the previous one, combining the messages.
- `fixup`: Merges the commit with the previous one while discarding the current message (ideal for quick fixes with `git commit --fixup <SHA>`).
- `drop`: Removes the commit from history entirely.

### 2.2 The Reflog (Reference Log) and Disaster Recovery
`git reflog` tracks all branch-pointer and `HEAD` updates over the last 90 days (by default):
```bash
# Inspecionar histórico de movimentações da HEAD
git reflog show HEAD

# Restaurar commit acidentalmente deletado via reset hard
git reset --hard HEAD@{2}

# Resgatar branch deletada a partir do SHA identificado no reflog
git checkout -b branch-restaurada e4a81c2
```

### 2.3 Automated Binary Search Debugging (`git bisect`)
Locates the exact commit that introduced a regression through an $O(\log n)$ binary search over history:
```bash
# Iniciar sessão de bisect
git bisect start
git bisect bad HEAD              # Versão atual está com defeito
git bisect good v2.4.0           # Versão v2.4.0 estava íntegra

# Execução 100% automatizada com script de teste de saída (exit 0 = good, exit != 0 = bad)
git bisect run pytest tests/unit/test_payment.py
```

### 2.4 Forensic Purge with `git-filter-repo`
A modern, safe replacement that is orders of magnitude faster than the obsolete `git filter-branch`:
```bash
# Instalação
pip install git-filter-repo

# 1. Purgar arquivo sensível (.env ou chave privada) de TODO o histórico
git-filter-repo --invert-paths --path secrets.env --path id_rsa

# 2. Purgar arquivos maiores que 50MB que entraram indevidamente no histórico
git-filter-repo --strip-blobs-bigger-than 50M

# 3. Reescrever histórico alterando e-mails ou nomes de autores
git-filter-repo --mailmap my-mailmap.txt
```

---

## 3. Managing Workspaces, Dependencies, and Monorepos

### 3.1 Multiple Working Trees with `git worktree`
Switches context or runs long tests without needing `git stash` or re-cloning the repository:
```bash
# Criar uma worktree isolada para hotfix em diretório paralelo
git worktree add ../hotfix-auth-service hotfix/login-bug

# Listar worktrees ativas
git worktree list

# Remover worktree concluída
git worktree remove ../hotfix-auth-service
git worktree prune
```

### 3.2 Shallow Clones and `sparse-checkout` for Giant Monorepos
For repositories of tens of gigabytes, avoid downloading the full history and trees:
```bash
# Clone sem blobs (baixa apenas a árvore e histórico de commits; blobs baixados sob demanda)
git clone --filter=blob:none https://github.com/org/monorepo.git

# Clone raso com profundidade limitada
git clone --depth=1 --no-single-branch https://github.com/org/monorepo.git

# Sparse-checkout em modo cone (baixa apenas pastas selecionadas)
git sparse-checkout init --cone
git sparse-checkout set services/payment services/auth shared/libs
```

### 3.3 Git LFS (Large File Storage)
Keeps text pointers in Git and large binary files (videos, ML models, datasets) on dedicated storage servers:
```bash
# Inicializar LFS no repositório
git lfs install

# Rastrear extensões de binários
git lfs track "*.onnx" "*.zip" "*.tar.gz" "*.mp4"
git add .gitattributes

# Validar arquivos gerenciados pelo LFS
git lfs ls-files
```

### 3.4 Git Submodules vs. Git Subtree
- **Submodules**: Point to a specific commit of a remote repository via the `.gitmodules` file. Lower coupling, but requires explicit management (`git submodule update --init --recursive`).
- **Subtrees**: Merge another repository's history directly into a subfolder of the main repository without changing clone metadata. Easier for downstream developers (`git subtree add --prefix=vendor/lib https://github.com/org/lib.git main --squash`).

---

## 4. Subversion (SVN) Architecture and Engineering

### 4.1 Centralized Paradigm and FSFS Backend
Unlike Git (where every clone holds the entire history), SVN operates on a centralized client-server model:
- **Atomic Global Revisions**: Each commit increments a global integer revision number ($r1, r2, \dots, rN$) that represents the complete state of the entire filesystem in the server tree.
- **FSFS (Filesystem on Filesystem)**: A flat-file persistence mechanism that groups revisions into shards for high fault tolerance.
- **Peg Revisions vs. Operative Revisions**:
  - `svn cat -r 15 foo.c@10`: Shows the file `foo.c` as it existed in operative revision 15, tracing the lineage of the file named `foo.c` at peg revision 10 (resolving past renames and deletions).

### 4.2 Canonical SVN Directory Convention
```text
meu-projeto/
├── trunk/            # Linha principal de desenvolvimento contínuo (HEAD)
├── branches/         # Bifurcações temporárias para features, manutenções ou releases
│   ├── feature-pix/
│   └── release-2.0/
└── tags/             # Cópias estáticas e congeladas de releases específicos (ex: v1.0.0)
```
In SVN, branches and tags are **cheap copies** (copy-on-write copies) created by the `svn copy` command.

### 4.3 Versioned Properties (`svn:props`)
Versioned metadata attached to files and directories:
- **`svn:ignore`**: The equivalent of `.gitignore`, defining locally ignored patterns.
- **`svn:keywords`**: Expansion of variables in code (for example, `$Id$`, `$Date$`, `$Revision$`).
- **`svn:eol-style`**: Line-ending normalization (`LF`, `CRLF`, or `native`).
- **`svn:externals`**: Maps external repositories or folders inside the local tree (analogous to Git submodules).
- **`svn:mergeinfo`**: Tracks which revision ranges were merged between branches to avoid repeated conflicts.

### 4.4 SVN Repository Administration (`svnadmin`)
```bash
# Criar novo repositório com backend FSFS
svnadmin create /var/svn/repos/financeiro --fs-type fsfs

# Realizar backup completo (dump stream)
svnadmin dump /var/svn/repos/financeiro > backup_financeiro.dump

# Restaurar ou carregar histórico em repositório novo
svnadmin load /var/svn/repos/novo_financeiro < backup_financeiro.dump

# Verificação de integridade do banco FSFS
svnadmin verify /var/svn/repos/financeiro

# Sincronização e espelhamento contínuo entre servidores
svnsync initialize https://svn-mirror.local/repos/financeiro https://svn-master.local/repos/financeiro
svnsync sync https://svn-mirror.local/repos/financeiro
```

### 4.5 SVN Server Hooks
Scripts executed on the server, triggered by commit events and transactional control:
- **`pre-commit`**: Runs inside a transaction before confirmation. It can abort the commit by returning status code != 0 and emitting an error message on `stderr`.
  ```bash
  #!/bin/bash
  # Validação de mensagem de commit não vazia
  REPOS="$1"
  TXN="$2"
  LOGMSG=$(svnlook log -t "$TXN" "$REPOS")
  if [ -z "$LOGMSG" ]; then
      echo "ERRO: Commits sem mensagem explicativa são proibidos." >&2
      exit 1
  fi
  ```
- **`post-commit`**: Runs after confirmation to trigger webhooks, emails, or CI/CD build triggers.

---

## 5. Mercurial (Hg) and Perforce Helix Core

### 5.1 Mercurial (Hg)
- **Revlog Structure**: Stores history in append-only files with an index (`.i`) and data (`.d`), ensuring fast reads and writes.
- **Mutability Phases**:
  - `public`: Publicly shared commits, immutable by default.
  - `draft`: Local commits, still subject to rebase or amendment.
  - `secret`: Private commits that are never propagated during `hg push`.
- **Official Extensions**: `evolve` (distributed history evolution without breaking commits) and `hg-git` (native interoperability with Git remotes).

### 5.2 Perforce Helix Core
- A high-performance centralized system, the standard in game and semiconductor industries for giant multimedia binary files (terabytes).
- Uses **Client Workspaces** mapped to **Depots**, manages changes through numbered atomic **Changelists**, and implements concurrency control with exclusive **File Locking** (`p4 edit` / `p4 submit`).

---

## 6. Interoperability and Migration Between VCS Systems

### 6.1 Bidirectional Bridge with `git-svn`
Lets you use Git's local flexibility on codebases centralized in SVN:
```bash
# Clonar repositório SVN com layout padrão (trunk, branches, tags)
git svn clone --stdlayout --authors-file=authors.txt http://svn.empresa.com/repos/app app-git

# Atualizar base local com novos commits do SVN (rebase limpo)
git svn rebase

# Desenvolver commits locais normalmente no Git
git commit -m "feat: implementa nova rota de pagamentos"

# Publicar commits locais de volta para o repositório SVN
git svn dcommit
```

### 6.2 Full Migration from SVN to Native Git
Canonical procedure for migrating the complete history without losing lineage, branches, or authors:

#### Step 1: Extract and Map SVN Authors to Git
```bash
# Extrair todos os autores únicos do histórico do SVN
svn log -q http://svn.empresa.com/repos/app | awk -F '|' '/^r/ {sub("^ ", "", $2); sub(" $", "", $2); print $2}' | sort -u > svn-authors.txt

# Mapear para o formato: svnuser = Nome Completo <email@empresa.com>
sed -i 's/^\(.*\)$/\1 = \1 <\1@empresa.com>/' svn-authors.txt
```

#### Step 2: Clone via `git-svn`
```bash
git svn clone --stdlayout --authors-file=svn-authors.txt http://svn.empresa.com/repos/app app-migrado
```

#### Step 3: Convert SVN Remote Branches and Tags to Local Git References
```bash
cd app-migrado

# Converter tags remotas em tags reais anotadas do Git
for tag in $(git branch -r | grep 'tags/'); do
    tag_name=$(echo $tag | sed 's/.*tags\///')
    git tag -a -m "Convertido do SVN tag: $tag_name" "$tag_name" "$tag"
    git branch -r -d "$tag"
done

# Converter branches remotas em branches locais rastreáveis
for branch in $(git branch -r | grep -v 'trunk' | grep -v 'tags/'); do
    branch_name=$(echo $branch | sed 's/.*///')
    git branch "$branch_name" "$branch"
    git branch -r -d "$branch"
done
```

#### Step 4: Migrate `svn:ignore` to `.gitignore`
```bash
git svn show-ignore > .gitignore
git add .gitignore
git commit -m "chore: migra propriedades svn:ignore para .gitignore"
```

#### Step 5: Link to the New Git Remote and Publish
```bash
git remote add origin git@github.com:empresa/app.git
git push --all origin
git push --tags origin
```

---

## 7. Governance, Branching Strategies, and Security

### 7.1 Branching Strategies
1. **Trunk-Based Development (Recommended for Modern CI/CD)**:
   - All developers integrate small, frequent changes directly into `main` (or into short-lived branches of $< 1$ day).
   - Use **Feature Flags** to decouple deploy from release and keep the main branch always stable and deployable.
2. **GitFlow (Traditional for Scheduled Release Cycles)**:
   - A structure with long-lived branches: `main` (production) and `develop` (continuous integration).
   - Auxiliary branches: `feature/*`, `release/*`, and `hotfix/*`.

### 7.2 Cryptographic Commit and Tag Signing (GPG & SSH)
Guarantees non-repudiation and prevents committer identity forgery:
```bash
# Configurar assinatura de commits com chave SSH moderna
git config --global user.signingkey "~/.ssh/id_ed25519.pub"
git config --global gpg.format ssh
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Validar assinatura de commits
git log --show-signature -n 5
```

### 7.3 Branch Protection and `CODEOWNERS`
- Configure pull request policies: minimum approvals, required passing CI status checks, and a ban on forced pushes (`force-push`).
- Map mandatory reviewers per domain in `.github/CODEOWNERS`:
  ```text
  # Regras de revisão por path
  *                   @org/core-team
  /services/billing/  @org/billing-engineers
  /infra/             @org/devops-architects
  *.sql               @org/dba-specialists
  ```
