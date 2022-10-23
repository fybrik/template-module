# template-module

This is a [template github repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) that helps make a fybrik module faster and easier.

## Requirements:

+ `python 3.8+`
+ `jinja` lib installed (`pip install jinja`)

## Usage:

1. Create a template with the green button at the top "Use this template" [(more detailed explaination)](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

2. Change `config.json` to your desired module configuration with the fields given.

`config.json` is set at the begining as an example to match [delete-module](https://github.com/fybrik/delete-module)

3. Create the new module with: 
```
python3 traverse.py
```

4. If all the files were created correctly, clean up the tempalte files with:
```
rm -r template-files traverse.py config.json
```