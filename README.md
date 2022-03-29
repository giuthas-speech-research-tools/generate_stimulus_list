# Delayed Naming Stimulus Generation

Stimulus list generation for delayed naming:
- Stimulus lists are generated from block specification files and shuffled while 
  preventing across-block-boundary repeats by resampling.
- Optional beeps with a randomised (or rather shuffled) silent delay are generated into .wav files.
- Lists are written out for AAA (in DOS format) and RASL formats.

## Roadmap

- [ ] Convert stimulus list randomisation from R to Python.
- [ ] Convert beep / delay generation from Matlab to Python.
- [ ] Write exporter to AAA format.
- [ ] Write exporter to RASL format.

- [ ] Include a markdown license file and link to it when there is some actual code here.

## License

GPL 3.0 