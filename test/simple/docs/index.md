---
xvar:
    bla: 1
    blub: 2
---

# Hello

{{ cal }}

Serie 1 : {{ cal.s01 }}
Serie 2 : {{ cal.s02 }}

{{ page.meta.xvar.bla }}

{{ page.meta.xvar.blub }}

{{ macros_info() }}
