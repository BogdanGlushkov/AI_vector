from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

import asyncio

TELEGRAM_TOKEN=""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    answers = retriever.invoke(question)
    result = chain.invoke({"answers": answers, "question": question})
    await update.message.reply_text(result)


model = OllamaLLM(model="deepseek-r1:14b")

template = """
Ты эксперт в ответах на вопросы о услугах жкх (горячая вода, электроэнергия)

Здесь факты об ответах на самые популярные вопросы: {answers}

Здесь вопросы на которые нужно ответить: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен")
    await app.run_polling()
    
if __name__ == "__main__":
    asyncio.run(main())