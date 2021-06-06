import redis
import sys
import ops.config as cfg
from neo4j import GraphDatabase

rediscfg = cfg.redis
neocfg = cfg.neo4j


rconnection = redis.Redis(host=rediscfg["host"], port=rediscfg["port"], db=0, decode_responses=True)
nconnection = GraphDatabase.driver("bolt://localhost:7687", auth=(neocfg["user"], neocfg["pass"]))
 
def rconnect():
    try:
        rconnection.ping()
    except Exception as err:
        sys.exit(err)

