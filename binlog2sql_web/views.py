import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from binlog2sql_web.source_code.binlog2sql import Binlog2sql

# 默认参数配置
default_args = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'start_file': '',
    'start_pos': 4,
    'end_file': '',
    'end_pos': 0,
    'start_time': '',
    'stop_time': '',
    'stop_never': False,
    'databases': '',
    'tables': '',
    'only_dml': False,
    'sql_type': ['INSERT', 'UPDATE', 'DELETE'],
    'no_pk': False,
    'flashback': False,
    'back_interval': 1.0
}

@csrf_exempt
def run_binlog2sql(request):
    if request.method == 'POST':
        try:
            # 获取请求数据并合并默认参数
            data = json.loads(request.body)
            args = {**default_args, **data}  # 将请求数据覆盖默认参数

            # 设置 Binlog2sql 连接参数
            connection_settings = {
                'host': args['host'],
                'port': int(args['port']),
                'user': args['user'],
                'passwd': args['password'],
                'charset': 'utf8'
            }

            # 处理日期时间格式
            start_time = args['start_datetime']
            stop_time = args['stop_datetime']
            flashback_html =False
            if args['flashback'] == 'true':
                flashback_html = True
                

            # 实例化 Binlog2sql
            binlog2sql = Binlog2sql(
                connection_settings=connection_settings,
                start_file=args['start_file'],
                start_pos=args['start_pos'],
                end_file=args['end_file'],
                end_pos=args['end_pos'],
                start_time=start_time,
                stop_time=stop_time,
                only_schemas=[args['database']] if args['database'] else None,
                only_tables=[args['table']] if args['table'] else None,
                no_pk=args['no_pk'],
                flashback=flashback_html,
                stop_never=args['stop_never'],
                back_interval=args['back_interval'],
                only_dml=args['only_dml'],
                sql_type=args['sql_type']
            )
           
            # 捕获 Binlog2sql 输出
            output_value = binlog2sql.process_binlog()

            return JsonResponse({"status": "success", "output": output_value}, safe=False)

        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "error": "Only POST method is allowed"}, status=405)

def binlog_form(request):
    return render(request, 'binlog_form.html')


def index(request):
    return render(request, 'index.html')
