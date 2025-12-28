# ABOUTME: Streamlit chat UI for AWS AgentCore agent
# ABOUTME: Provides web interface to interact with deployed agent

import streamlit as st
import boto3
import json
import uuid

# === CUSTOMIZE: Update these values ===
AGENT_ARN = "arn:aws:bedrock-agentcore:us-west-2:ACCOUNT:runtime/your_agent-ID"
REGION = "us-west-2"

st.set_page_config(
    page_title="Agent Chat",
    
    layout="centered"
)

st.title("Agent Chat")
st.caption("Powered by AWS AgentCore")


def invoke_agent(prompt: str, session_id: str) -> str:
    """Call AgentCore Runtime."""
    try:
        client = boto3.client("bedrock-agentcore", region_name=REGION)
        response = client.invoke_agent_runtime(
            agentRuntimeArn=AGENT_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps({"prompt": prompt})
        )

        # Read streaming body
        body = response.get('response')
        if hasattr(body, 'read'):
            body = body.read().decode('utf-8')

        result = json.loads(body) if body else {}
        return result.get("result", str(result))
    except Exception as e:
        return f"Error: {str(e)}"


# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call AgentCore
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = invoke_agent(prompt, st.session_state.session_id)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This assistant can help you with various tasks.
    Customize this description for your agent.
    """)

    st.markdown("---")
    st.markdown(f"Session: `{st.session_state.session_id[:8]}...`")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
