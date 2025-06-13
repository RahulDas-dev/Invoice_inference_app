import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar, Tuple

from flask import Flask
from pydantic_ai import Agent, BinaryContent, ModelRetry
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.bedrock import BedrockProvider

from .prompts import PAGE_TEMPLATE, SYSTEM_MESSAGE_1, SYSTEM_MESSAGE_2, USER_MESSAGE_1
from .schemas import Invoice, InvoiceData
from .utility import get_secret_keys, image_to_byte_string, sorted_images

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InvoiceSeviceConfig:
    model1_name: str = field(default="us.meta.llama3-2-90b-instruct-v1:0")
    model2_name: str = field(default="gpt-4o")

    @classmethod
    def init_from_app(cls, app: Flask) -> "InvoiceSeviceConfig":
        with app.app_context():
            model1_name_ = app.config.get("MODEL1_NAME", "")
            model2_name_ = app.config.get("MODEL2_NAME", "")

            return InvoiceSeviceConfig(model1_name=model1_name_, model2_name=model2_name_)


class InvoiceService:
    config: ClassVar[InvoiceSeviceConfig]

    @classmethod
    def configure_from_app(cls, app: Flask) -> None:
        config_ = InvoiceSeviceConfig.init_from_app(app)
        cls.set_config(config_)

    @classmethod
    def set_config(cls, config: InvoiceSeviceConfig) -> None:
        cls.config = config

    @classmethod
    def setup_agents(cls) -> Tuple[Agent[None, str], Agent[None, Invoice]]:
        agent1 = Agent(
            model=BedrockConverseModel(
                model_name=cls.config.model1_name,
                provider=BedrockProvider(**get_secret_keys()),
            ),
            system_prompt=SYSTEM_MESSAGE_1,
            result_type=str,
            model_settings={"temperature": 0},
        )

        agent2 = Agent(
            model=OpenAIModel(cls.config.model2_name),
            system_prompt=SYSTEM_MESSAGE_2,
            result_type=Invoice,
            model_settings={"temperature": 0},
        )

        @agent2.result_validator
        async def validate_result(result: Any) -> Any:
            if isinstance(result, Invoice):
                return result
            return ModelRetry("Final result Format is not Correct ")

        return agent1, agent2

    @classmethod
    def run(cls, image_dir: str | Path) -> Tuple[InvoiceData, str]:
        agent1, agent2 = cls.setup_agents()
        pdf_content, page_no = [], 0
        for file in sorted_images(image_dir):
            page_no += 1
            logger.info(f"Agent1 Processing Page : {file.name}")
            img_byte, mimetype = image_to_byte_string(file.resolve())
            input_msg = [
                USER_MESSAGE_1,
                BinaryContent(data=img_byte, media_type=mimetype),
            ]
            result1 = agent1.run_sync(input_msg)
            pdf_content.append((page_no, PAGE_TEMPLATE.substitute(page_no=page_no, page_content=result1.data)))
        logger.info(f"Agent1 has completed the processing of {page_no} pages")
        final_result = []
        for p_no, content in pdf_content:
            logger.info(f"Agent2 Processing Page No : {p_no}")
            result2 = agent2.run_sync([content])
            if isinstance(result2.data, Invoice):
                final_result.append(result2.data)
        invoice_data = InvoiceData(details=final_result)
        return invoice_data, "\n".join(item for _, item in pdf_content)
