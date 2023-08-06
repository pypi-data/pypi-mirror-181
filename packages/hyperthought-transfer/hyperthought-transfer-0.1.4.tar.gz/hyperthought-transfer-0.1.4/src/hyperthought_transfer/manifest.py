"""
Define functionality to write to and read from manifest files.

See the Manifest class.
"""

from collections.abc import Sequence
from copy import deepcopy
import json
import multiprocessing
import os

import hyperthought as ht

from . import utils


class PathNotFoundException(Exception):
    pass


def _compute_hash_and_end_bytes(data):
    """
    Compute file hash and end bytes for a file.

    Called from Manifest._compute_file_info_with_pool.
    (Must be defined outside the class.)

    Parameters
    ----------
    data : dict
        Contains keys 'id" and 'path'.

    Returns
    -------
    A dict containing 'id', 'hash', and 'end_bytes'.
    """
    return {
        "id": data["id"],
        "hash": utils.get_hash(data["path"]),
        "end_bytes": utils.get_end_bytes(data["path"]),
    }


class Manifest:
    """
    File transfer manifest.

    Maintains data on job, paths (files and folders to be transferred),
    parsers, and metadata.

    Parameters
    ----------
    job_name : str
        The name of the job.  Conventionally, [SOURCE_COMPUTER]_[DATETIME].
    username : str
        The HyperThought username of the user making the upload request.
    workspace_alias : str
        The alias of the workspace to which the files will be uploaded.
    ignore_path : str or None
        The (beginning) part of each path that will not be duplicated in
        HyperThought.
    hyperthought_root : str
        Human-readable path to the root HyperThought folder.
        Ex:
            For a file `/a/b/c/d.txt`, ignore_path `/a/b`, and
            hyperthought_root `/x/y`, the path to the file after upload
            will be `/x/y/c/d.txt`.
    """
    def __init__(self, job_name, username, workspace_alias,
                 ignore_path=None, hyperthought_root="/"):
        if not job_name or not isinstance(job_name, str):
            raise ValueError("job_name must be a non-empty string")

        if not username or not isinstance(username, str):
            raise ValueError("username must be a non-empty string")

        if not workspace_alias or not isinstance(workspace_alias, str):
            raise ValueError("workspace_id must be a non-empty string")

        if ignore_path is not None and not os.path.isdir(ignore_path):
            raise ValueError(
                "ignore_path_prefix must be a directory if provided")

        if (
            not hyperthought_root
            or
            not isinstance(hyperthought_root, str)
        ):
            raise ValueError("hyperthought_root must be a string")

        if not hyperthought_root.startswith("/"):
            raise ValueError("hyperthought_root must start with '/'")

        self._job_name = job_name
        self._username = username
        self._workspace_alias = workspace_alias
        self.ignore_path = utils.clean_path(ignore_path)

        if self.ignore_path:
            self._ignore_path_token_count = (
                len(self.ignore_path.split(os.path.sep))
            )
        else:
            self._ignore_path_token_count = 0

        self._hyperthought_root = hyperthought_root

        # Common metadata will always be a list of MetadataItem objects.
        self._common_metadata = []

        # Lookup graph.
        # After stripping the path prefix and tokenizing path names,
        # the result is a graph/dictionary with tokens as keys and
        # dictionaries containing 'id', 'type', 'children', 'size', 'hash',
        # and 'end_bytes' as values.
        self._path_graph = {}

        # Map of ids to graph nodes.
        self._id_to_node = {}

        # Data on parsers and metadata.  Used for fast lookup.
        self._parsers = []
        self._metadata = []

    @property
    def common_metadata(self):
        return deepcopy(self._common_metadata)

    @common_metadata.setter
    def common_metadata(self, metadata):
        self._validate_metadata(metadata)
        self._common_metadata = deepcopy(metadata)

    @property
    def parsers(self):
        return deepcopy(self._parsers)

    @property
    def metadata(self):
        return deepcopy(self._metadata)

    @property
    def ignore_path(self):
        return deepcopy(self._ignore_path)

    @ignore_path.setter
    def ignore_path(self, ignore_path):
        self._ignore_path = utils.clean_path(ignore_path)

    def _validate_metadata(self, metadata):
        """Make sure metadata is a list of MetadataItem objects."""
        if not isinstance(metadata, Sequence) or isinstance(metadata, str):
            raise ValueError("metadata must be a non-string sequence")

        for item in metadata:
            if not isinstance(item, ht.metadata.MetadataItem):
                raise ValueError(
                    "all elements of metadata must be instances of "
                    "hyperthought.metadata.MetadataItem"
                )

    def add_path(self, path, hash=None, end_bytes=None, id_=None):
        """Add a path to the manifest."""
        path = utils.clean_path(path)
        self._validate_path(path)
        path_is_folder = os.path.isdir(path)
        size = None if path_is_folder else os.path.getsize(path)

        # Exit early if the path has already been added.
        if self.has_path(path):
            # Update data if provided.
            if id_ is not None:
                current_id = self.get_path_id(path)

                if current_id != id_:
                    node = self._id_to_node[current_id]
                    node["id"] = id_
                    del self._id_to_node[current_id]
                    self._id_to_node[id_] = node

            if hash is not None:
                current_id = self.get_path_id(path)
                node = self._id_to_node[current_id]
                node["hash"] = hash

            if end_bytes is not None:
                current_id = self.get_path_id(path)
                node = self._id_to_node[current_id]
                node["end_bytes"] = end_bytes

            return

        tokens = self._get_path_tokens(path)
        len_tokens = len(tokens)
        current_location = self._path_graph

        for i in range(len_tokens):
            token = tokens[i]

            if token in current_location:
                # NOTE:  If the last token exists, the path exists.  See above.
                node = current_location[token]
            else:
                is_last = i == len_tokens - 1
                is_folder = not is_last or path_is_folder

                if id_ and is_last:
                    current_path_id = id_
                else:
                    current_path_id = utils.generate_id()

                node = {
                    "id": current_path_id,
                    "type": "folder" if is_folder else "file",
                    "children": {},
                    "relative_path": os.path.join(*tokens[:(i + 1)]),
                    "size": None if not is_last else size,
                    "hash": None if not is_last else hash,
                    "end_bytes": None if not is_last else end_bytes,
                }

                current_location[token] = node
                self._id_to_node[current_path_id] = node

            current_location = node["children"]

    def _get_path_tokens(self, path):
        """Get path tokens for the part of the path not ignored."""
        return path.split(os.path.sep)[self._ignore_path_token_count:]

    def _validate_path(self, path):
        """Determine whether a path is valid."""
        path = utils.clean_path(path)

        if (
            self.ignore_path
            and
            not path.startswith(self.ignore_path)
        ):
            raise ValueError(
                f"path '{path}' does not begin with "
                f"'{self.ignore_path}'"
            )

        if not os.path.isfile(path) and not os.path.isdir(path):
            raise ValueError("path must be a file or directory")

    def has_path(self, path):
        """Determine whether a path has already been added."""
        path = utils.clean_path(path)
        self._validate_path(path)
        tokens = self._get_path_tokens(path)
        current_location = self._path_graph

        for token in tokens:
            if token not in current_location:
                return False

            current_location = current_location[token]['children']

        return True

    def get_path_id(self, path):
        """Get internal id associated with a path."""
        path = utils.clean_path(path)

        if not self.has_path(path):
            raise PathNotFoundException(
                f"path '{path}' has not been added to the manifest")

        tokens = self._get_path_tokens(path)
        location = self._path_graph
        id_ = None

        for token in tokens:
            id_ = location[token]["id"]
            location = location[token]["children"]

        return id_

    def _validate_id(self, id_):
        if not id_ in self._id_to_node:
            raise ValueError(f"id '{id_}' not found")

    def _validate_ids(self, ids):
        for id_ in ids:
            self._validate_id(id_)

    def get_progeny(self, folder_id, depth=None):
        """
        Get a list of ids for progeny of a given path.

        Parameters
        ----------
        folder_id : str
            The internal id of the folder of interest.  See get_path_id.
        depth : int or None
            The maximum distance between the path and its progeny.
            For example, depth=1 would get children only, depth=2 would get
            children and grandchildren, etc.
            If None, there will be no limit to the depth.

        Returns
        -------
        A list of ids for files/folders that are progeny up to the indicated
        depth.
        """
        if depth is not None and not (isinstance(depth, int) and depth >= 1):
            raise ValueError("depth must be a positive integer if provided")

        self._validate_id(folder_id)

        def add_progeny(node, depth, progeny_ids):
            """Add progeny ids in place."""
            maximum_depth_reached = False

            if depth is not None:
                depth -= 1

                if depth < 1:
                    maximum_depth_reached = True

            for node_name in node["children"]:
                child_node = node["children"][node_name]
                progeny_ids.append(child_node["id"])

                if not maximum_depth_reached and child_node["children"]:
                    add_progeny(child_node, depth, progeny_ids)

        node = self._id_to_node[folder_id]
        progeny_ids = []
        add_progeny(node=node, depth=depth, progeny_ids=progeny_ids)
        return progeny_ids

    def _validate_parser(self, parser_class_name):
        if parser_class_name not in ht.parsers.PARSERS:
            raise ValueError(f"parser '{parser_class_name}' not found")

    def add_parser(self, file_id, parser_class_name, apply_to_file_ids):
        """
        Add a parser application to the manifest.

        Parameters
        ----------
        file_id : str
            The id of the file to be parsed.
        parser_class_name : str
            The class name of the parser to be used.
        apply_to_file_ids : list of str
            Internal ids of files/folders to which the parsed metadata will
            be applied.
        """
        self._validate_id(file_id)
        self._validate_ids(apply_to_file_ids)
        self._validate_parser(parser_class_name)
        self._parsers.append({
            "file_id": file_id,
            "parser_class_name": parser_class_name,
            "apply_to_file_ids": apply_to_file_ids,
        })

    def add_metadata(self, metadata, apply_to_file_ids):
        """
        Add file-specific metadata to the manifest.

        Parameters
        ----------
        metadata : list of MetadataItem
            The metadata of interest.
        apply_to_file_ids : list of str
            Internal ids of files/folders to which the metadata will be
            applied.
        """
        self._validate_metadata(metadata)
        self._validate_ids(apply_to_file_ids)
        self._metadata.append({
            'metadata': metadata,
            'apply_to_file_ids': apply_to_file_ids,
        })

    def _compute_file_info_with_pool(self, n_processes):
        """Compute file hashes and end bytes using a process pool."""
        if (
            n_processes is not None
            and
            not (isinstance(n_processes, int) and n_processes > 0)
        ):
            raise ValueError(
                "n_processes must be a positive integer if provided")

        if n_processes is None:
            n_processes = multiprocessing.cpu_count() * 2

        files = [
            {
                "id": node["id"],
                "path": os.path.join(self.ignore_path, node["relative_path"]),
            }
            for _, node in self._id_to_node.items()
            if node["type"] == "file"
        ]
        pool = multiprocessing.Pool(processes=n_processes)
        outputs = pool.map(_compute_hash_and_end_bytes, files)
        pool.close()
        pool.join()

        for output in outputs:
            node = self._id_to_node[output["id"]]
            node["hash"] = output["hash"]
            node["end_bytes"] = output["end_bytes"]

    def _compute_file_info_without_pool(self):
        """Compute file hashes and end bytes in the current process."""
        for _, node in self._id_to_node.items():
            if node["type"] != "file":
                continue

            path = os.path.join(self.ignore_path, node["relative_path"])
            node["hash"] = utils.get_hash(path)
            node["end_bytes"] = utils.get_end_bytes(path)

    def compute_file_info(self, use_pool=True, n_processes=None):
        """Compute hash and end_bytes for each file in the manifest."""
        if use_pool:
            self._compute_file_info_with_pool(n_processes=n_processes)
        else:
            self._compute_file_info_without_pool()

    def write(self, path_to_manifest):
        """Write data to manifest file."""
        manifest_data = {
            "job": {
                "name": self._job_name,
                "username": self._username,
                "workspaceAlias": self._workspace_alias,
                "hyperthoughtRootPath": self._hyperthought_root,
                "ignorePathPrefix": self.ignore_path,
            },
            "files": [
                {
                    "id": node["id"],
                    "path": os.path.join(
                        self.ignore_path, node["relative_path"]),
                    "type": node["type"],
                    "size": node["size"],
                    "hash": node["hash"],
                    "endBytes": node["end_bytes"],
                }
                for _, node in self._id_to_node.items()
            ],
            "metadata": {
                "common": ht.metadata.to_api_format(self.common_metadata),
                "parsing": [
                    {
                        "parserClass": parser["parser_class_name"],
                        "parseFileId": parser["file_id"],
                        "applyToFileIds": parser["apply_to_file_ids"],
                    }
                    for parser in self._parsers
                ],
                "fileSpecific": [
                    {
                        "metadata": ht.metadata.to_api_format(
                            entry["metadata"]),
                        "applyToFileIds": entry["apply_to_file_ids"],
                    }
                    for entry in self._metadata
                ]
            }
        }

        with open(path_to_manifest, "w") as f:
            json.dump(manifest_data, f, indent=2)

    @classmethod
    def read(cls, path_to_manifest):
        """Create a manifest object from a manifest file."""
        if not os.path.exists(path_to_manifest):
            raise ValueError(f"Invalid path: {path_to_manifest}")

        with open(path_to_manifest) as f:
            manifest_data = json.load(f)

        manifest = cls(
            job_name=manifest_data["job"]["name"],
            username=manifest_data["job"]["username"],
            workspace_alias=manifest_data["job"]["workspaceAlias"],
            hyperthought_root=manifest_data["job"]["hyperthoughtRootPath"],
            ignore_path=manifest_data["job"]["ignorePathPrefix"],
        )

        for file_ in manifest_data["files"]:
            kwargs = {
                "id_": file_["id"],
                "path": file_["path"],
            }

            if "hash" in file_:
                kwargs["hash"] = file_["hash"]

            if "endBytes" in file_:
                kwargs["end_bytes"] = file_["endBytes"]

            manifest.add_path(**kwargs)

        manifest.common_metadata = ht.metadata.from_api_format(
            metadata=manifest_data["metadata"]["common"],
        )

        for metadata_listing in manifest_data["metadata"]["fileSpecific"]:
            metadata = ht.metadata.from_api_format(
                metadata=metadata_listing["metadata"],
            )
            manifest.add_metadata(
                metadata=metadata,
                apply_to_file_ids=metadata_listing["applyToFileIds"],
            )

        for parser_listing in manifest_data["metadata"]["parsing"]:
            manifest.add_parser(
                file_id=parser_listing["parseFileId"],
                parser_class_name=parser_listing["parserClass"],
                apply_to_file_ids=parser_listing["applyToFileIds"],
            )

        return manifest
