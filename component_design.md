
## Waveguides

**Requirements**
- SiN WG with SiO2 cladding
- 400nm thickness
- 100nm min feature size?

### Jan 19 2026

![E field amplitude of TE00 mode.](image-2.png)
We see the simulation volume is large enough to allow field to fall off.

![Simulation of neff vs width for first four modes.](image-5.png)
We analyse the 400nm tall SiN waveguide subject to transmitting 810nm light. Focusing on the higher order modes, we see the maximum width for a single mode waveguide is about 500mm.
![Zoomed in.](image-4.png)

This also justifies us to use the provided 450nm width SiN waveguides for 895nm light. I will use this for my designs.

### Jan 22 2026
Todays goal is to optimize and implement GC design using the universal GC model (https://doi.org/10.1117/12.2042185F).  This was done so far by a 2D simulation in FDTD.
![2D FDTD simulation](image-7.png)

In this simulation I swept the followiong parameters as they are found in the universal GC PCell:
 - Pitch
 - Duty Cycle
 - Fibre X pos
 - Input length
 - Output length

Had issues here with optimization and sweeps as the program would crash if my desktop went to sleep. Even persisted as an issue when I disabled going to sleep.

## Jan 30, 2026
Imported proper data from ANT for SiN and SiO2. Re-ran waveguide width sweep and saved effective index values at 450nm width. This sweep shows good confinement up to 410nm width, while at 450nm the effective index for the higher order modes is only 1.495. That is compared to the native refractive index provided by ANT of 1.4759.
![Waveguide width sweep at 810nm](image-6.png)