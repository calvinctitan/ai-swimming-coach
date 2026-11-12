# Benchmarks research

## Freestyle

## Elbow catch angle
Convention: inside angle, straight arm = 180 degrees (same as my code).

| Source | Who was measured | Method | Catch angle | Mid-pull angle |
|---|---|---|---|---|
| ERIC paper (EJ1331738) | 7 male age-group swimmers, ~14 yrs, 200m free | 3D, 3 underwater cameras, 60 Hz | 153.11 ± 12.79 | 96.72 ± 13.13 |
| McCabe (2008), Table 4.6, p.116 | 15 male national/international swimmers, ~18 yrs | 3D, 6 cameras, 50 Hz | 151.14 ± 8.65 (sprint group, sprint pace) | 103.18 ± 9.28 (sprint group, sprint pace) |

Sources have data around the same (catch angles differ around 2 degrees, Mid-pull angles differ by around 6.5 degrees).
Both studies used 3D cameras. My system uses 2D video, so my numbers may differ.



## Stroke rate
Cycles per minute. One cycle = right arm + left arm.

| Source | Who was measured | Sprint pace | Distance pace |
|---|---|---|---|
| McCabe (2008), section 4.2.3, p.93 | 15 male national/international swimmers, ~18 yrs | 54.64 ± 5.08 (sprint group), 55.38 ± 3.73 (distance group) | 38.59 ± 6.00 (sprint group), 41.26 ± 3.70 (distance group) |
| Pelayo et al. (1996), via McCabe Table 2.1, p.10 | National/international swimmers in competition | 57.61 ± 4.67 (50m pace) | 44.59 ± 3.34 (400m pace) |


- McCabe's sprint pace = 25m all out sprint. Distance pace = 400m max effort.
- Pelayo labeled its values "strokes/min," but they match full cycles (unconfirmed). I have not read the original paper yet.
- Pelayo is about 2 to 3 cycles/min higher at sprint pace and about 3 to 6 higher at distance pace. This may be due to the reason that the swimmers were measured in different settings: Pelayo in an actual meet while the McCabe is a simulated experiment.
- Pace changes stroke rate by about 15 cycles per minute, still, always record the pace.
- Rejected: Altan et al. (2022), Table 1, p.898. Stroke rate is given in seconds and never defined, can't be converted.


## Sources
- Altan, B. K., Ercin, C. B., Bingul, B. M., Kesepara, F. (2022). *The kinematic analysis of 3 repeated 200 meters freestyle swimming performances of swimmers aged 13-15 years.* International Journal of Curriculum and Instruction. https://files.eric.ed.gov/fulltext/EJ1331738.pdf
- McCabe, C. (2008). *Effects of 50m and 400m Race Paces on Three-Dimensional Kinematics and Linear Kinetics of Sprint and Distance Front Crawl Swimmers.* PhD thesis, University of Edinburgh. https://era.ed.ac.uk/items/e13d92a5-b137-4801-9048-5d62e044c750
- Pelayo, P., Sidney, M., Kherif, T., Chollet, D., Tourny, C. (1996). *Stroking characteristics in freestyle swimming and relationships with anthropometric characteristics.* Journal of Applied Biomechanics, 12(2), 197-206. https://acnpsearch.tweb-dev.unibo.it/singlejournalindex/16851155
