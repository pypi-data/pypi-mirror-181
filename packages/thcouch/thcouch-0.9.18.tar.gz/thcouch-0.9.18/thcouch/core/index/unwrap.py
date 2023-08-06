__all__ = [
    'get_index',
    'post_index',
    'delete_index',
]

from thresult import auto_unwrap

import thcouch.core.index


get_index = auto_unwrap(thcouch.core.index.get_index)
post_index = auto_unwrap(thcouch.core.index.post_index)
delete_index = auto_unwrap(thcouch.core.index.delete_index)