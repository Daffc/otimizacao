min : x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 +  x9 + x10 + x11 + x12;

// PROBLEMA ORIGINAL (SINAIS INVERTIDOS PARA QUE LIMITE SEJA SUPERIOR).
// 2 x1 + x2 + x3 >= 97
// x2 + 2 x5 + x6 + x7 + x8 >= 610
// x3 + 2 x6 + x7 + 3 x9 + 2 x10 + x11 >= 395
// x2 + x3 + 3 x4 + 2 x5 + 2 x7 + 4 x8 + 2 x10 + 4 x11 + 7 x12 >= 211

- 2 x1 - x2 - x3 <= - 97;
- x2 - 2 x5 - x6 - x7 - x8 <= - 610;
- x3 - 2 x6 - x7 - 3 x9 - 2 x10 - x11 <= - 395;
- x2 - x3 - 3 x4 - 2 x5 - 2 x7 - 4 x8 - 2 x10 - 4 x11 - 7 x12 <= - 211;