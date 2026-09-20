---
name: "lang-perl"
description: "Provides software engineering patterns in modern Perl (Perl 5.30+). Covers strict use of pragmas (use strict; use warnings; use utf8;), subroutines with signatures, modern Object Orientation (Moo/MooX or Perl 5.38+ builtin class), defensive regular expressions, safe file handling with lexically scoped filehandles, and CPAN best practices."
---

# AI Skill: Perl Engineering (Perl Specialist)

This skill guides the AI to act as a specialist in the **Perl** language (with a focus on **Modern Perl**, version 5.32+ and 5.38+), promoting clean, safe, maintainable, and idiomatic code, and eliminating legacy habits from "archaic Perl 4/5" code.

---

## 🧭 Perl Development Guidelines

While working under this skill, apply the following patterns strictly:

### 1. Mandatory Pragmas and Modern Features
- **Strict and Safe**: EVERY script or module must start by enabling strict compile-time checking and warnings:
  ```perl
  use strict;
  use warnings;
  use utf8;
  ```
- **Enabling Modern Features (`use v5.36;`)**: In modern Perl versions, prefer using `use v5.36;` or `use v5.38;`, which already enable `strict`, `warnings`, and features such as `signatures` (function signatures) and `state`.

### 2. Subroutine Signatures
- **Avoid Manual `@_`**: Replace the traditional unpacking `my ($self, $foo) = @_` with native subroutine signatures:
  ```perl
  use v5.36;

  sub calculate_total ($price, $tax_rate = 0.05, $discount = 0) {
      return ($price * (1 + $tax_rate)) - $discount;
  }
  ```

### 3. File I/O and Defensive Data Handling
- **Lexical Filehandles and 3-Argument `open`**: Always use the three-argument form of the `open` function combined with `my`-scoped variables:
  ```perl
  open(my $fh, '<:encoding(UTF-8)', $filename)
      or die "Não foi possível abrir '$filename': $!";
  ```
- **Using `autodie` or Error Handling**: Use `use autodie;` in automation scripts to avoid repetitive `or die` checks on file and system operations.

### 4. Modern Object Orientation (Moo / Perl 5.38 Class)
- **Moo / Moose**: For established projects, use `Moo` (or `Moose`) for OOP based on declarative attributes, automatic constructors, and roles:
  ```perl
  package App::Model::User;
  use Moo;
  use namespace::autoclean;

  has id       => (is => 'ro', required => 1);
  has username => (is => 'rw', required => 1);
  has email    => (is => 'rw');

  sub is_active ($self) {
      return defined $self->email && length($self->email) > 0;
  }

  1;
  ```
- **Native `class` Feature (Perl 5.38+)**: When on Perl 5.38+ environments, use the new native `feature 'class'` syntax.

### 5. Readable and Defensive Regular Expressions
- **`/x` Modifier (Extended Regex)**: Write complex regexes across multiple commented lines using the `/x` modifier:
  ```perl
  if ($input =~ /
      ^                     # Início da linha
      (?<area_code> \d{3} ) # Código de área (3 dígitos)
      -
      (?<number>    \d{7} ) # Número principal (7 dígitos)
      $                     # Fim da linha
  /x) {
      my $area = $+{area_code};
  }
  ```

---

## 🧰 Recommended Code Patterns

### Modern CLI Script for Batch File Processing

```perl
#!/usr/bin/env perl
use v5.36;
use autodie;
use Path::Tiny;
use Getopt::Long qw(GetOptions);

# Declaração de Opções
my $input_dir  = '.';
my $output_file = 'report.csv';
my $verbose     = 0;

GetOptions(
    'dir|d=s'    => \$input_dir,
    'output|o=s' => \$output_file,
    'verbose|v'  => \$verbose,
) or die("Erro nos argumentos passados da linha de comando.\n");

sub process_log_file ($file_path) {
    say "Processando: $file_path" if $verbose;
    
    my $file = path($file_path);
    my @lines = $file->lines_utf8({ chomp => 1 });
    
    my $matched_count = 0;
    for my $line (@lines) {
        if ($line =~ /ERROR|CRITICAL/i) {
            $matched_count++;
        }
    }
    
    return {
        filename => $file->basename,
        errors   => $matched_count,
        size     => $file->stat->size,
    };
}

sub main () {
    my $dir = path($input_dir);
    die "Diretório inexistente: $input_dir\n" unless $dir->is_dir;

    my @results;
    my $iterator = $dir->iterator({ recurse => 0 });

    while (my $path = $iterator->()) {
        next unless $path->is_file && $path->basename =~ /\.log$/;
        push @results, process_log_file($path);
    }

    # Gravando relatório CSV de saída
    my $out_fh = path($output_file)->openw_utf8;
    $out_fh->say("Filename,ErrorCount,SizeBytes");

    for my $res (@results) {
        $out_fh->say(sprintf("%s,%d,%d", $res->{filename}, $res->{errors}, $res->{size}));
    }

    say "Relatório gerado com sucesso em: $output_file";
}

main();
```

### Object-Oriented Class with `Moo` and Attribute Validation

```perl
package Services::PaymentProcessor;
use Moo;
use Types::Standard qw(Str Num BoolObject InstanceOf);
use namespace::autoclean;
use v5.36;

# Atributos declarativos tipados
has api_key => (
    is       => 'ro',
    isa      => Str,
    required => 1,
);

has sandbox_mode => (
    is      => 'ro',
    isa     => BoolObject,
    default => sub { 1 },
);

has timeout => (
    is      => 'rw',
    isa     => Num,
    default => 30.0,
);

# Método público usando assinaturas
sub process_transaction ($self, $amount, $currency = 'USD') {
    die "Valor da transação deve ser maior que zero" if $amount <= 0;

    my $endpoint = $self->sandbox_mode
        ? 'https://sandbox.api.payment.com/v1/charge'
        : 'https://api.payment.com/v1/charge';

    say sprintf("Enviando cobrança de %.2f %s para %s (Timeout: %.1fs)...",
        $amount, $currency, $endpoint, $self->timeout);

    # Simulação de resposta da API
    return {
        success        => 1,
        transaction_id => 'TXN-' . int(rand(1_000_000)),
        amount         => $amount,
        currency       => $currency,
    };
}

1;
```

## 🔒 Security Issues and Safe Practices

- **Injection in `open()`**: Never use the two-argument syntax of the `open` function (e.g., `open(FH, "$file")`). Always prefer the three-argument syntax `open(my $fh, '<', $file)` to avoid accidental command execution.
- **Taint Mode Bypass**: Always enable Taint Mode (`-T`) in Perl scripts exposed to the internet or CGI to mark external input as unsafe until it is cleaned via regular expressions.
- **Regular Expression Denial of Service (ReDoS)**: Avoid nested regex patterns with complex quantifiers that could cause catastrophic exponential backtracking.
