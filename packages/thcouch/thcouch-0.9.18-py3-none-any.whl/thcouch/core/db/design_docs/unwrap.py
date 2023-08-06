__all__ = [
    'get_design_docs',
    'post_design_docs',
]

from thresult import auto_unwrap

import thcouch.core.db.design_docs


get_design_docs = auto_unwrap(thcouch.core.db.design_docs.get_design_docs)
post_design_docs = auto_unwrap(thcouch.core.db.design_docs.post_design_docs)
