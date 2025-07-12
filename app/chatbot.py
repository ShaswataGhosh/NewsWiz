import streamlit as st
import re
import pandas as pd
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from app.web_scrapper import webscrapper
from app.llm_prompt_chain import Llm_prompt

class ChatBot:
    def __init__(self):
        self.topic = None
        self.article = []
        self.prompt = None
        self.option = None
        self.content = None
        self.table = None
        self.command = None

    def chatbot(self):
        st.title("AI Chatbot 🤖🧠🇦🇮👾")

        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append(SystemMessage(content="Act like a helpful news chatbot."))

        # Show previous chat messages
        for message in st.session_state.messages:
            role = "user" if isinstance(message, HumanMessage) else "assistant"
            with st.chat_message(role):
                st.markdown(message.content)

        # 🧠 Show persistent news table if available
        if "news_df" in st.session_state:
            st.subheader("📰 Latest News Table")
            st.markdown(
                """
                <style>
                    .dataframe th, .dataframe td {
                        text-align: left !important;
                        white-space: normal !important;
                    }
                    .stDataFrame {
                        width: 100% !important;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.dataframe(
                st.session_state["news_df"],
                use_container_width=True,
                height=320
            )

        # Chat input
        self.prompt = st.chat_input("Hi, I am your Chatbot!")

        if self.prompt:
            st.session_state.messages.append(HumanMessage(content=self.prompt))
            with st.chat_message("user"):
                st.markdown(self.prompt)

            # 🔍 News fetch request
            if self.check_for_news_request(self.prompt):
                self.topic = self.extract_topic(self.prompt)
                with st.chat_message("assistant"):
                    st.markdown(f"🔎 Fetching top news articles on **{self.topic}**...")

                    scrapper = webscrapper(topic=self.topic)
                    self.article = scrapper.fetch_results()

                    if not self.article:
                        reply = "❌ Sorry, no articles found."
                    else:
                        df = pd.DataFrame(self.article)
                        st.session_state["news_df"] = df  # ✅ Save DataFrame for persistence

                        st.markdown(
                            """
                            <style>
                                .dataframe th, .dataframe td {
                                    text-align: left !important;
                                    white-space: normal !important;
                                }
                                .stDataFrame {
                                    width: 100% !important;
                                }
                            </style>
                            """,
                            unsafe_allow_html=True,
                        )

                        st.dataframe(df, use_container_width=True, height=320)
                        df.index = df.index + 1
                        table_markdown = df.to_markdown(index=True)
                        reply = f"📋 Top news articles on **{self.topic}**:\n\n"

                        st.session_state.messages.append(AIMessage(content=reply))

            # 🤖 LLM summarizer/explainer
            elif self.check_for_llm_request(self.prompt):
                self.option = self.option_check(prompt=self.prompt)

                if self.option:
                    article_text = " ".join(
                        [i["tagline"] for i in self.article]
                        if self.article
                        else st.session_state.get("news_df", pd.DataFrame())["tagline"].tolist()
                    )

                    result = Llm_prompt(option=self.option, article=article_text)
                    self.content = result.create_chain()
                    reply = self.content
                    st.markdown(reply)
                    st.session_state.messages.append(AIMessage(content=reply))

            # 💬 General chatbot response
            else:
                response = self.generate_response()
                with st.chat_message("assistant"):
                    st.markdown(response)
                    st.session_state.messages.append(AIMessage(content=response))

    def generate_response(self):
        llm = ChatOllama(model="llama3.2", temperature=1)
        return llm.invoke(st.session_state.messages).content

    def extract_topic(self, prompt):
        match = re.search(r'\b(?:on|about|in|from)\s+(.+)', prompt, re.IGNORECASE)
        return match.group(1).strip() if match else "a general topic"

    def check_for_news_request(self, prompt):
        return bool(re.search(r'\btop\s*(news|headlines)\b', prompt, re.IGNORECASE))

    def check_for_llm_request(self, prompt):
        return bool(re.search(r'\b(?:Summarize|Simplify|Shorten|Summary|Explain)\b', prompt, re.IGNORECASE))

    def option_check(self, prompt):
        option = re.search(r'\b(?:Summarize|Simplify|Shorten|Summary|Explain)\b', prompt, re.IGNORECASE)
        return option.group(0).lower() if option else None

    def run(self):
        self.chatbot()

# Entry point
if __name__ == "__main__":
    app = ChatBot()
    app.run()
