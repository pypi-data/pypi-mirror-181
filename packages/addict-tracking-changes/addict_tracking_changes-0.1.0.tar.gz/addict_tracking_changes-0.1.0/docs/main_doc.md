## Usage

### Get and clear history
```python
mydict = Dict()

mydict.a.b.c = 15

for _ in mydict.get_changed_history():
    print(_) 
```
The output
```
/a/b/c
```

Use clear_changed_history method to clear all changed history.

```
mydict.clear_changed_history()
for _ in mydict.get_changed_history():
    print(_)
```
outputs empty. 

### Freeze/unfreeze 
Once a dict is frozen, adding new keys will raise KeyError. 
Although modification to existing keys is allowed 

To freeze:
```
mydict.freeze()
```

To unfreeze:
```
mydict.unfreeze()
```

### pickling
History is lost during pickling dump and load operation. 
To enable tracking after pickle.load, use set_tracker operation.


### Handling dict and list as values of keys
A py-dict is treated as any other opaque value object. 
Hence,
```python
mydict = Dict()

mydict.a.b.c = {'kk': 1}
mydict.a.b.e = {'dd': 1}

for _ in mydict.get_changed_history():
    print(_) 
```
will print paths
```
/a/b/c
/a/b/e
```
and not 
```
/a/b/cc/kk
/a/b/e/dd
```

List values on the other hand are exposed. Addict will walk within the list recursively,
an report all the list location. So, for following Dict with list values:
```
        trackerprop.a.b = [1, [1]]
        trackerprop.a.c = [2, [2, [3]]]
```
get_changed_history will report following paths:
```
            "/a/b/0",
            "/a/b/1/0",
            "/a/c/0",
            "/a/c/1/0",
            "/a/c/1/1/0",
```


