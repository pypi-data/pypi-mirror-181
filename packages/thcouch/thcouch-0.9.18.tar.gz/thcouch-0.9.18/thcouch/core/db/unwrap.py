__all__ = [
    'get_all_docs',
    'bulk_docs',
    'bulk_get',
    'delete_db',
    'find_db',
    'get_db',
    'head_db',
    'post_db',
    'put_db',
]

from thresult import auto_unwrap

import thcouch.core.db


get_all_docs = auto_unwrap(thcouch.core.db.get_all_docs)
bulk_docs = auto_unwrap(thcouch.core.db.bulk_docs)
bulk_get = auto_unwrap(thcouch.core.db.bulk_get)
delete_db = auto_unwrap(thcouch.core.db.delete_db)
find_db = auto_unwrap(thcouch.core.db.find_db)
get_db = auto_unwrap(thcouch.core.db.get_db)
head_db = auto_unwrap(thcouch.core.db.head_db)
post_db = auto_unwrap(thcouch.core.db.post_db)
put_db = auto_unwrap(thcouch.core.db.put_db)
