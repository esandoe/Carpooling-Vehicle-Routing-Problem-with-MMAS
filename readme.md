### Carpooling modified MMAS
#### Overview:
- Main.py: runs single simulation
- MultiMain: runs many simulations and plots results.
    - progress is not reported, so larger simulations (iterations or simulations > 100) may take a while, depending on the hardware.
    - the number of processor threads can be adjusted by a single variable, adjust it according to your hardware and preferences.
- data.py: contains all datasets used in report
- mapgen.py: very primitive file used to generate datasets.