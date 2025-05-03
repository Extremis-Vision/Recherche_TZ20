from mem0 import Memory

config = {
    "llm": {
        "provider": "lmstudio",
        "config": {
            "model": "deepthink-reasoning-7b",  # Remplace par le nom exact du mod�le charg� dans LM Studio
            "temperature": 0.7,
            "max_tokens": 1024,
            "lmstudio_base_url": "http://localhost:1234/v1"
        }
    },
    "embedder": {
        "provider": "lmstudio",
        "config": {
            "model": "text-embedding-nomic-embed-text-v1.5",  # Remplace par le nom du mod�le d'embedding
            "lmstudio_base_url": "http://localhost:1234/v1"
        }
    }
}

memory = Memory.from_config(config)

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # Recherche des souvenirs pertinents
    relevant_memories = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])

    # G�n�ration de la r�ponse
    system_prompt = f"You are a helpful AI. Answer the question based on query and memories.\nUser Memories:\n{memories_str}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]
    response = memory.chat(messages, user_id=user_id)
    assistant_response = response["choices"][0]["message"]["content"]

    # Ajout de la conversation � la m�moire
    messages.append({"role": "assistant", "content": assistant_response})
    memory.add(messages, user_id=user_id)

    return assistant_response

def main():
    print("Chat with AI (type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        print(f"AI: {chat_with_memories(user_input)}")

if __name__ == "__main__":
    main()