from typing import Set

from backend.core import run_llm
import streamlit as st
import time

st.set_page_config(
    page_title="ChatDB"
    )
st.header("ChatDB - Chat with your database")

st.html(
    """
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <span style="font-size: 1rem; color: #888;">Powered by Langchain&nbsp;</span>
    </div>
    """
)


prompt = st.chat_input(
    "Ask to generate an SQL query or answer a question about your database"
)
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


def stream_data(data):
    """Stream data to the Streamlit app."""
    for chunk in data.split(" "):
        yield chunk + " "
        time.sleep(0.05)  # Add a space after each chunk for better readability


if prompt:
    with st.status("Generating response..") as status:
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        # sources = set(
        #     [doc.metadata["source"] for doc in generated_response["source_documents"]]
        # )

        formatted_response = f"{generated_response['result']} \n\n"
        status.update(label="Generation complete!", state="complete")

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))


if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        st.chat_message("user").write(user_query)
        if generated_response == st.session_state["chat_answers_history"][-1]:
            st.chat_message(
                "assistant",
            ).write_stream(stream_data(generated_response))
        else:
            st.chat_message(
                "assistant",
            ).write(generated_response)
