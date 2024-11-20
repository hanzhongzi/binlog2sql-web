import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from binlog2sql_web.source_code.binlog2sql import Binlog2sql
from typing import Dict, Any
from datetime import datetime

# 默认参数配置 - 用于解析 MySQL binlog 的默认参数设置
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



@csrf_exempt  # 测试环境下 CSRF 豁免
def run_binlog2sql(request):
    """
    处理 binlog 解析请求的主要视图函数
    接收 POST 请求，解析 binlog 并返回结果
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

    try:
        # 解析请求数据
        data = json.loads(request.body)
        print("接收到的请求数据:", data)

        # 校验和清理数据
       
        args = {**default_args, **data}
        print("清理后的数据:", data)
        print("合并后的参数:", args)

        # 设置 Binlog2sql 的连接参数
        connection_settings = {
            'host': args['host'],
            'port': int(args['port']),
            'user': args['user'],
            'passwd': args['password'],
            'charset': 'utf8',
        }
        print("连接设置:", connection_settings)

        # 实例化 Binlog2sql 对象
        binlog2sql = Binlog2sql(
            connection_settings=connection_settings,
            start_file=args['start_file'],
            start_pos=args['start_pos'],
            end_file=args['end_file'],
            end_pos=args['end_pos'],
            start_time=args['start_time'],
            stop_time=args['stop_time'],
            only_schemas=[args['databases']] if args['databases'] else None,
            only_tables=[args['tables']] if args['tables'] else None,
            no_pk=args['no_pk'],
            flashback = str(args['flashback']).lower() != 'false',
            stop_never=args['stop_never'],
            back_interval=args['back_interval'],
            only_dml=args['only_dml'],
            sql_type=args['sql_type']
        )
        
        # 执行 binlog 解析
        output = binlog2sql.process_binlog()
        print("Binlog 解析结果:", output)
        return JsonResponse({'status': 'success', 'output': output})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'}, status=400)
    except ValueError as ve:
        return JsonResponse({'status': 'error', 'message': str(ve)}, status=400)
    except Exception as e:
        print("执行错误:", str(e))
        import traceback
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': f"Internal error: {str(e)}"}, status=500)

def binlog_form(request):
    """
    渲染 binlog 解析表单页面
    """
    return render(request, 'binlog_form.html')

def index(request):
    """
    渲染首页
    """
    return render(request, 'index.html')
