# DeclarativeFS

A Python library for declaring and serializing filesystem structures declaratively.

Currently, `declarativefs` supports creating basic filesystem structures using a declarative, tree-like syntax.

Configuration/object deserialization/data loading support may be added in the future.
Filesystem schema validation support may be added in the future.

### Example: Creating a Complex Filesystem Structure

```py
import json
import pickle
from declarativefs import *

structure = Directory(
	name="test",
	children=[
		Directory(name="subdir"),
		File(
			name="text.txt",
			content="some text content"
		),
		File(
			name="data.json",
			content={
				"key": "value",
				"num": 12,
				"nested": {
					"values": [12, 6, None, False, "hello"],
					"true": False
				}
			},
			content_serializer=lambda obj: json.dumps(obj, indent=1)
		),
		File(
			name="pickled.obj",
			content=object(),
			content_serializer=pickle.dumps
		)
	]
)

structure.serialize(force=True)
```

The above code will result in a structure that looks like the following:
```
test/
├── subdir/
├── text.txt (contains ASCII text)
├── data.json (contains JSON data)
└── pickled.obj (contains a pickled Python object)
```