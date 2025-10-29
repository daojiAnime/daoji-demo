"""
nb_log 高级示例 4: Web 框架集成

这个示例展示了如何在 Web 框架中使用 nb_log：
- Flask 集成
- FastAPI 集成
- 自动捕获框架日志
"""

print("=== Web 框架集成示例 ===\n")

# ========================================
# 1. Flask 集成
# ========================================
print("=== 1. Flask 集成 ===\n")

print("创建 Flask 应用:")
print("""
from flask import Flask
from nb_log import get_logger

# 创建 Flask 应用
app = Flask('my_flask_app')

# 配置日志 - 在创建应用后立即配置
nb_log.get_logger('werkzeug', log_filename='flask_requests.log')
nb_log.get_logger('my_flask_app', log_filename='flask_app.log')

@app.route('/')
def index():
    logger = nb_log.get_logger('my_flask_app')
    logger.info('访问首页')
    return 'Hello World!'

@app.route('/error')
def error_page():
    # 未捕获的异常会自动记录
    raise Exception('测试异常')

if __name__ == '__main__':
    app.run(debug=True)
""")

print("访问 http://localhost:5000/ 时:")
print("  - werkzeug.log 会记录 HTTP 请求信息")
print("  - my_flask_app.log 会记录应用日志")
print()

# ========================================
# 2. FastAPI 集成
# ========================================
print("=== 2. FastAPI 集成 ===\n")

print("创建 FastAPI 应用:")
print("""
from fastapi import FastAPI
from nb_log import get_logger
import uvicorn

# 创建 logger
logger = get_logger('fastapi_app', log_filename='fastapi.log')

# 创建 FastAPI 应用
app = FastAPI()

@app.get('/')
async def root():
    logger.info('访问根路径')
    return {'message': 'Hello World'}

@app.get('/users/{user_id}')
async def get_user(user_id: int):
    logger.info(f'查询用户: {user_id}')
    return {'user_id': user_id, 'name': 'Test User'}

@app.post('/users')
async def create_user(name: str):
    logger.info(f'创建用户: {name}')
    return {'name': name, 'id': 1}

# 自定义异常处理
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logger.error(f'未处理的异常: {exc}', exc_info=True)
    return {'error': str(exc)}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
""")

print("特点:")
print("  - 自动记录所有 API 请求")
print("  - 捕获异常并记录堆栈信息")
print("  - 支持异步日志记录")
print()

# ========================================
# 3. 请求中间件 - 更详细的日志
# ========================================
print("=== 3. 添加请求日志中间件 ===\n")

print("FastAPI 中间件示例:")
print("""
from fastapi import Request
import time

logger = get_logger('api_middleware', log_filename='api_requests.log')

@app.middleware('http')
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 记录请求信息
    logger.info(f'请求开始: {request.method} {request.url.path}')
    
    # 处理请求
    response = await call_next(request)
    
    # 记录响应信息
    process_time = time.time() - start_time
    logger.info(
        f'请求完成: {request.method} {request.url.path} '
        f'状态码={response.status_code} '
        f'耗时={process_time:.2f}s'
    )
    
    return response
""")
print()

# ========================================
# 4. 结构化日志 - 便于分析
# ========================================
print("=== 4. 结构化日志（推荐）===\n")

print("使用 extra 参数添加结构化信息:")
print("""
@app.get('/api/orders/{order_id}')
async def get_order(order_id: int, user_id: int):
    logger.info(
        '查询订单',
        extra={
            'order_id': order_id,
            'user_id': user_id,
            'action': 'get_order',
            'api': '/api/orders'
        }
    )
    return {'order_id': order_id}
""")

print("这样可以:")
print("  - 在日志中包含结构化数据")
print("  - 便于后续分析和搜索")
print("  - 配合 Elasticsearch 进行高级查询")
print()

# ========================================
# 5. 性能监控
# ========================================
print("=== 5. 性能监控 ===\n")

print("记录慢查询:")
print("""
import time

@app.get('/api/slow')
async def slow_endpoint():
    start = time.time()
    
    # 执行业务逻辑
    result = do_some_work()
    
    elapsed = time.time() - start
    if elapsed > 1.0:  # 超过 1 秒
        logger.warning(
            f'慢请求: /api/slow 耗时 {elapsed:.2f}s',
            extra={'elapsed': elapsed, 'threshold': 1.0}
        )
    
    return result
""")
print()

# ========================================
# 6. 完整示例
# ========================================
print("=== 6. 完整的 FastAPI + nb_log 示例 ===\n")

print("""
from fastapi import FastAPI, Request, HTTPException
from nb_log import get_logger
import time

# 创建不同用途的 logger
request_logger = get_logger('api_requests', log_filename='requests.log')
business_logger = get_logger('business', log_filename='business.log')
error_logger = get_logger('errors', 
                         log_filename='errors.log',
                         error_log_filename='errors_only.log')

app = FastAPI(title='My API')

# 请求日志中间件
@app.middleware('http')
async def log_middleware(request: Request, call_next):
    start = time.time()
    
    request_logger.info(f'→ {request.method} {request.url.path}')
    
    try:
        response = await call_next(request)
        elapsed = time.time() - start
        
        request_logger.info(
            f'← {request.method} {request.url.path} '
            f'[{response.status_code}] {elapsed:.3f}s'
        )
        
        # 慢请求警告
        if elapsed > 1.0:
            request_logger.warning(f'慢请求警告: {request.url.path} ({elapsed:.2f}s)')
        
        return response
        
    except Exception as e:
        error_logger.error(f'请求处理失败: {e}', exc_info=True)
        raise

# API 端点
@app.get('/users/{user_id}')
async def get_user(user_id: int):
    business_logger.info(f'查询用户: {user_id}')
    
    if user_id < 0:
        error_logger.error(f'无效的用户ID: {user_id}')
        raise HTTPException(status_code=400, detail='Invalid user ID')
    
    return {'user_id': user_id, 'name': f'User {user_id}'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
""")

print("\n✅ Web 框架集成示例完成！")
print("\n💡 最佳实践:")
print("  1. 为不同类型的日志创建独立的 logger")
print("     - requests_logger: 记录所有 HTTP 请求")
print("     - business_logger: 记录业务逻辑")
print("     - error_logger: 专门记录错误")
print()
print("  2. 使用中间件统一处理日志")
print("     - 自动记录请求/响应")
print("     - 计算请求耗时")
print("     - 捕获异常")
print()
print("  3. 添加结构化信息")
print("     - 使用 extra 参数")
print("     - 便于后续分析")
print()
print("  4. 监控性能")
print("     - 记录慢请求")
print("     - 设置告警阈值")
print()
print("  5. 生产环境配置")
print("     - 配置 log_level_int=20 (INFO)")
print("     - 启用文件轮转")
print("     - 集成外部服务（Elasticsearch/MongoDB）")
