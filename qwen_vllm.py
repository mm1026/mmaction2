from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.entrypoints.openai import api_server
from vllm.entrypoints.openai.serving_chat import OpenAIServingChat
from transformers import AutoTokenizer
import os

# 设置HF镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


class CustomOpenAIServingChat(OpenAIServingChat):
    def __init__(self, engine, served_model, response_role):
        super().__init__(engine, served_model, response_role)
        # 加载原始tokenizer用于聊天模板
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")

    async def create_chat_completion(self, request, raw_request):
        # 使用原始tokenizer应用聊天模板
        prompt = self.tokenizer.apply_chat_template(
            request.messages,
            tokenize=False,
            add_generation_prompt=True
        )
        # 替换原始请求的messages为格式化后的prompt
        request.messages = []
        request.prompt = prompt
        return await super().create_chat_completion(request, raw_request)


def main():
    # 解析引擎参数
    engine_args = AsyncEngineArgs(
        model="Qwen/Qwen2.5-Coder-7B-Instruct",
        tensor_parallel_size=torch.cuda.device_count(),
        gpu_memory_utilization=0.9,
        dtype="auto"
    )
    engine = AsyncLLMEngine.from_engine_args(engine_args)

    # 创建自定义API服务
    served_model = "Qwen2.5-Coder-7B-Instruct"
    openai_serving_chat = CustomOpenAIServingChat(
        engine, served_model, response_role="assistant"
    )

    # 启动服务器
    api_server.served_model = served_model
    api_server.openai_serving_chat = openai_serving_chat
    api_server.app.router.post("/v1/chat/completions")(api_server.create_chat_completion)

    api_server.run_server(
        host="0.0.0.0",
        port=5000,
    )


if __name__ == "__main__":
    print('yes')
    main()
