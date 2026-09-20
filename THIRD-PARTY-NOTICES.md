# Third-Party Notices

Coacus is distributed under [AGPL-3.0](LICENSE). It also contains material
imported from other repositories. Those components remain under their original
licenses, reproduced below as their terms require.

Provenance for every imported file — source repository, commit, path and content
hash — is recorded in [`sources.lock.json`](sources.lock.json)
([provenance standard](docs/standards/provenance.md)).

## Superpowers — MIT

The process workflows under `methodology/workflows/superpowers-*` are derived
from the Superpowers workflow collection by Jesse Vincent
(<https://github.com/obra/superpowers>), imported at commit
`5bf4e78011075bcfc0dc295f0724994cd123ee71`. They are redistributed under the MIT
License, reproduced in full below.

```text
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Skills corpus — GPL-3.0

The skills under `knowledge/skills/**` and the agents under `knowledge/agents/**`
are imported from the `skills` source repository
(<https://github.com/dandgabr/skills>), which is licensed under the GNU General
Public License v3.0. The license text is available in that repository and at
<https://www.gnu.org/licenses/gpl-3.0.txt>.

## Applying this notice

Any redistribution of Coacus, in whole or in part, must retain this file
alongside the imported components. The installer writes a copy to the skills
root of each harness it targets, so an installed corpus carries the same
notices as the repository.
