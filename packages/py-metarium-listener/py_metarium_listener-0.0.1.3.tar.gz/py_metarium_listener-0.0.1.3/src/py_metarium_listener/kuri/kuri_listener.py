import re

from ..base import BaseListener
from ..utils import QueryParameter


METARIUM_EXTRINSIC = "Metarium"
FUNCTION_CALL_SELF_REGISTER_CONTENT = "self_register_content"
FUNCTION_CALL_ADMIN_UPDATE_SCRIBE_STATUS = "force_update_scribe_authority_status"

class KuriListener(BaseListener):

    def __processed_block(self, block):
        processed_block = {
            "block_number": block["header"]["number"],
            "extrinsics": []
        }
        for extrinsic in block["extrinsics"]:
            extrinsic = extrinsic.serialize()
            if extrinsic["call"]["call_module"] == METARIUM_EXTRINSIC:
                log = {
                    "call_index": extrinsic["call"]["call_index"],
                    "call_function": extrinsic["call"]["call_function"],
                    "caller": extrinsic["address"],
                    "kuri": None,
                    "scribe": None
                }
                if log["call_function"] == FUNCTION_CALL_SELF_REGISTER_CONTENT:
                    log["kuri"] = extrinsic["call"]["call_args"][0]["value"]
                if log["call_function"] == FUNCTION_CALL_ADMIN_UPDATE_SCRIBE_STATUS:
                    log["scribe"] = extrinsic["call"]["call_args"][0]["value"]
                
                processed_block["extrinsics"].append(log)
        
        return processed_block

    def __listen(self, direction, block_hash, block_count, query):
        assert all(isinstance(parameter, QueryParameter) for parameter in query)
        
        print(f"\n\nQUERY IS {query}\n\n")
        
        for block, is_metarium in super().listen(direction, block_hash, block_count):
            if not is_metarium:
                continue
            block = self.__processed_block(block)
            if len(query):
                extrinsics = block.pop("extrinsics")
                block["extrinsics"] = []
                for extrinsic in extrinsics:
                    for parameter in query:
                        # print(f"\nparameter : {parameter}")
                        if (
                                (f"{parameter.field}" in extrinsic) and \
                                (re.search(f"{parameter.value}", f"{extrinsic[parameter.field]}"))
                            ):
                            block["extrinsics"].append(extrinsic)
                if not len(block["extrinsics"]):
                    continue

            yield block

    def listen(self, direction, block_hash=None, block_count=None, query=[]):
        query = query or []
        for block in self.__listen(direction, block_hash, block_count, query):
            yield block
