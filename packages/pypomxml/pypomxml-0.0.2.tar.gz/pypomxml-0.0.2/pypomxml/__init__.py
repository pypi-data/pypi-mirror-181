

from .pomparse import pomparser

__all__ = []
__author__ = "SenRanja"
__version__ = "0.0.2"
__doc__ = """pypomxml

pypomxml is python3's lib, its used to parse maven's pom.xml and maven-metadata.xml.

[NOTE]
If one of [groupId artifactId version] doesn't exist but [parent] exists, we will use parent's tag's [groupId artifactId version] as its GAV(GAV: [groupId artifactId version])

We will compelete its functions in the future!
"""




