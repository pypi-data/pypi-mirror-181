# saxonhe4py

A packaged Java Saxon HE for Python.

[![PyPI](https://img.shields.io/pypi/v/saxonhe4py.svg)]()

## Install

Java Saxon HE is made easy to install as a single Python package:

```bash
pip install saxonhe4py
```

## Usage

```python
>>> from saxonhe4py import SAXON_HE_JAR
>>> SAXON_HE_JAR
PosixPath('/Users/johndoe/dev/saxonhe4py/jdk4py/java-runtime')
```

### Command line

```python
>>> from subprocess import check_output, run, STDOUT
>>> from jdk4py import JAVA
>>> from saxonhe4py import SAXON_HE_JAR
>>>
>>> cmd_list = [str(JAVA), "-jar", str(SAXON_HE_JAR), "net.sf.saxon.Transform", "-t", "-?"] 
>>> print(check_output(cmd_list, stderr=subprocess.STDOUT, text=True))
SaxonJ-HE 11.4 from Saxonica
Java version 17.0.3
...
```

### With jsaxonpy

Could be convinient if you want to execute your code as cloud function
where there is no java VM nor Saxon are avaiable in the environment
of the container.

```python
import os
from jdk4py import JAVA
from saxonhe4py import SAXON_HE_JAR
from jsaxonpy import Xslt


os.environ.update({
    "JVM_OPTIONS": os.environ.get("JVM_OPTIONS", "-Xmx64m"),
    "CLASSPATH": os.environ.get("CLASSPATH", "") + os.pathsep + str(SAXON_HE_JAR),
    "PATH": os.environ.get("PATH", "") + os.pathsep + str(JAVA)
})

xml = "<root><child>text</child></root>"
xsl = """
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <xsl:copy-of select="."/>
  </xsl:template>
</xsl:stylesheet>
"""
t = Xslt()
print(t.transform(xml, xsl))
```

## Versioning

`saxonhe4py`'s version contains 3 numbers:

- The first 2 numbers are the Java Saxon HE version.
- The third is `saxonhe4py` specific: it starts at 0 for each Java Saxon HE version and then increases.

