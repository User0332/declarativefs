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