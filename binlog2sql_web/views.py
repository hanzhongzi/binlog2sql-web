import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from binlog2sql_web.source_code.binlog2sql import Binlog2sql

# 默认参数配置 - 用于解析MySQL binlog的默认参数设置
default_args = {
    'host': '127.0.0.1',          # MySQL主机地址
    'port': 3306,                 # MySQL端口号
    'user': 'root',               # MySQL用户名
    'password': '',               # MySQL密码
    'start_file': '',             # 起始binlog文件
    'start_pos': 4,               # 起始binlog位置
    'end_file': '',               # 结束binlog文件
    'end_pos': 0,                 # 结束binlog位置
    'start_time': '',             # 起始时间
    'stop_time': '',              # 结束时间
    'stop_never': False,          # 持续解析开关
    'databases': '',              # 数据库名
    'tables': '',                 # 表名
    'only_dml': False,            # 只解析DML语句
    'sql_type': ['INSERT', 'UPDATE', 'DELETE'],  # SQL类型
    'no_pk': False,               # 不显示主键
    'flashback': False,           # 闪回模式
    'back_interval': 1.0          # 闪回间隔
}

@csrf_exempt  # 禁用CSRF保护
def run_binlog2sql(request):
    """
    处理binlog解析请求的主要视图函数
    接收POST请求，解析binlog并返回结果
    """
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

            # 处理闪回模式参数
            flashback_html = False
            if args['flashback'] == 'true':
                flashback_html = True

            # 实例化 Binlog2sql 对象并设置参数
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
           
            # 执行binlog解析并获取输出
            output_value = binlog2sql.process_binlog()

            # 返回成功响应
            return JsonResponse({"status": "success", "output": output_value}, safe=False)

        except Exception as e:
            # 返回错误响应
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    else:
        # 非POST请求返回方法不允许的响应
        return JsonResponse({"status": "error", "error": "Only POST method is allowed"}, status=405)

def binlog_form(request):
    """
    渲染binlog解析表单页面
    """
    return render(request, 'binlog_form.html')

def index(request):
    """
    渲染首页
    """
    return render(request, 'index.html')
