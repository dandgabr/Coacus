# Integration and Lifecycle

## Asset ownership

Reuse the project's package manager, lockfile and established asset pipeline. The core package supplies compiled styling and behavior; inspect its contents before adding another Bootstrap runtime or stylesheet. Optional charts, selects, maps and editors are separate selections with their own licenses and loading costs. A bundled example does not authorize adding every plugin.

Prefer the existing local asset strategy. If a CDN is appropriate to the requested delivery, use an exact resolved package pin and integrity hash computed for those exact bytes, with the required cross-origin setting. Never transfer a hash to another release. Preserve standalone/offline requirements when they apply.

## Server rendering and dynamic views

Keep browser-dependent initialization out of server module evaluation and render functions. Load browser behavior on the client, after the owning elements exist. Verify the selected package's actual exports before choosing an initialization API.

For each tooltip, popover or other DOM-managed instance, identify its owner element and retain a reference to the owned instance. Repeated mounting must not create duplicate instances or listeners. On unmount or route replacement, dispose owned instances and cancel pending initialization. If an asynchronous import completes after unmount, do not initialize against a stale element.

Use automatic initialization only when its timing covers the actual dynamic elements. Do not combine automatic and manual initialization without checking duplication. A documented startup example is not evidence of correct route-change cleanup.

Test initial render, mount, unmount and remount; count owned instances/listeners where observable and exercise the user-visible behavior. Verify that SSR does not access browser globals. A successful build alone does not prove cleanup.

Use the existing [state and resource ownership procedure](../../../roles/frontend-developer/references/interface-state-lifecycle.md).

Sources reviewed 2026-10-28:
- [React integration guide](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/docs/content/ui/getting-started/frameworks/react.mdx).
- [Next.js integration guide](https://github.com/tabler/tabler/blob/7ec9589ba63da56be273a12d9da9b9dfce59f5ee/docs/content/ui/getting-started/frameworks/nextjs.mdx).

These sources establish integration examples, not a tested reusable lifecycle implementation.
