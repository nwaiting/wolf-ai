
# 1、 intervals查询
{
  "query": {
    "intervals": {
      "message": {
        "all_of": {
          "ordered": true,
          "intervals": [
            {
              "match": {
                "query": "my favorite food",
                "max_gaps": 0,
                "ordered": true
              }
            }
          ]
        }
      }
    }
  },
  "size": 15
}

# 2、 match查询
{
  "query": {
    "match": {
      "hobbies": {
        "query": "football basketball",
        "operator": "or"    (默认参数)
      }
    }
  }
}

# 3、match_phrase 短语查询
{
  "query": {
    "match_phrase": {
      "message": {
          "query": "绿豆粉",
          "analyzer":"ik_max_word"
      }
    }
  }
}

# 4、match_phrase_prefix 查询
{
    "query": {
        "match_phrase_prefix" : {
            "message" : {
                "query" : "quick brown f"
            }
        }
    }
}

# 5、multi_match 查询
{
  "query": {
    "multi_match" : {
      "query":    "this is a test",
      "fields": [ "subject", "message" ]
    }
  }
}

# 6、query string 查询
{
    "query": {
        "query_string" : {
            "query" : "(new york city) OR (big apple)",
            "default_field" : "content"
        }
    }
}

# 对多个fields进行查询
{
    "query": {
        "query_string" : {
            "fields" : ["content", "name"],
            "fields" : ["city.*"],      # fields支持通配符
            "query" : "this AND that"   # 如果要分别查询每个术语，则需要在术语周围添加显式运算符（例如this AND that）
        }
    }
}

# 查询分词
{
    "analyzer":"ik_smart",
    "text": "中华人民共和国人民大会堂"
}
