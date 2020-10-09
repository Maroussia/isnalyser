# What?

- TODO: Introduce Hadith


  <img src="https://user-images.githubusercontent.com/12030245/95599970-13c1dc00-0a52-11eb-96e9-f9969fdd572f.png" width="350">



## Why?

- TODO: Give motivation


## Who is it for?
- TODO: detail target group



## How?

Isnalyser can be installed easily and is ready to use within seconds.

### Installation
```bash
pip install isnalyser
```
### Usage
- A nice function of isnalyser is *view_graph*. Let's import it!

```python
from isnalyser import view_graph
```
- Now, if you already **have some data** available that you want to display as an Isnad tree, you can use the function we just imported like so:

```python
view_graph(
	'/path/to/your/data/transmitters.csv', # path to transmitters file
	'/path/to/your/data/transmissions.csv', # path to transmissions file
	15) # step size of timeline
```

- If you **don't have any data yet**, or just want to get a feel for it, we provided some examples. By looking at them, you can also find out how the data needs to be structured for isnalyser to work.

```python
view_graph(
	'', # you can write anyting here, as we don't need it
	'', # same is true here
	15, # 15 is a good step size for the example
	use_example=True) # use example data
```



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
