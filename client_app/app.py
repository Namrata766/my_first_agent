import streamlit as st
import json
from agent_client import create_session, query_agent

# ----------------------------
# Streamlit UI setup
# ----------------------------
st.title("Content Creation Agent")

user_id = st.text_input("User name")


# ----------------------------
# Utility: split concatenated JSON objects
# ----------------------------
def split_concatenated_json(raw: str):
    """
    Agent Engine streaming responses often arrive as:
    {json1}{json2}{json3}

    This function splits them into a list of dicts.
    """
    objects = []
    decoder = json.JSONDecoder()
    idx = 0
    raw = raw.strip()

    while idx < len(raw):
        obj, offset = decoder.raw_decode(raw[idx:])
        objects.append(obj)
        idx += offset

        # Skip whitespace between objects
        while idx < len(raw) and raw[idx].isspace():
            idx += 1

    return objects


# ----------------------------
# Merge and format agent responses
# ----------------------------
def format_agent_responses(response):
    """
    Groups agent responses by author and merges all text content.
    """
    merged = {}

    # Normalize input
    if isinstance(response, str):
        responses = split_concatenated_json(response)
    elif isinstance(response, list):
        responses = response
    else:
        responses = [response]

    for resp in responses:
        if not isinstance(resp, dict):
            continue

        author = resp.get("author", "Unknown")

        parts = resp.get("content", {}).get("parts", [])
        text = "\n\n".join(p.get("text", "") for p in parts)

        if not text.strip():
            continue

        merged.setdefault(author, "")
        merged[author] += ("\n\n" + text) if merged[author] else text

    return merged


# ----------------------------
# Friendly author labels
# ----------------------------
def author_label(author: str) -> str:
    author_lower = author.lower()

    if "blog" in author_lower:
        return "Blog Content"
    elif "instagram" in author_lower:
        return "Reels Content"
    elif "youtube" in author_lower:
        return "YouTube Content"
    else:
        return f"{author} Content"


# ----------------------------
# Main app logic
# ----------------------------
if user_id:
    if "session_id" not in st.session_state:
        st.session_state.session_id = create_session(user_id)

    message = st.text_area("Message")
    print("Current session ID:", st.session_state.session_id)
    print("User ID:", user_id)
    print("Message:", message)

    if st.button("Send"):
        response = query_agent(
            user_id=user_id,
            session_id=st.session_state.session_id,
            message=message
        )

        print("Raw agent response:", response)

        # Format agent output
        merged = format_agent_responses(response)
        print("Formatted agent response:", merged)

        if not merged:
            st.warning("No formatted content found. Raw response below:")
            st.write(response)
        else:
            for author, text in merged.items():
                st.subheader(author_label(author))
                st.write(text)
