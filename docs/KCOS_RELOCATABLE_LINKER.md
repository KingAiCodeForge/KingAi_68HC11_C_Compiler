# KCOS relocatable modules and multi-file linking

Compiler package version: **0.4.0**

This document describes the software-only relocatable-object path added for KCOS modules. It does not require an ECU, PCM, bench harness, or emulator to compile and link modules.

## Pipeline

```text
module_a.c -> parser/codegen -> module_a.k11o --\
                                               \
module_b.c -> parser/codegen -> module_b.k11o ----> hc11kcos linker -> linked ASM/BIN/S19/listing
                                               /
resource-map.json -----------------------------/
```

A `.k11o` file is KingAI's JSON relocatable container, not ELF or COFF. It stores:

- format magic/version and KCOS ABI
- module name and target profile
- SHA-256 of the source translation unit
- symbolic HC11 assembly with no program `ORG`
- exported and imported symbols
- RAM/zero-page resource requests

The linker assigns RAM/ZP addresses, resolves external symbols, chooses a collision-free ROM placement, emits the assignment `EQU` symbols, then runs the normal two-pass HC11 assembler.

## CLI

Compile one translation unit:

```text
python hc11kcos.py compile kcos_scheduler.c --target vy_v6 -o kcos_scheduler.k11o
```

Inspect object metadata:

```text
python hc11kcos.py inspect kcos_scheduler.k11o
```

Link objects:

```text
python hc11kcos.py link kcos_scheduler.k11o kcos_events.k11o \
    --resource-map vy_kcos_map.json \
    --map-out linked.map.json \
    -o kcos.bin
```

Compile and link several C files in one command:

```text
python hc11kcos.py build kcos_scheduler.c kcos_events.c kcos_math.c \
    --target vy_v6 \
    --resource-map vy_kcos_map.json \
    --objects-dir build/objects \
    --map-out build/linked.map.json \
    -o build/kcos.s19
```

Emit a target's default resource map:

```text
python hc11kcos.py map --target vy_v6 -o vy_kcos_map.json
```

Output format is inferred from `.bin`, `.s19`/`.srec`, `.lst`, or `.asm`, or selected with `--format`.

## Link-time guards

The linker stops before producing a final image when it finds:

- duplicate public exports
- unresolved imports
- function/data symbol-kind mismatch
- duplicate module names, which would collide static namespaces
- target-profile mismatch
- KCOS ABI mismatch
- malformed/unsupported object version
- RAM/ZP requests that do not fit
- RAM/ZP/ROM overlap with any reserved or previously allocated physical range
- a relocatable object containing an absolute `ORG`
- a relocation that unexpectedly changes the assembled image size

Code from all objects is emitted as one contiguous ROM allocation. Global and static data requests are individually allocated.

## Resource-map format

Addresses can be decimal integers, `0x...`, or `$...` when supplied as strings. Region ends are inclusive.

Example:

```json
{
  "format": "k11-resource-map",
  "version": 1,
  "regions": [
    {"name": "zero_page", "kind": "zp", "start": "0x0040", "end": "0x00FF", "alignment": 1},
    {"name": "kcos_ram", "kind": "ram", "start": "0x0100", "end": "0x03FF", "alignment": 1},
    {"name": "kcos_rom", "kind": "rom", "start": "0x9000", "end": "0xBFFF", "alignment": 2}
  ],
  "allocations": [
    {
      "name": "factory_owned_ram",
      "kind": "ram",
      "start": "0x0100",
      "size": 64,
      "module": "base_image",
      "reserved": true
    }
  ]
}
```

Regions may overlap logically. Collision checking is physical/global, so the same byte cannot be allocated twice through different pools.

## Register and stack ABI

Normal compiled C functions use:

- `A` for 8-bit results and working values
- `D` (`A:B`) for 16-bit results and working values
- `X` as caller-clobbered transient pointer/index scratch
- `Y` as a stable callee-preserved function-frame pointer
- arguments pushed right-to-left
- caller cleanup of arguments
- 8-bit return in `A`
- 16-bit/pointer return in `D`

The callee reserves its entire local frame once in the prologue. Local accesses therefore remain stable while temporary values or call arguments are pushed. This removes the previous moving-`TSX` local-address problem and leaves `X` available for arrays, pointers and struct-member addressing.

## Arrays

Implemented subset:

- fixed one-dimensional arrays declared as `type name[N]`
- `N` from 1 through 255
- global and local arrays
- char/int/pointer/previously-defined struct element types
- array-to-pointer decay in expressions
- indexed scalar loads and stores
- element-size scaling for indexing
- `sizeof(array)`

Deliberate limits:

- no multidimensional arrays yet
- no aggregate initializer syntax yet
- no whole-array assignment/copy
- dynamic indexing uses an 8-bit index value, hence the 255-element bound

## Structs

Implemented subset:

- named definitions: `struct Foo { ... };`
- named forward declarations
- packed byte layout with deterministic field offsets
- scalar and fixed-array fields
- struct globals and locals
- struct pointers
- `object.member` and `pointer->member`
- scalar member loads and stores
- `sizeof(struct Foo)`

Deliberate limits:

- no implicit padding/alignment is inserted
- no anonymous structs/unions/bitfields
- no whole-struct assignment, return or by-value parameter ABI yet
- no aggregate initializers

Packed layout is intentional for the current embedded subset; code that must match an external binary layout should still use explicit field widths and verify offsets.

## Static symbols

In relocatable mode, file-local functions and globals are rewritten into a module-qualified assembly namespace. They therefore cannot collide with static symbols of the same C name in another object.

Public definitions remain unmangled and enter the export table.

## Interrupt vectors

A relocatable object containing compiler-owned interrupt-vector output is currently rejected. Vector slots have global ownership and require an explicit link policy rather than allowing each translation unit to emit `ORG $FFD6` independently.

KCOS ISR code can be compiled as ordinary callable code, but binding a hardware vector remains an explicit final-image step until vector records are added to K11O.

## Software verification

The new regression suite covers:

- array and struct scalar code generation
- local Y-frame stability
- K11O serialization round-trip
- cross-module function resolution
- RAM and zero-page allocation without overlap
- duplicate-export rejection
- unresolved-import rejection
- RAM exhaustion
- reserved ROM-hole avoidance

These tests validate software behavior only. They do not claim ECU runtime validation.
