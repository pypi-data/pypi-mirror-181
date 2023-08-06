__all__ = [
    'BaseIndex',
    'BaseModel',
    'BaseObject',
    'Field',
]

from thresult import auto_unwrap

import thcouch.orm.decl


BaseIndex = auto_unwrap(thcouch.orm.decl.BaseIndex)
BaseModel = auto_unwrap(thcouch.orm.decl.BaseModel)
BaseObject = auto_unwrap(thcouch.orm.decl.BaseObject)
Field = auto_unwrap(thcouch.orm.decl.Field)
