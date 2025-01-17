# Copyright (c) spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import spdx.file as spdxfile
from spdx.parsers import jsonparser
from spdx.parsers import yamlparser
from spdx.parsers import rdf
from spdx.parsers import xmlparser
from spdx.parsers import tagvalue
from spdx.parsers.loggers import StandardLogger
from spdx.parsers import jsonyamlxmlbuilders, tagvaluebuilders, rdfbuilders
from spdx.parsers.builderexceptions import FileTypeError


def parse_file(fn):
    buildermodules = [rdfbuilders, jsonyamlxmlbuilders, jsonyamlxmlbuilders, jsonyamlxmlbuilders, tagvaluebuilders]
    parsing_modules = [rdf, xmlparser, yamlparser, jsonparser, tagvalue]
    read_datas = [False, False, False, False, True]
    for i in range(len(buildermodules)):
        parsing_module = parsing_modules[i]
        buildermodule = buildermodules[i]
        read_data = read_datas[i]
        try:
            p = parsing_module.Parser(buildermodule.Builder(), StandardLogger())
            if hasattr(p, "build"):
                p.build()
            with open(fn) as f:
                if read_data:
                    data = f.read()
                    return p.parse(data)
                else:
                    return p.parse(f)
        except:
            if i == len(buildermodules) - 1:
                raise FileTypeError("FileType Not Supported" + str(fn))


