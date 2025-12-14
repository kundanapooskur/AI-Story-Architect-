# In your LangChain QA tab, replace with:

with tab6:
    st.header("🔗 Literary Q&A System")
    st.info("�� Powered by LangChain + Pinecone RAG")
    
    # Book selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        question = st.text_input(
            "Ask a question",
            placeholder="Who is Elizabeth Bennet? What themes are explored?"
        )
    
    with col2:
        book_filter = st.selectbox(
            "Search in:",
            ["All Books", "Frankenstein", "Pride and Prejudice", 
             "The Great Gatsby", "Elena's Story (Fantasy)"]
        )
    
    # Sample questions
    with st.expander("💡 Sample Questions"):
        st.write("**Character Questions:**")
        st.write("- Who is Elizabeth Bennet?")
        st.write("- Describe Victor Frankenstein")
        st.write("- What is Jay Gatsby's background?")
        st.write()
        st.write("**Theme Questions:**")
        st.write("- What themes are in Pride and Prejudice?")
        st.write("- How is ambition portrayed in Frankenstein?")
        st.write("- What does the green light symbolize?")
        st.write()
        st.write("**Comparative:**")
        st.write("- Compare class themes across the books")
        st.write("- How do the protagonists differ?")
    
    if st.button("🤔 Ask Question", type="primary"):
        if question:
            with st.spinner("Searching literary database..."):
                # Search logic here
                from pinecone import Pinecone
                from openai import OpenAI
                
                pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
                openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                index = pc.Index("story-memory")
                
                # Get embedding
                response = openai_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=question
                )
                query_embedding = response.data[0].embedding
                
                # Search with filter
                if book_filter != "All Books":
                    book_name = book_filter.replace(" (Fantasy)", "")
                    if "Elena" in book_name:
                        results = index.query(
                            vector=query_embedding,
                            top_k=5,
                            include_metadata=True,
                            filter={"type": "novel_chapter"}
                        )
                    else:
                        results = index.query(
                            vector=query_embedding,
                            top_k=5,
                            include_metadata=True,
                            filter={"title": book_name}
                        )
                else:
                    results = index.query(
                        vector=query_embedding,
                        top_k=5,
                        include_metadata=True
                    )
                
                if results.matches:
                    # Build context
                    context = "\n\n".join([
                        match.metadata.get('text', '')[:500] 
                        for match in results.matches
                    ])
                    
                    # Generate answer
                    answer_response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Answer based on literary passages."},
                            {"role": "user", "content": f"Context: {context}\n\nQ: {question}"}
                        ],
                        max_tokens=400
                    )
                    
                    st.success("📚 Answer:")
                    st.write(answer_response.choices[0].message.content)
                    
                    # Show sources
                    with st.expander(f"📄 {len(results.matches)} Sources"):
                        for i, match in enumerate(results.matches, 1):
                            title = match.metadata.get('title', 'Unknown')
                            author = match.metadata.get('author', 'Unknown')
                            text = match.metadata.get('text', '')[:300]
                            
                            st.write(f"**{i}. {title}** by {author}")
                            st.write(f"Score: {match.score:.3f}")
                            st.caption(text + "...")
                            st.markdown("---")
                else:
                    st.warning("No relevant passages found.")
        else:
            st.warning("Please enter a question!")
