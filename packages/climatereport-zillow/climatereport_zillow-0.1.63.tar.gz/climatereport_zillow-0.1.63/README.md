# climatereport_zillow

Unlike other real estate sites, Zillow listings do not contain a section on the environmental risk of the property in the listing. This package takes a Zillow url as input and uses it to compile an HTML report on the climate risks of the property in the zillow listing. This report will automatically open after running the function. The report includes data provided by the First Street Foundation, under the the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License. 

## Installation

```bash
$ pip install climatereport_zillow

```

## How to Use
```bash
$ from climatereport_zillow import climatereport_zillow
$ climatereport_zillow.climatereport_zillow("https://www.zillow.com/homedetails/13353-Cavandish-Ln-Moreno-Valley-CA-92553/18008847_zpid/")
```
## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`climatereport_zillow` was created by Darci Kovacs. It is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License
 license. 

## Credits

`climatereport_zillow` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
