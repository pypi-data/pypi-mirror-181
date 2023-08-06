__all__ = [
    'get_attachment',
    'put_attachment',
    'head_attachment',
    'delete_attachment',
]

from thresult import auto_unwrap

import thcouch.core.attachment


get_attachment = auto_unwrap(thcouch.core.attachment.get_attachment)
put_attachment = auto_unwrap(thcouch.core.attachment.put_attachment)
head_attachment = auto_unwrap(thcouch.core.attachment.head_attachment)
delete_attachment = auto_unwrap(thcouch.core.attachment.delete_attachment)