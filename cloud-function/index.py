# -*- coding: utf-8 -*-
"""
腾讯混元大模型云函数
用于流量卡智能顾问AI对话
"""
import json
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models

# 从环境变量读取密钥（部署时配置）
SECRET_ID = os.environ.get('TENCENT_SECRET_ID', '')
SECRET_KEY = os.environ.get('TENCENT_SECRET_KEY', '')
APP_ID = os.environ.get('TENCENT_APP_ID', '1258843033')

# 系统提示词 - 定义AI角色和能力
SYSTEM_PROMPT = """你是「流量卡智能顾问」，专门帮助用户推荐最适合的手机流量卡套餐。

【你的能力】
1. 根据用户需求（预算、流量、通话、运营商偏好）推荐套餐
2. 解释套餐详情：月租、流量、通话、归属地、合约期等
3. 对比不同套餐的优缺点
4. 回答关于办理流程、激活、售后等问题

【推荐原则】
- 优先推荐全国通用、无合约、不虚量的正规套餐
- 学生党预算有限，推荐低月租高性价比套餐
- 大流量需求用户，推荐200G以上套餐
- 通话需求用户，推荐含免费通话分钟的套餐

【回答风格】
- 专业、亲切、简洁
- 用emoji增加亲和力
- 给出明确的推荐理由
- 必要时提醒用户注意合约期、优惠期等细节

【可用套餐数据】
当前系统有142个套餐，涵盖电信、移动、联通、广电四大运营商，包括省内套餐和全国套餐。"""

def main_handler(event, context):
    """
    云函数入口
    """
    # 处理CORS预检请求
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"message": "OK"})
        }
    
    try:
        # 解析请求体
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        user_message = body.get('message', '')
        history = body.get('history', [])  # 对话历史，用于多轮对话
        
        if not user_message:
            return response_error("请输入消息")
        
        # 调用腾讯混元
        reply = call_hunyuan(user_message, history)
        
        return response_success({
            "reply": reply,
            "type": "text"
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return response_error(f"服务异常: {str(e)}")

def call_hunyuan(user_message, history=None):
    """
    调用腾讯混元大模型
    """
    try:
        # 认证
        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        
        # HTTP配置
        httpProfile = HttpProfile()
        httpProfile.endpoint = "hunyuan.tencentcloudapi.com"
        
        # 客户端配置
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        
        # 创建客户端
        client = hunyuan_client.HunyuanClient(cred, "", clientProfile)
        
        # 构建消息
        messages = [{"Role": "system", "Content": SYSTEM_PROMPT}]
        
        # 添加历史对话（最多保留5轮）
        if history and len(history) > 0:
            for msg in history[-10:]:  # 最近10条
                role = "user" if msg.get("isUser") else "assistant"
                messages.append({"Role": role, "Content": msg.get("content", "")})
        
        # 添加当前用户消息
        messages.append({"Role": "user", "Content": user_message})
        
        # 构建请求
        req = models.ChatCompletionsRequest()
        req.Model = "hunyuan-lite"  # 使用轻量版，速度快成本低
        req.Messages = messages
        req.Stream = False
        
        # 调用API
        resp = client.ChatCompletions(req)
        
        # 解析响应
        if resp.Choices and len(resp.Choices) > 0:
            return resp.Choices[0].Message.Content
        else:
            return "抱歉，我暂时无法回答，请稍后再试。"
            
    except TencentCloudSDKException as err:
        print(f"TencentCloudSDKException: {err}")
        return f"服务暂时不可用，请稍后重试。"
    except Exception as e:
        print(f"Exception: {str(e)}")
        return "抱歉，我遇到了一些问题，请稍后再试。"

def response_success(data):
    """成功响应"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "code": 0,
            "message": "success",
            "data": data
        }, ensure_ascii=False)
    }

def response_error(message):
    """错误响应"""
    return {
        "statusCode": 500,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "code": -1,
            "message": message,
            "data": None
        }, ensure_ascii=False)
    }

# 本地测试入口
if __name__ == "__main__":
    # 测试
    test_event = {
        "body": json.dumps({
            "message": "学生党，预算20以内，推荐什么套餐？",
            "history": []
        })
    }
    result = main_handler(test_event, None)
    print(json.dumps(result, ensure_ascii=False, indent=2))