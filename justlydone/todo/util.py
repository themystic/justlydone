# Copyright (C) 2012  The Boulevard Platform Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributors:
#  - Tom Aratyn <tom@aratyn.name>

from django.core.serializers import json
from django.utils import simplejson
from django.utils.cache import add_never_cache_headers
from tastypie.serializers import Serializer


class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data,
                                cls=json.DjangoJSONEncoder,
                                sort_keys=True,
                                ensure_ascii=False,
                                indent=self.json_indent)


def do_not_cache_response(view):
    def add_do_not_cache_headers(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        add_never_cache_headers(response)
        return response
    return add_do_not_cache_headers
