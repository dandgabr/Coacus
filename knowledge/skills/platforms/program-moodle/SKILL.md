---
name: program-moodle
description: "Acts as a senior specialist in Moodle LMS, covering plugin development and lifecycle (Frankenstyle), core APIs (DB, Form, Page, Output), XMLDB modeling and database tuning, theme design (Mustache/SCSS), large-scale infrastructure (OPcache, MUC Redis/Memcached), and security."
---

# 🎓 Comprehensive Moodle LMS Specialist (program-moodle)

This skill provides rigorous guidelines, architecture standards, and software-engineering best practices for the entire Moodle LMS (Learning Management System) ecosystem.

---

## 🏛️ 1. Frankenstyle Architecture & Plugin Lifecycle

Moodle uses the **Frankenstyle** naming convention (`[plugintype]_[pluginname]`):

```
moodle/
├── mod/               # Módulos de atividades (ex: mod_quiz, mod_assign)
├── block/             # Blocos laterais (ex: block_myoverview)
├── local/             # Plugins locais de customização (ex: local_custom_reports)
├── theme/             # Temas visuais (ex: theme_boost)
└── enrol/             # Métodos de inscrição (ex: enrol_manual)
```

- **Standard Plugin Structure**:
  - `version.php`: Declares `$plugin->version`, `$plugin->requires`, and `$plugin->component`.
  - `lib.php`: Extension functions, callbacks, and hooks.
  - `db/`: `install.xml` (XMLDB table definitions), `upgrade.php`, `access.php` (capabilities).
  - `lang/en/` and `lang/pt_br/`: Internationalization strings.
  - `settings.php`: Administrative settings tree.

---

## 🗄️ 2. Database, XMLDB, and DBA Optimization

- **XMLDB Modeling**: Every Moodle table must be defined via the XMLDB Editor (`db/install.xml`) with rigorous conventions:
  - Primary fields always named `id (int 10, not null, auto-increment)`.
  - Foreign keys with explicit indexes to avoid *Full Table Scans*.
- **Safe Delegated Transactions**:
```php
$transaction = $DB->start_delegated_transaction();
try {
    $DB->insert_record('custom_table', $record1);
    $DB->update_record('other_table', $record2);
    $transaction->allow_commit();
} catch (Exception $e) {
    $transaction->rollback($e);
}
```

---

## 🎨 3. Interface Design, Themes, and Accessibility (UI/UX)

- **Mustache Templates**: Strict separation between rendering logic and presentation (`templates/component.mustache`).
- **SCSS Styling**: Customization in the `scss/preset/default.scss` file by extending the `theme_boost` theme and respecting WCAG 2.1 AA standards.

---

## 🌐 4. Infrastructure, Performance, and MUC (Moodle Universal Cache)

- **PHP OPcache**: Enable `opcache.enable=1`, `opcache.memory_consumption=512`, `opcache.max_accelerated_files=20000`.
- **MUC (Moodle Universal Cache)**: Configure Redis or Memcached for Application and Session caches, slowing down database queries.
- **Batch Cron**: Run `admin/cli/cron.php` via a background process decoupled from the web server.
