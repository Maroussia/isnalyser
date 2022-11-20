[![PyPI 
version](https://img.shields.io/badge/pypi%20package-0.0.1-brightgreen)](https://img.shields.io/badge/pypi%20package-0.0.1-brightgreen)
[![Contributions 
welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Maroussia/isnalyser/blob/master/README.md)
[![GitHub 
license](https://img.shields.io/badge/license-GNU-orange)](https://github.com/Maroussia/isnalyser/blob/master/LICENSE)

# Automated isnād tree visualisations

For scholars studying Ḥadīth texts, drawing an __isnād__ tree with more than 40 transmitters is a tedious work and finding the right medium to desplay it fully can even prove to be impossible. The `isnalyser` is a simple program for the automation of __isnād__ trees drawing and their customisable display in handy formats.


  <img src="https://user-images.githubusercontent.com/12030245/95599970-13c1dc00-0a52-11eb-96e9-f9969fdd572f.png" width="350">



## The motivation behind the project

The `isnalyser` aims at facilitating the analysis of large quantity of __aḥādīth__ and more specifically their chains of transmiters or __asānid__ by allowing scholars to visualise these chains of transmitters quickly in a complete graph that includes geo-spatial and chronological information.

## Who is it for?

The `isnalyser` is open-source and publicly available. It is meant for scholars in Ḥadīth studies who are analysing a great number of __aḥādīth__ and need to visualise their chains of transmitters in a single graph. The program can also be used by any scholars in Islamic studies or else who want to visualise the transmission of a text or its recension history. All data that follows the pattern of numerous chains of transmitters/scribes/citations/etc. can serve as input for the present program. 

## How?

The `isnalyser` can be installed easily and is ready to use within seconds following the instructions below. The input data consist of two relational databases, containing the transmitters on the one hand, and the transmission path on the other. See the section **Usage** below for indications about where to find examples.

### Installation
```bash
pip install isnalyser
```
### Usage
- A nice function of isnalyser is *view_graph*. Let's import it!

```python
from isnalyser import view_graph
```
- Now, if you already **have some data** available that you want to display as an isnād tree, you can use the function we just imported with the following lines:

```python
view_graph(
	'/path/to/your/data/transmitters.csv', # path to transmitters table in .csv format
	'/path/to/your/data/transmissions.csv', # path to transmissions table in .csv format
	15) # step size of timeline
```

- If you **don't have any data yet**, or just want to get an idea of how the `isnalyser` draws isnād trees, we provided some examples. By looking at them, you can also find out how the data needs to be structured for the `isnalyser` to work.

```python
view_graph(
	'', # you can write anyting here, as we don't need it
	'', # same is true here
	15, # step size of timeline, change the number if you want to see how it affects the graph
	use_example=True) # use example data
```
- Practical examples
Besides the example data furnished in this repository (isnalyser/isnalyser/example_data/), the isnalyser was used in a recent publication which is available here: 

https://brill.com/view/journals/ils/28/3/article-p125_125.xml?language=en&ebody=figures

It comes from the following article by Omar Anchassi:

Anchassi, Omar. Status Distinctions and Sartorial Difference: Slavery, Sexual Ethics, and the Social Logic of Veiling in Islamic Law, Islamic Law and Society, 2021, 28(3), 125-155. https://doi.org/10.1163/15685195-bja10008

This example will give you an idea of the type of output you can expect from the `isnalyser`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.