__all__ = [
    'get_doc',
    'put_doc',
    'head_doc',
    'delete_doc',
]

from thresult import auto_unwrap

import thcouch.core.doc


get_doc = auto_unwrap(thcouch.core.doc.get_doc)
put_doc = auto_unwrap(thcouch.core.doc.put_doc)
head_doc = auto_unwrap(thcouch.core.doc.head_doc)
delete_doc = auto_unwrap(thcouch.core.doc.delete_doc)