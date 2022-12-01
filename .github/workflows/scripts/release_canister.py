from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
import os
import sys
import base64
from ic.candid import encode, Types

if len(sys.argv) != 2:
  print("Usage: python3 request_canister.py <ref>")
  exit(1)

for v in ["DFX_IDENTITY_PREVIEW","POOL_CANISTER_ID"]:
  if not v in os.environ:
    print(f"request_canister.py: {v} env variable missing")
    exit(1)



private_key = base64.b64decode(os.environ["DFX_IDENTITY_PREVIEW"]).decode("utf-8")
pool_id = os.environ["POOL_CANISTER_ID"]

identity = Identity.from_pem(private_key)
client = Client()
agent = Agent(identity, client)


def release_canister():
  res = agent.update_raw(
      pool_id, "release_canister", encode([{'type': Types.Text, 'value': sys.argv[1]}]))
  return res

# print(whoami())
# print(request_canister())

release_canister()


"""
type Self = 
 service {
   check_cycles: (text) -> (variant {
                              err: text;
                              ok: nat;
                            });
   get_pool: () -> (vec record {
                          canister_id: principal;
                          ref: opt text;
                        }) query;
   release_canister: (text) -> (variant {
                                  err: text;
                                  ok;
                                });
   request_canister: (text) -> (principal);
   set_params: (InitParams) -> () oneway;
 };
type InitParams = 
 record {
   cycles_per_canister: nat;
   max_canisters: opt nat;
   min_cycles_per_canister: nat;
 };
service : (InitParams) -> Self
"""