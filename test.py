import asyncio
import json

from gt_telem import TurismoClient
from gt_telem.models import Telemetry

async def print_telem(t: Telemetry):
    print(json.dumps(t.as_dict, indent=4))

tc = TurismoClient()
tc.register_callback(print_telem)
asyncio.run(tc.run())
