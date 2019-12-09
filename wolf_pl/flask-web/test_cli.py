import click
import logging.config
import time
from elasticsearch import Elasticsearch

ELASTICSEARCH = {
    "hosts": "localhost:39200"
}

class ObjectDict(dict):
    """
    Object like dict, every dict[key] can visite by dict.key

    If dict[key] is `Get`, calculate it's value.
    """

    def __getattr__(self, name):
        ret = self.__getitem__(name)
        if hasattr(ret, '__get__'):
            return ret.__get__(self, ObjectDict)
        return ret

@click.command()
@click.option('--name',
              help='The person to greet.',default="E:\logging.conf")
@click.pass_context
def hello(ctx, **kwargs):
    #logging.config.fileConfig(kwargs['name'])

    print(type(ctx))

    #ctx.obj = ObjectDict(ctx.obj or {})
    #ctx.obj.update({'c': Client})
    #ctx.obj.update({'bc': ClientPyMySQL})
    #return ctx


if __name__ == "__main__":
    """
    es = Elasticsearch(ELASTICSEARCH['hosts'])
    print(type(es))
    begin = 0
    end = time.time()
    body = {
        "query": {
            "mast": [
                {
                    "term": {
                        "message": "body"
                    }
                },
                {
                    "range": {
                        "date_timestamp": {
                            "gte":begin,  # >=
                            "lte":end  # <=
                        }
                    }
                }
            ]
        },
        "from":1,
        "size":1
    }
    print(es.indices.exists(index="testes2"))
    try:
        res = es.search(index='testes2', body=body, size=1)
        print(res)
    except Exception as e:
        print("exception {}".format(e))
    #c = hello()
    #print(type(c))
    """

    a = 0
    if a:
        print('a is 0')

