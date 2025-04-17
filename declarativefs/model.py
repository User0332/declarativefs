import os
import shutil
from typing import Callable, TypeVar


class FSObject:
	def __init__(self, *, name: str, permissions: int, owner: str):
		self.name = name
		self.perms = permissions
		self.owner = owner

	def serialize(self, parent_path="./", *, force=False):
		path = os.path.join(parent_path, self.name)

		if self.perms is not None: os.chmod(path, self.perms)
		if self.owner is not None: shutil.chown(path, self.owner)

class Directory(FSObject):
	def __init__(self, *, permissions: int=None, owner: str=None, name: str, children: list[FSObject]=None):
		super().__init__(permissions=permissions, owner=owner, name=name)
		self.children = children if children else []

	def serialize(self, parent_path="./", *, force=False):
		path = os.path.join(parent_path, self.name)

		if (os.path.exists(path)):
			if not force: raise FileExistsError(path)

			shutil.rmtree(path)

		os.mkdir(path)

		for child in self.children:
			child.serialize(path, force=force)

		super().serialize(parent_path)

T = TypeVar('T')

class File(FSObject):
	def __init__(self, *, permissions: int=None, owner: str=None, name: str, content: T | bytes, content_serializer: Callable[[T], str | bytes]=str):
		super().__init__(permissions=permissions, owner=owner, name=name)

		self.content = content
		self.serializer = content_serializer

	def serialize(self, parent_path="./", *, force=False):
		path = os.path.join(parent_path, self.name)

		if (os.path.exists(path)):
			if not force: raise FileExistsError(path)

			os.remove(path)

		if type(self.content) is bytes:
			open(path, "wb").write(self.content)
		else:
			ser_content = self.serializer(self.content)

			if type(ser_content) is bytes: open(path, "wb").write(ser_content)
			elif type(ser_content) is str: open(path, 'w').write(ser_content)
			else: raise ValueError("serializer function must return bytes or str")

		super().serialize(parent_path)

class Symlink(FSObject):
	def __init__(self, *, name: str, target: str):
		self.name = name
		self.target_path = target

	def serialize(self, parent_path="./", *, force=False):
		raise NotImplementedError()