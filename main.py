from neo4jclient import Neo4jClient
import os
from functools import wraps
from time import time


def timing(f):
    '''decorator/helper function for timing measurements'''
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap



def construct_query(skip_interval):
    '''

    :param (int) skip_interval: Interval for Neo4j SKIP Clause
    :return: (String) query: Fully Constructed Query
    '''
    query = f'MATCH (u:User) RETURN u ORDER BY u.id SKIP {skip_interval} LIMIT 10000'
    return query

def transaction_function(tx,query):
    '''
    TODO: More documentation on transaction functions can be found here: https://neo4j.com/docs/api/python-driver/current/api.html
    :param tx:
    :param query:
    :return:
    '''
    result = tx.run(query)
    values = [record.values() for record in result]
    return values



@timing
def read_results(queries:list) -> list:
    '''
    Function that takes an input of query strings in a list,  executes read transactions of those queries, and returns all the results collected in a list
    :param queries:
    :return:
    '''
    with neo4j.client.session() as session:
        results = [session.execute_read(transaction_function,query) for query in queries]
        return results






if __name__ == '__main__':

    # Connection credentials
    url = 'bolt://54.68.133.241:7687'
    username = os.environ.get('NEO4J_CENTRAL_USER')
    password = os.environ.get('NEO4J_CENTRAL_PASSWORD')
    database = os.environ.get('neo4j')





    skip_range = [x for x in range(0, 1000000, 10000)]
    queries = [construct_query(skip_interval) for skip_interval in skip_range]
    query = ['''MATCH (u:User) RETURN u.id''']
    neo4j = Neo4jClient(url=url,username=username,password=password,database=database)



    print('results with batching:')
    read_results(queries)

    print('results without batching')
    read_results(query)






















