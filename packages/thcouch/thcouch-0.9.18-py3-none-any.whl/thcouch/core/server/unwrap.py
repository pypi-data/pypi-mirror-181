__all__ = [
    'get_all_dbs',
    'post_dbs_info',
    'get_server',
]

from thresult import auto_unwrap

import thcouch.core.server


get_all_dbs = auto_unwrap(thcouch.core.server.get_all_dbs)
post_dbs_info = auto_unwrap(thcouch.core.server.post_dbs_info)
get_server = auto_unwrap(thcouch.core.server.get_server)