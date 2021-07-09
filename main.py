import json
from flask import Flask, Response, request
from components.tsv_reader import tsv_reader
from components.print_log import print_log
from engine.search_engine import SearchEngine

# tsv 파일 읽은 뒤 dictionary로 저장
file_location = 'dataset/product_name.tsv'
raw_data = tsv_reader(file_location)

# 검색 엔진 실행
search_engine = SearchEngine(raw_data)
print_log('-----------------------------------------------------------------------------------------\n')
print_log('Running Search API...\n')

# get
app = Flask(__name__)


@app.route("/search", methods=['GET'])
def get(engine=search_engine):
    parameter_dict = request.args.to_dict()

    if parameter_dict.get('query') is None:
        return 'No query parameter'

    query = parameter_dict['query']
    search_result = json.dumps(engine.get_search_result(query), ensure_ascii=True)

    return Response(search_result, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
