import streamlit as st
from app.chatbot import ChatBot

def main():
    bot = ChatBot()
    bot.run()

if __name__ == "__main__":
    main()
