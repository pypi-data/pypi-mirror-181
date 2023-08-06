# Ofjustpy programming paradigm
When building a webapp, the
first goal is  to build
what is called document-object-model or DOM tree. The browser engine will
use this DOM-tree to render out the webpage. 

## Background
### DOM tree
In its simplest sense, a DOM tree is collection HTML components
arranged in a tree structure which is defind using parent-child
relationship between components.

## Object-oriented/imperative vs. functional way towards building a DOM tree
In Justpy, and most other object-oriented/imperative programming,
express the DOM tree in a imperative object-oriented style.
Here, one would create a button object (an instance of Button type)
and add it to some  parent component (another instance some html component type):
```python
mybtn = Button(a=parent)
```
.
The html equivalent for the above statement is
```html
<parent>
<button>
</button>
</parent>
```
Two points to note here:
the creation of button instance is coupled/tied to building the DOM tree (or a link of the tree).


Ofjustpy doesn't follow the classic object-oriented impreative style.
Instead ofjustpy follows a functional paradigm, 
where  object instantiation is decoupled from DOM creation.

### Functional approach for DOM tree: Stubs and containers
In Ofjustpy, instead of creating an instance of a component type, you
first  create/instantiate a component `stubs`.
What are component `stubs`? Stubs are functions that when invoked will generate the
respective component. 
We follow the convention that capital letter name with "_" suffix referes to stub generators
while names starting with small letters and ending with "_" suffix is the stub.
The code example below  illustrates this with example:
```python
button_ = oj.Button_("mybtn", text="Submit")
```
Here `oj.Button_` is a stub generator while `button_` is the generated stub.

Once we have generated the stubs, we can define parent-child relationship to build the 
the DOM tree. 
In ofjustpy, stub generator functions
have an argument called `cgens`.  The cgens takes in the list/iterator
over stubs that will the child components of that component. 
As example to illustrate:
```python
lots_of_buttons = [oj.Button_(f"btn_{i}",
                              ...
                              )
                   for i in range(0,10)
                              ]
oj.Div_("buttonpanel", cgens = logs_of_buttons)                              
```

In the above code, ofjustpy will create 10 buttons and
make them child of a Div component.


### The ofjustpy component zoo
Lets briefly familiarze with types of component present in current ofjustpy ecosytem.
We have all the usual


