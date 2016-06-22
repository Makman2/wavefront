import re

from wavefront.mesh import Mesh


_anti_comment_regex = re.compile("#.*")
_token_regex = re.compile("o|v")
_token_o_regex = re.compile(r" +([^\s]+)")
_token_v_regex = re.compile(r"\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)\s+"
                            r"([0-9]+\.[0-9]+)(?:\s+([0-9]+\.[0-9]+))?")


def load(string):
    """
    Yields `Mesh`es from the given wavefront-obj data string.

    :param string: The data string of the obj-file to load.
    :return:       An iterator returning `Mesh`es loaded from `string`.
    """
    mesh = None
    for line in string.splitlines():
        if line.startswith("o"):
            mesh = Mesh(name=_token_o_regex.match(line).group(1))

        if mesh:
            if line.startswith("v"):
                pass
            elif line.startswith("vn"):
                pass

    # Remove all comment strings.
    string = _anti_comment_regex.sub("", string)

    pos = 0
    mesh = None
    while True:
        token = _token_regex.search(string, pos)

        if token is None:
            break

        token_id = token.group()

        if token_id == "o":
            if mesh:
                yield mesh

            match = _token_o_regex.match(string, token.endpos)
            mesh = Mesh(match.group(1))

        elif token_id == "v":
            match = _token_v_regex.match(string, token.endpos)
            vertices = tuple(match.group(i) for i in (1, 2, 3))
            if 4 in match.groups():
                vertices += (match.group(4),)

            mesh.vertices.append(vertices)

        pos = match.endpos


def store(meshes):
    """
    Creates a wavefront-obj data-string from the given meshes.

    :param meshes: A sequence of `Mesh`es to store.
    :return:       The data string of the obj-file.
    """
    token_list = []
    for mesh in meshes:
        token_list.append("o " + mesh.name)
        for vector in mesh.vertices:
            token_list.append("v " + " ".join(vector))

    return "\n".join(token_list)
