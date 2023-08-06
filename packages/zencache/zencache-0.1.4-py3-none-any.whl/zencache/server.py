#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement


__all__ = [
    "ZencachedApplication",
    "zencached_application",
]


from zenutils import dictutils
from orpc import SimpleOrpcApplication

class ZencachedApplication(SimpleOrpcApplication):
    default_server_port = 6679

    def get_default_config(self):
        config = super().get_default_config()
        dictutils.deep_merge(config, {
            "services": [{
                "class": "zencache.service.ZenCacheService",
            }],
            "authentication": {
                "event": "zencache.login",
            }
        })
        return config

    def main(self):
        from gevent import monkey
        monkey.patch_all()
        return super().main()

zencached_application = ZencachedApplication().get_controller()


if __name__ == "__main__":
    zencached_application()
